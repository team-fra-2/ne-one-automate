import logging
from datetime import datetime, date
from typing import List, Optional

import pymongo
import requests
from fastapi import APIRouter, HTTPException, Request, Query
from pymongo.errors import ServerSelectionTimeoutError
from rdflib import RDF, Graph, URIRef

import config
from database import create_rule as create_rule_in_db
from database import (
    find_change_requests,
    find_change_request,
    update_change_request,
    create_change_request,
    find_change_request_by_change_request_id,
    find_rules,
    find_rule,
    update_rule_in_db,
)
from models.neone_automate import ChangeRequestApproval, Rule, LO_TYPES
from models.one_record import (
    ChangeRequest,
    ApprovalStatus,
)
from oidc_token_manager import OIDCTokenManager
from services.logistics_object_service import process_change_request
from utils import (
    normalize_action_request,
)

router = APIRouter()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

oidc_token_manager: OIDCTokenManager = OIDCTokenManager(
    token_url=config.access_token_url,
    client_id=config.client_id,
    client_secret=config.client_secret,
)


@router.get("/health", tags=["health"])
def get_health(request: Request):
    if request.app.mongodb_client is not None:
        with pymongo.timeout(seconds=3):
            try:
                request.app.mongodb_client.admin.command("ping")
            except ServerSelectionTimeoutError:
                raise HTTPException(status_code=503, detail="MongoDB not available")

    return {"status": "UP"}


@router.get("/rules", tags=["rules"])
@router.get(
    "/rules",
    tags=["rules"],
    summary="Get all Rules",
    response_model=List[Rule],
    response_model_exclude_none=True,
)
def get_rules(request: Request) -> List[Rule]:
    return find_rules(request.app.database)


@router.get("/rules/{id}", tags=["rules"])
def get_rule(request: Request, id: str):
    rule = find_rule(request.app.database, id)
    return rule


@router.post("/rules", tags=["rules"])
def create_rule(request: Request, rule: Rule):
    rule = create_rule_in_db(request.app.database, rule)
    return rule


@router.put("/rules/{id}", tags=["rules"])
def update_rule(request: Request, id: str, rule: Rule):
    update_rule_in_db(request.app.database, id, rule)


@router.get("/dashboard", tags=["dashboard"])
def get_dashboard_data():
    return {
        "pending_requests": 3,
        "pending_change_requests": 21,
        "automated_requests_per_second": 14,
        "average_approval_time_in_seconds": 3,
        "share_of_automated_requests": 0.8,
    }


def patch_1R_change_request(change_request_id: str, approval_status: ApprovalStatus):
    if approval_status == ApprovalStatus.ACCEPTED:
        status = "REQUEST_ACCEPTED"
    elif (
        approval_status == ApprovalStatus.REJECTED
        or approval_status == ApprovalStatus.AUTO_REJECTED
    ):
        status = "REQUEST_REJECTED"
    url = f"{change_request_id}?status={status}"
    response = requests.patch(url, timeout=10)
    return response


def reject_other_change_requests(database, change_request: ChangeRequest, id: str):
    change = change_request.change
    lo_id = change.logistics_object.id
    revision = change.revision
    filters = {
        "_id": {"$ne": id},
        "change.logistics_object.id": lo_id,
        "change.revision": revision,
    }

    other_change_requests = find_change_requests(database, filters=filters)
    for other_change_request in other_change_requests:
        patch_and_update_change_request(
            database, other_change_request, ApprovalStatus.REJECTED
        )


def patch_and_update_change_request(
    database, change_request: ChangeRequest, approval_status: ApprovalStatus
):
    # response = patch_1R_change_request(change_request.change_request_id, approval_status)
    # response.raise_for_status()

    updated_change_request = update_change_request(
        database,
        change_request.id,
        {"approval_status": approval_status},
        return_document=True,
    )
    return update_change_request


@router.post("/change-requests/{id}/approve", tags=["change-requests"], status_code=204)
def approve_change_request(
    request: Request, id: str, change_request_approval: ChangeRequestApproval
):
    database = request.app.database
    approval_status = change_request_approval.approval_status
    if (change_request := find_change_request(database, id)) is None:
        raise HTTPException(status_code=404, detail=f"ChangeRequest {id} not found")

    if approval_status == ApprovalStatus.PENDING:  # TODO Required / useful?
        update_change_request(database, id, {"approval_status": approval_status})
        return

    # Else approval_status is ACCEPTED or REJECTED
    patch_and_update_change_request(database, change_request, approval_status)

    reject_other_change_requests(database, change_request, id)

    # TODO What should happen with comments?
    # What should happen with the change request object, Fetch object again (hasRequestStatus etc is not up-to-date)?


@router.get(
    "/change-requests",
    tags=["change-requests"],
    summary="Get all ChangeRequests",
    response_model=List[ChangeRequest],
    response_model_exclude_none=True,
)
# def get_change_requests(request: Request, start_date: date = None, end_date: date = None, historical: bool=False):
def get_change_requests(
    request: Request,
    from_date: Optional[date] = None,
    to_date: Optional[date] = None,
    historical: Optional[bool] = False,
    states: List[ApprovalStatus] = Query(default=[]),
    LO_types: List[LO_TYPES] = Query(default=[]),
    requestor: Optional[str] = None,
    skip: Optional[int] = None,
    limit: Optional[int] = None,
):
    if from_date is not None:
        datetime_from_date = datetime.combine(from_date, datetime.min.time())
    else:
        datetime_from_date = None
    if to_date is not None:
        datetime_to_date = datetime.combine(to_date, datetime.max.time())
    else:
        datetime_to_date = None
    change_requests = find_change_requests(
        database=request.app.database,
        from_date=datetime_from_date,
        to_date=datetime_to_date,
        historical=historical,
        states=states,
        lo_types=LO_types,
        requestor=requestor,
        skip=skip,
        limit=limit,
        filters={},
    )
    print(len(list(change_requests)))
    return change_requests


@router.get(
    "/change-requests/{id}",
    tags=["change-requests"],
    summary="Get ChangeRequest details",
)
def get_change_request(request: Request, id: str):
    if (change_request := find_change_request(request.app.database, id)) is not None:
        return change_request
    raise HTTPException(status_code=404, detail=f"ChangeRequest {id} not found")


def is_change_request(action_request: dict) -> bool:
    # only consider action requests of type ChangeRequest
    # check if graph contains triple with rdf:type and object https://onerecord.iata.org/ns/api#ChangeRequest
    g = Graph().parse(data=action_request, format="json-ld")
    type_uri = RDF.type
    change_request_uri = URIRef("https://onerecord.iata.org/ns/api#ChangeRequest")

    result = False
    for s, p, o in g.triples((None, type_uri, change_request_uri)):
        result = True
        break

    return result


def send_action_request_response_to_one_record_server(
    change_request: ChangeRequest, action_request_status: str
):
    url = f"{change_request.id}?status={action_request_status}"
    requests.post(url, timeout=10)

    # TODO error handling, also pending?


@router.post(
    "/evaluation/actionrequest",
    tags=["ne-one-server-integration"],
    summary="Receive ActionRequest for evaluation from ne-one server",
)
async def receive_action_request(request: Request):
    logger.info("Received ActionRequest evaluation request from ne-one server")
    action_request = await request.json()

    if not is_change_request(action_request):
        logger.info("Received ActionRequest is not a ChangeRequest, ignoring")
        return {"actionRequestStatus": "REQUEST_PENDING"}
    resolved_change_request = normalize_action_request(action_request)

    change_request = ChangeRequest(**resolved_change_request)
    logger.info("Process ChangeRequest: {}".format(change_request.change_request_id))

    if existing_change_request := find_change_request_by_change_request_id(
        request.app.database, change_request.change_request_id
    ):
        logger.info("Already in database")
        if (
            existing_change_request.approval_status == ApprovalStatus.AUTO_ACCEPTED
            or existing_change_request.approval_status == ApprovalStatus.ACCEPTED
        ):
            return {"actionRequestStatus": "REQUEST_ACCEPTED"}
        elif (
            existing_change_request.approval_status == ApprovalStatus.AUTO_REJECTED
            or existing_change_request.approval_status == ApprovalStatus.REJECTED
        ):
            return {"actionRequestStatus": "REQUEST_REJECTED"}
        else:
            return {"actionRequestStatus": "REQUEST_PENDING"}

    change_request = process_change_request(
        change_request, find_rules(request.app.database)
    )
    logger.info("Store ChangeRequest in database")

    create_change_request(request.app.database, change_request)

    if change_request.approval_status == ApprovalStatus.AUTO_ACCEPTED:
        return {"actionRequestStatus": "REQUEST_ACCEPTED"}
    elif change_request.approval_status == ApprovalStatus.AUTO_REJECTED:
        return {"actionRequestStatus": "REQUEST_REJECTED"}

    return {"actionRequestStatus": "REQUEST_PENDING"}
