from models.one_record import ChangeRequest, LogisticsObject


def change_request_piece_updated_goods_description() -> ChangeRequest:
    input = {
        "@id": "http://localhost:8080/action-requests/803307c4-b251-4403-a1c3-b981d1a70919",
        "@type": "https://onerecord.iata.org/ns/api#ChangeRequest",
        "https://onerecord.iata.org/ns/api#hasChange": {
            "@id": "neone:856f45ed-315f-4168-b12d-2490c2a6eb73",
            "@type": "https://onerecord.iata.org/ns/api#Change",
            "https://onerecord.iata.org/ns/api#hasDescription": "Update goods description and coload",
            "https://onerecord.iata.org/ns/api#hasLogisticsObject": {
                "@id": "http://localhost:8080/logistics-objects/a3e84659-b4b7-4738-9960-fe221836127a"
            },
            "https://onerecord.iata.org/ns/api#hasOperation": {
                "@id": "neone:7ee79e23-22b9-4928-a736-2aee75584bf9",
                "https://onerecord.iata.org/ns/api#o": {
                    "@id": "neone:17960ab0-e9d8-4d91-9e0e-3e2ffa4c16a2",
                    "https://onerecord.iata.org/ns/api#hasDatatype": "http://www.w3.org/2001/XMLSchema#string",
                    "https://onerecord.iata.org/ns/api#hasValue": "ONE Record Advertisement Materials",
                },
                "https://onerecord.iata.org/ns/api#op": {
                    "@id": "https://onerecord.iata.org/ns/api#ADD"
                },
                "https://onerecord.iata.org/ns/api#p": "https://onerecord.iata.org/ns/cargo#goodsDescription",
                "https://onerecord.iata.org/ns/api#s": "http://localhost:8080/logistics-objects/a3e84659-b4b7-4738-9960-fe221836127a",
            },
            "https://onerecord.iata.org/ns/api#hasRevision": {
                "@type": "http://www.w3.org/2001/XMLSchema#int",
                "@value": "1",
            },
            "https://onerecord.iata.org/ns/api#notifyRequestStatusChange": False,
        },
        "https://onerecord.iata.org/ns/api#hasRequestStatus": {
            "@id": "https://onerecord.iata.org/ns/api#REQUEST_PENDING"
        },
        "https://onerecord.iata.org/ns/api#isRequestedAt": {
            "@type": "http://www.w3.org/2001/XMLSchema#dateTime",
            "@value": "2023-11-19T17:47:17.989000+00:00",
        },
        "https://onerecord.iata.org/ns/api#isRequestedBy": {
            "@id": "http://localhost:8080/logistics-objects/_data-holder"
        },
    }

    change_request = ChangeRequest(**input)
    change_request.original_logistics_object = LogisticsObject(
        **{
            "@id": "http://localhost:8080/logistics-objects/a3e84659-b4b7-4738-9960-fe221836127a",
            "@type": "https://onerecord.iata.org/ns/cargo#Piece",
            "https://onerecord.iata.org/ns/cargo#grossWeight": {
                "@id": "neone:2fcb744d-ccea-4102-b52d-edff818ba198",
                "@type": "https://onerecord.iata.org/ns/cargo#Value",
                "https://onerecord.iata.org/ns/cargo#numericalValue": 100.0,
                "https://onerecord.iata.org/ns/cargo#unit": {
                    "@id": "https://onerecord.iata.org/ns/coreCodeLists#MeasurementUnitCode_KGM"
                },
            },
        }
    )
    change_request.updated_logistics_object = LogisticsObject(
        **{
            "@id": "http://localhost:8080/logistics-objects/a3e84659-b4b7-4738-9960-fe221836127a",
            "@type": "https://onerecord.iata.org/ns/cargo#Piece",
            "https://onerecord.iata.org/ns/cargo#goodsDescription": "ONE Record Advertisement Materials",
            "https://onerecord.iata.org/ns/cargo#grossWeight": {
                "@id": "neone:2fcb744d-ccea-4102-b52d-edff818ba198",
                "@type": "https://onerecord.iata.org/ns/cargo#Value",
                "https://onerecord.iata.org/ns/cargo#numericalValue": 100.0,
                "https://onerecord.iata.org/ns/cargo#unit": {
                    "@id": "https://onerecord.iata.org/ns/coreCodeLists#MeasurementUnitCode_KGM"
                },
            },
        }
    )
    return change_request


def change_request_waybill_updated_arrival_airport():
    pass
