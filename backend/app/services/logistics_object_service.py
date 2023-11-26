import json
import logging
from http.client import HTTPException
from typing import List, Tuple

import requests
from fastapi import APIRouter
from pyld import jsonld

import config
from models.neone_automate import Rule
from models.one_record import (
    ChangeRequest,
    ApprovalStatus,
    LogisticsObject,
    Recommendation,
    OperationDetail,
    Operation,
    Decision,
)
from oidc_token_manager import OIDCTokenManager
from rule_engine import load_rule
from rule_engine.functions import *
from utils import normalize_logistics_object

router = APIRouter()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

oidc_token_manager: OIDCTokenManager = OIDCTokenManager(
    token_url=config.access_token_url,
    client_id=config.client_id,
    client_secret=config.client_secret,
)


def process_change_request(
    change_request: ChangeRequest, rules: List[Rule]
) -> ChangeRequest:
    get_goods_description(change_request.original_logistics_object)
    original_logistics_object = fetch_original_logistics_object(
        change_request.change.logistics_object.id
    )
    # apply first? or both original and new
    # if its a waybill fetch Locations
    # if (
    #     original_logistics_object.type == "https://onerecord.iata.org/ns/cargo#Waybill"
    #     and original_logistics_object.departureLocation is not None
    #     and original_logistics_object.arrivalLocation is not None
    # ):
    #     original_logistics_object.departureLocation = fetch_original_logistics_object(
    #         original_logistics_object.departureLocation.id
    #     )
    #     original_logistics_object.arrivalLocation = fetch_original_logistics_object(
    #         original_logistics_object.arrivalLocation.id
    #     )
    change_request.original_logistics_object = original_logistics_object

    new_lo, lo = apply_change_request(
        original_logistics_object, change_request
    )
    if "@graph" in new_lo:
        expanded = jsonld.compact(new_lo, ctx={})
        new_lo = expanded["@graph"]
    if isinstance(new_lo, list):
        new_lo = new_lo[0]

    new_lo["@type"] = change_request.original_logistics_object.type

    change_request.updated_logistics_object = LogisticsObject(**new_lo)

    ############################
    # Rule Engine Magic
    ############################
    if change_request is not None:
        recommendations: List[Recommendation] = []
        rule: Rule
        for rule in rules:
            try:
                logger.info(rule.rule_id)
                rule_function = load_rule(rule.function_code)
                recommendation = rule_function(change_request)
                if recommendation is not None:
                    recommendations.append(recommendation)
            except Exception as e:
                logger.error(e)
                logger.error("Failed to execute rule {}".format(rule.rule_id))

    change_request.recommendations = recommendations
    automated_decision = set(
        {recommendation.decision for recommendation in recommendations}
    )

    if automated_decision == {Decision.ACCEPTED}:
        change_request.approval_status = ApprovalStatus.AUTO_ACCEPTED
    elif automated_decision == {Decision.REJECTED}:
        change_request.approval_status = ApprovalStatus.AUTO_REJECTED
    elif not automated_decision:  # If empty == no rules applied
        change_request.approval_status = ApprovalStatus.PENDING
    else:
        change_request.approval_status = ApprovalStatus.MANUAL_CHECK_REQUIRED

    return change_request


def fetch_original_logistics_object(logistics_object_id: str) -> LogisticsObject:
    logger.info("Try to fetch {}".format(logistics_object_id))
    # get original logisticsObject from ne-one server based on change#hasLogisticsObject
    token = oidc_token_manager.get_token()
    response = requests.get(
        logistics_object_id,
        timeout=10,
        headers={
            "Accept": "application/ld+json",
            "Authorization": "Bearer {}".format(token),
        },
    )

    if response.status_code == 200:
        logger.info(
            "Successfully fetched referenced logistics object: {}".format(
                logistics_object_id
            )
        )
        original_logistics_object = response.json()
        normalized: dict = normalize_logistics_object(original_logistics_object)
        return LogisticsObject(**normalized)
    else:
        raise HTTPException(
            status_code=response.status_code,
            detail="Failed to fetch referenced logistics object",
        )


def update_recursively(data, s, p, value, datatype, op):
    """
    Recursively update JSON data with Subject-Predicate-Object style.
    
    Args:
    data (dict): JSON data to be updated.
    s (str): Subject key.
    p (str): Predicate key.
    value: Value to be updated.
    datatype (str): Data type of the value.
    op (str): Operation to perform ('add', 'update', 'delete').
    
    Returns:
    Updated JSON data.
    """

    def update_item(subj, pred, val, dtype, operation, obj):
          if isinstance(obj, dict):
              if pred in obj:
                  if operation == 'https://onerecord.iata.org/ns/api#DELETE':
                      del obj[pred]
                  else:
                      obj[pred] = {'@value': val, '@type': dtype}
              else:
                  obj[pred] = {'@value': val, '@type': dtype}
          else:
              # Handle non-dict value that cannot contain predicates
              if operation == 'https://onerecord.iata.org/ns/api#ADD':
                  raise ValueError("Cannot add predicate to non-dict value.")
              else:
                  print(f"Warning: Subject '{subj}' is not a dictionary, predicate '{pred}' cannot be updated.")

    # Split the subject string into parts (if nested)
    subject_keys = s.split('.')
    current_data = data

    # Traverse through the nested structure to locate and update the predicate
    for key in subject_keys[:-1]:
        if key in current_data:
            current_data = current_data[key]
        else:
            print(f"Warning: Subject '{key}' not found.")
            return data  # Return the original data if subject is not found

    update_item(subject_keys[-1], p, value, datatype, op, current_data)

    return data


def apply_change_request(
    original_logistics_object: LogisticsObject, change_request
) -> Tuple[str, str]:
    logger.info("original")
    logger.info(original_logistics_object)

    compacted_lo = jsonld.compact(
        original_logistics_object.model_dump(exclude_none=True, by_alias=True), {}
    )

    change = change_request.change
    operations: List[Operation] = change.operations

    new_compacted_lo = compacted_lo.copy()

    operations = sorted(operations, key=lambda operation: operation.op.id, reverse=True)

    for operation in operations:
        s = operation.s
        p = operation.p
        o: OperationDetail = operation.o
        value = o.value
        datatype = o.datatype
        op = operation.op.id
        new_compacted_lo = update_recursively(new_compacted_lo, s, p, value, datatype, op)

    normalized_lo = jsonld.normalize(
        compacted_lo, {"algorithm": "URDNA2015", "format": "application/nquads"}
    )

    # new_normalized_lo = jsonld.normalize(
    #     new_compacted_lo, {"algorithm": "URDNA2015", "format": "application/nquads"}
    # )


    return new_compacted_lo, compacted_lo
