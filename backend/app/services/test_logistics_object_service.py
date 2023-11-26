from typing import List

from pyld import jsonld

from models.one_record import ChangeRequest, LogisticsObject, Operation, OperationDetail

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def test_apply_change_request():
    change_request_dict: dict = {}
    change_request: ChangeRequest = ChangeRequest(**change_request_dict)
    pass

LOGISTICS_OBJECT_BASE_URL = "https://localhost:8080/logistics-objects"

security_declaration = LogisticsObject(**{
    "@id": f"{LOGISTICS_OBJECT_BASE_URL}/security-declaration-1",
    "@type": "SecurityDeclaration",
    "https://onerecord.iata.org/ns/cargo#issuedForPiece": {
        "@id": f"{LOGISTICS_OBJECT_BASE_URL}/piece-1"
    }    
})

change_request = ChangeRequest(**{
    "_id": "CR-103",
    "@id": "http://localhost:8080/action-requests/e404d623-cf49-46be-b415-1a44a4605050",
    "@type": "https://onerecord.iata.org/ns/api#ChangeRequest",
    "https://onerecord.iata.org/ns/api#hasChange": {
      "@id": "neone:90b9bbf5-a0ff-4488-8c2c-9b44af909c24",
      "@type": "https://onerecord.iata.org/ns/api#Change",
      "https://onerecord.iata.org/ns/api#hasDescription": "Updated security status to SPX after screening",
      "https://onerecord.iata.org/ns/api#hasLogisticsObject": {
        "@id": "http://localhost:8080/logistics-objects/security-declaration-1"
      },
      "https://onerecord.iata.org/ns/api#hasOperation": [
        {
          "@id": "neone:c7a640a7-b9a4-4ca6-aeb7-d7c3b577fd71",
          "https://onerecord.iata.org/ns/api#o": {
            "@id": "neone:92492198-8478-4a09-993d-ddea80eb3830",
            "https://onerecord.iata.org/ns/api#hasDatatype": "https://onerecord.iata.org/ns/coreCodeLists#SecurityStatus",
            "https://onerecord.iata.org/ns/api#hasValue": "https://onerecord.iata.org/ns/coreCodeLists#SecurityStatus_SPX"
          },
          "https://onerecord.iata.org/ns/api#op": {
            "@id": "https://onerecord.iata.org/ns/api#ADD"
          },
          "https://onerecord.iata.org/ns/api#p": "https://onerecord.iata.org/ns/cargo#securityStatus",
          "https://onerecord.iata.org/ns/api#s": "http://localhost:8080/logistics-objects/security-declaration-1"
        }
      ],
      "https://onerecord.iata.org/ns/api#hasRevision": {
        "@type": "http://www.w3.org/2001/XMLSchema#int",
        "@value": "1"
      },
      "https://onerecord.iata.org/ns/api#notifyRequestStatusChange": False
    },
    "https://onerecord.iata.org/ns/api#hasRequestStatus": {
      "@id": "https://onerecord.iata.org/ns/api#REQUEST_PENDING"
    },
    "https://onerecord.iata.org/ns/api#isRequestedAt": "2023-11-25T22:31:02.133000",
    "https://onerecord.iata.org/ns/api#isRequestedBy": {
      "@id": "http://localhost:8080/logistics-objects/_data-holder"
    },
    "originalLogisticsObject": {
      "@id": "http://localhost:8080/logistics-objects/security-declaration-1",
      "@type": "https://onerecord.iata.org/ns/cargo#SecurityDeclaration",
      "https://onerecord.iata.org/ns/cargo#issuedForPiece": {
        "@id": "http://localhost:8080/logistics-objects/piece-1"
      }
    },
    "updatedLogisticsObject": {
      "@id": "http://localhost:8080/logistics-objects/security-declaration-1",
      "@type": "https://onerecord.iata.org/ns/cargo#SecurityDeclaration",
      "https://onerecord.iata.org/ns/cargo#securityStatus": {},
      "https://onerecord.iata.org/ns/cargo#issuedForPiece": {
        "@id": "http://localhost:8080/logistics-objects/piece-1"
      }
    },
    "recommendations": [
      {
        "rule_id": "rule_3",
        "decision": "MANUAL_CHECK_REQUIRED"
      }
    ],
    "approvalStatus": "MANUAL_CHECK_REQUIRED"
  })

compacted_lo = jsonld.compact(
    security_declaration.model_dump(exclude_none=True, by_alias=True), {}
)

print("-"*20)
print("compacted_lo")
print(compacted_lo)

normalized_lo = jsonld.normalize(
    compacted_lo, {"algorithm": "URDNA2015", "format": "application/nquads"}
)

print("-"*20)
print("normalized_lo")
print(normalized_lo)

# assert normalized_lo == """<https://localhost:8080/logistics-objects/security-declaration-1> <https://onerecord.iata.org/ns/cargo#issuedForPiece> <https://localhost:8080/logistics-objects/piece-1> ."""

back_converted = jsonld.from_rdf(
    normalized_lo,
    options={"format": "application/nquads", "useNativeTypes": True},
)

print("-"*20)
print("back_converted")
print(back_converted)

change = change_request.change
operations: List[Operation] = change.operations

new_normalized_lo = normalized_lo

# def update_recursively(s, p, value, datatype, op):
#     if value.startswith(("http", "neone")):
#         s[p] = update_recursively(s[p], )

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

print(operations)

for operation in operations:
    s = operation.s
    p = operation.p
    o: OperationDetail = operation.o
    value = o.value
    datatype = o.datatype
    op = operation.op.id

    print("op")
    print(op)
    print("*"*20)

    print("s")
    print(s)
    print("*"*20)

    print("p")
    print(p)
    print("*"*20)

    print("value")
    print(value)
    print("*"*20)

    print("datatype")
    print(datatype)
    print("*"*20)

    compacted_lo = update_recursively(compacted_lo, s, p, value, datatype, op)
    print(compacted_lo)