"""
This module contains function to interact with the MongoDB database backend
"""
import base64
import logging
from datetime import datetime

import pymongo
from pymongo.collection import ReturnDocument

from models.neone_automate import LO_TYPES, Rule
from models.one_record import ApprovalStatus
from rule_engine.rules import *

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

RULE_COLLECTION_NAME: str = "rules"
CHANGE_REQUEST_COLLECTION_NAME: str = "changerequests"
COUNTER_COLLECTION_NAME: str = "counters"


def get_next_sequence_value(database, sequence_name):
    """
    Retrieve the next sequence value from a specified collection.
    """
    sequence_doc = database[COUNTER_COLLECTION_NAME].find_one_and_update(
        {"_id": sequence_name},
        {"$inc": {"sequence_value": 1}},
        upsert=True,
        return_document=True,
    )
    return sequence_doc["sequence_value"]


def find_change_request_by_change_request_id(
    database, uri: str
) -> Optional[ChangeRequest]:
    """
    Find a change request by uri
    """
    document = database[CHANGE_REQUEST_COLLECTION_NAME].find_one(
        {"change_request_id": uri}
    )
    if not document:
        return None
    return ChangeRequest(**document)


def find_change_request(database, id: str) -> Optional[ChangeRequest]:
    """
    Find a change request by id
    """
    document = database[CHANGE_REQUEST_COLLECTION_NAME].find_one({"_id": id})
    if not document:
        return None
    return ChangeRequest(**document)


def change_request_exists(database, id: str) -> bool:
    """
    Check whether a change request exists by id
    """
    return bool(
        database[CHANGE_REQUEST_COLLECTION_NAME].count_documents({"_id": id}, limit=1)
    )


def update_change_request(
    database, id: str, new_values: dict, return_document: bool = False
) -> Optional[ChangeRequest]:
    """
    Update a change request by id
    """
    filter = {"_id": id}
    update = {"$set": new_values}
    if return_document:
        document = database[CHANGE_REQUEST_COLLECTION_NAME].find_one_and_update(
            filter, update, upsert=False, return_document=ReturnDocument.AFTER
        )
        return ChangeRequest(**document)
    else:
        database[CHANGE_REQUEST_COLLECTION_NAME].update_one(
            filter, update, upsert=False
        )


def find_rules(database) -> List[Rule]:
    """
    Get all rules
    """
    cursor = database[RULE_COLLECTION_NAME].find({})

    return [Rule(**document) for document in cursor]


def find_rule(database, id: str) -> Optional[Rule]:
    """
    Find a rule by id
    """
    document = database[RULE_COLLECTION_NAME].find_one({"_id": id})
    if not document:
        return None
    return Rule(**document)


def update_rule_in_db(database, id: str, rule: Rule):
    """
    Update a change request by id
    """
    filter = {"_id": id}
    document = rule.model_dump(exclude_none=False)
    document["_id"] = id
    database[RULE_COLLECTION_NAME].replace_one(filter, document, upsert=False)


def find_change_requests(
    database,
    from_date: Optional[datetime] = None,
    to_date: Optional[datetime] = None,
    historical: bool = False,
    states: List[ApprovalStatus] = [],
    lo_types: List[LO_TYPES] = [],
    requestor: Optional[str] = None,
    skip: Optional[int] = 0,
    limit: Optional[int] = 10,
    #  AWB: Optional[str] = None,
    filters: dict = {},
) -> List[ChangeRequest]:
    """
    Get all change requests that match the given filters
    """

    if from_date is not None:
        if "requested_at" not in filters:
            filters["requested_at"] = {}
        filters["requested_at"]["$gte"] = from_date

    if to_date is not None:
        if "requested_at" not in filters:
            filters["requested_at"] = {}
        filters["requested_at"]["$lte"] = to_date

    if states and len(states) > 0:
        filters["approval_status"] = {"$in": states}

    if lo_types:
        filters["change.logisticsObject.@type"] = {"$in": lo_types}

    if requestor is not None:
        filters["requested_by"] = requestor

    cursor = (
        database[CHANGE_REQUEST_COLLECTION_NAME]
        .find(filters)
        .sort("requested_at", pymongo.DESCENDING)
    )

    if skip is not None:
        cursor = cursor.skip(skip)

    if limit is not None:
        cursor = cursor.limit(limit)

    return [ChangeRequest(**document) for document in cursor]


def create_change_request(database, change_request: ChangeRequest):
    """
    Create a change request into the database
    """
    next_sequence_value = get_next_sequence_value(database, "change_request_id")
    unique_id = f"CR-{next_sequence_value}"

    document = change_request.model_dump(exclude_none=True)
    document["_id"] = unique_id

    result = database[CHANGE_REQUEST_COLLECTION_NAME].insert_one(document)
    assert result.acknowledged


def only_id_suffix(id):
    return id.split("/")[
        -1
    ]  # remove http://localhost:8080/action-requests/ => only {id}


def create_rule(database, rule: Rule, init: bool = False) -> Rule:
    """
    Insert a rule into the database
    """
    next_sequence_value = get_next_sequence_value(database, "rule_id")
    unique_id = f"{next_sequence_value}"

    if init:
        rule.rule_id = f"rule-{next_sequence_value}"

    document = rule.model_dump(exclude_none=False)
    document["_id"] = unique_id

    result = database[RULE_COLLECTION_NAME].insert_one(document)
    assert result.acknowledged
    return find_rule(database, unique_id)


def reset_database(database):
    logger.warning("Database will be reset")
    database.drop_collection(RULE_COLLECTION_NAME)
    database.drop_collection(CHANGE_REQUEST_COLLECTION_NAME)
    database.drop_collection(COUNTER_COLLECTION_NAME)


def init_database(database, reset: bool = False):
    if reset:
        reset_database(database)
    if not database[COUNTER_COLLECTION_NAME].find_one({"_id": "change_request_id"}):
        logger.info("Init change_request_id counter")
        database[COUNTER_COLLECTION_NAME].insert_one(
            {"_id": "change_request_id", "sequence_value": 100}
        )
    if not database[COUNTER_COLLECTION_NAME].find_one({"_id": "rule_id"}):
        logger.info("Init change_request_id counter")
        database[COUNTER_COLLECTION_NAME].insert_one(
            {"_id": "rule_id", "sequence_value": 0}
        )
    if not database[RULE_COLLECTION_NAME].find_one({}):
        logger.info("Init rules")
        # create rules
        for i in list(range(1, 8)):
            rule_str_repr = get_func_str_repr(eval(f"rule_{i}"))

            rule: Rule = Rule(
                rule_id=f"rule-x",
                description=rule_str_repr.split('"""', 3)[1].strip(),
                workspace_xml="PHhtbCB4bWxucz0iaHR0cHM6Ly9kZXZlbG9wZXJzLmdvb2dsZS5jb20vYmxvY2tseS94bWwiPjxibG9jayB0eXBlPSJjb250cm9sc19pZiIgaWQ9IihYJFA/YyNvfEZqfGNaVCEpXTdaIiB4PSItMTAiIHk9IjEzMCI+PHZhbHVlIG5hbWU9IklGMCI+PGJsb2NrIHR5cGU9ImxvZ2ljX29wZXJhdGlvbiIgaWQ9InpeUU1maHFdaG4uLFl+eVI4T0VIIj48ZmllbGQgbmFtZT0iT1AiPkFORDwvZmllbGQ+PHZhbHVlIG5hbWU9IkEiPjxibG9jayB0eXBlPSJsb2dpY19jb21wYXJlIiBpZD0iUy5YXks3KmpRNnBWfmwpJT9RYWUiPjxmaWVsZCBuYW1lPSJPUCI+TkVRPC9maWVsZD48dmFsdWUgbmFtZT0iQSI+PGJsb2NrIHR5cGU9ImdldF93ZWlnaHQiIGlkPSJVemNqVGU1T0ZOT3Ngc3xYYDJ2LyI+PHZhbHVlIG5hbWU9IkxPR0lTVElDU19PQkpFQ1QiPjxibG9jayB0eXBlPSJnZXRfb3JpZ2luYWxfbG9naXN0aWNzX29iamVjdCIgaWQ9Ii47YWovblNCNFU4IUpMVktHYFV8Ii8+PC92YWx1ZT48L2Jsb2NrPjwvdmFsdWU+PHZhbHVlIG5hbWU9IkIiPjxibG9jayB0eXBlPSJnZXRfd2VpZ2h0IiBpZD0iOnRxKSxURy1eWEFzdktMUHI7YV0iPjx2YWx1ZSBuYW1lPSJMT0dJU1RJQ1NfT0JKRUNUIj48YmxvY2sgdHlwZT0iZ2V0X3VwZGF0ZWRfbG9naXN0aWNzX29iamVjdCIgaWQ9IjF4Xn4kcnx7ZylQIT16T3Y5c0c0Ii8+PC92YWx1ZT48L2Jsb2NrPjwvdmFsdWU+PC9ibG9jaz48L3ZhbHVlPjx2YWx1ZSBuYW1lPSJCIj48YmxvY2sgdHlwZT0ibG9naWNfY29tcGFyZSIgaWQ9Im5bLih1dGcqOWBHTkl6JVBXcltAIj48ZmllbGQgbmFtZT0iT1AiPkxUPC9maWVsZD48dmFsdWUgbmFtZT0iQSI+PGJsb2NrIHR5cGU9Im1hdGhfc2luZ2xlIiBpZD0iP0ltUUJYcyFDZ2lxd3RZQX1vbUgiPjxmaWVsZCBuYW1lPSJPUCI+QUJTPC9maWVsZD48dmFsdWUgbmFtZT0iTlVNIj48c2hhZG93IHR5cGU9Im1hdGhfbnVtYmVyIiBpZD0iY0s5RSVpb3IjI1JLfSFFKl9fd2QiPjxmaWVsZCBuYW1lPSJOVU0iPjk8L2ZpZWxkPjwvc2hhZG93PjxibG9jayB0eXBlPSJtYXRoX2FyaXRobWV0aWMiIGlkPSI9VUt8Rls7LnthTVczUiN2dz15USI+PGZpZWxkIG5hbWU9Ik9QIj5NSU5VUzwvZmllbGQ+PHZhbHVlIG5hbWU9IkEiPjxzaGFkb3cgdHlwZT0ibWF0aF9udW1iZXIiIGlkPSJjcyhveiRUNClQbF1fMVJucj1pTiI+PGZpZWxkIG5hbWU9Ik5VTSI+MTwvZmllbGQ+PC9zaGFkb3c+PGJsb2NrIHR5cGU9ImdldF93ZWlnaHQiIGlkPSJkcE4hYytjfVB5MVl1dTIveFd5VSI+PHZhbHVlIG5hbWU9IkxPR0lTVElDU19PQkpFQ1QiPjxibG9jayB0eXBlPSJnZXRfb3JpZ2luYWxfbG9naXN0aWNzX29iamVjdCIgaWQ9InMoKltHQG1FeGJXYiwra3YqWTRCIi8+PC92YWx1ZT48L2Jsb2NrPjwvdmFsdWU+PHZhbHVlIG5hbWU9IkIiPjxzaGFkb3cgdHlwZT0ibWF0aF9udW1iZXIiIGlkPSJ9WUo/Y1F8ezFnKUgkNktwU3YqZyI+PGZpZWxkIG5hbWU9Ik5VTSI+MTwvZmllbGQ+PC9zaGFkb3c+PGJsb2NrIHR5cGU9Im1hdGhfc2luZ2xlIiBpZD0iRG86JEUhN1NvV3duLzB0LjluamsiPjxmaWVsZCBuYW1lPSJPUCI+QUJTPC9maWVsZD48dmFsdWUgbmFtZT0iTlVNIj48c2hhZG93IHR5cGU9Im1hdGhfbnVtYmVyIiBpZD0iP21VXXspQF87c1ZhTWNEdkYlQDciPjxmaWVsZCBuYW1lPSJOVU0iPjk8L2ZpZWxkPjwvc2hhZG93PjxibG9jayB0eXBlPSJnZXRfd2VpZ2h0IiBpZD0iVVoyZkEsYURKW2IodyErVyheRzgiPjx2YWx1ZSBuYW1lPSJMT0dJU1RJQ1NfT0JKRUNUIj48YmxvY2sgdHlwZT0iZ2V0X3VwZGF0ZWRfbG9naXN0aWNzX29iamVjdCIgaWQ9IkAlP1BjKWRfWU1bUWRseG51XV9NIi8+PC92YWx1ZT48L2Jsb2NrPjwvdmFsdWU+PC9ibG9jaz48L3ZhbHVlPjwvYmxvY2s+PC92YWx1ZT48L2Jsb2NrPjwvdmFsdWU+PHZhbHVlIG5hbWU9IkIiPjxibG9jayB0eXBlPSJtYXRoX251bWJlciIgaWQ9Iko9ZmcyfFhpW0VSVyp+aU4hZjplIj48ZmllbGQgbmFtZT0iTlVNIj4xPC9maWVsZD48L2Jsb2NrPjwvdmFsdWU+PC9ibG9jaz48L3ZhbHVlPjwvYmxvY2s+PC92YWx1ZT48c3RhdGVtZW50IG5hbWU9IkRPMCI+PGJsb2NrIHR5cGU9ImRlY2lzaW9uX2FjY2VwdGVkIiBpZD0iOCR4d15oOG9ESDUhT05zbW5WUDoiLz48L3N0YXRlbWVudD48L2Jsb2NrPjwveG1sPg==",
                function_code=base64.b64encode(rule_str_repr.encode("utf-8")),
            )
            if i == 7:
                rule.workspace_xml = "PHhtbCB4bWxucz0iaHR0cHM6Ly9kZXZlbG9wZXJzLmdvb2dsZS5jb20vYmxvY2tseS94bWwiPjxibG9jayB0eXBlPSJjb250cm9sc19pZiIgaWQ9IihYJFA/YyNvfEZqfGNaVCEpXTdaIiB4PSIxMCIgeT0iMzMwIj48dmFsdWUgbmFtZT0iSUYwIj48YmxvY2sgdHlwZT0iaXNfdHlwb19jb3JyZWN0aW9uIiBpZD0iNmlkXTkpYlNAJEYzKEpILm5Ob28iPjx2YWx1ZSBuYW1lPSJPUklHSU5BTF9TVFJJTkciPjxibG9jayB0eXBlPSJnZXRfZ29vZHNfZGVzY3JpcHRpb24iIGlkPSJASG9Zd149fWdmJEFWfW1FbXYsXSI+PHZhbHVlIG5hbWU9IkxPR0lTVElDU19PQkpFQ1QiPjxibG9jayB0eXBlPSJnZXRfb3JpZ2luYWxfbG9naXN0aWNzX29iamVjdCIgaWQ9Ii5yLytyLWNvejlIVl1bNG9aP3JoIi8+PC92YWx1ZT48L2Jsb2NrPjwvdmFsdWU+PHZhbHVlIG5hbWU9IlVQREFURURfU1RSSU5HIj48YmxvY2sgdHlwZT0iZ2V0X2dvb2RzX2Rlc2NyaXB0aW9uIiBpZD0iM3NkNS9EKiMlNCFyOVhGZ3RCSlAiPjx2YWx1ZSBuYW1lPSJMT0dJU1RJQ1NfT0JKRUNUIj48YmxvY2sgdHlwZT0iZ2V0X3VwZGF0ZWRfbG9naXN0aWNzX29iamVjdCIgaWQ9InZUP1p+YT1ocUsoMVpyLSkwVkRJIi8+PC92YWx1ZT48L2Jsb2NrPjwvdmFsdWU+PC9ibG9jaz48L3ZhbHVlPjxzdGF0ZW1lbnQgbmFtZT0iRE8wIj48YmxvY2sgdHlwZT0iZGVjaXNpb25fYWNjZXB0ZWQiIGlkPSI4JHh3Xmg4b0RINSFPTnNtblZQOiIvPjwvc3RhdGVtZW50PjwvYmxvY2s+PC94bWw+"
            create_rule(database, rule, init=True)
    if not database[CHANGE_REQUEST_COLLECTION_NAME].find_one({}):
        logger.info("Init change requests")
        # change_request1: ChangeRequest = ChangeRequest()

    # create change-requests
    # one pending
    # one accepted
    # one rejected
