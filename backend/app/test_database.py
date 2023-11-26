import datetime

from models.one_record import ChangeRequest


def test_populate_change_request():
    document = {
        "_id": "0494a4ff-ac91-44be-be0c-992fe8749176",
        "@id": "http://localhost:8080/action-requests/0494a4ff-ac91-44be-be0c-992fe8749176",
        "type": "https://onerecord.iata.org/ns/api#ChangeRequest",
        "change": {
            "id": "neone:3ce38f36-a190-42b9-ae75-54b806929459",
            "type": "https://onerecord.iata.org/ns/api#Change",
            "description": "asd",
            "logistics_object": {
                "id": "http://localhost:8080/logistics-objects/af680c8d-acf2-4490-b7d8-71071f4b2f3a"
            },
            "operations": [
                {
                    "id": "neone:7796ea92-e22c-45c7-a828-5c396950af7d",
                    "o": {
                        "id": "neone:efa75718-103c-4d6a-b97a-54c15023c4ac",
                        "datatype": "http://www.w3.org/2001/XMLSchema#string",
                        "value": "ONE Record Advertisement Materials2",
                    },
                    "op": {"id": "https://onerecord.iata.org/ns/api#ADD"},
                    "p": "https://onerecord.iata.org/ns/cargo#goodsDescription",
                    "s": "http://localhost:8080/logistics-objects/af680c8d-acf2-4490-b7d8-71071f4b2f3a",
                }
            ],
            "revision": 1,
            "notify_request_status_change": False,
        },
        "request_status": {"id": "https://onerecord.iata.org/ns/api#REQUEST_PENDING"},
        "requested_at": datetime.datetime(2023, 11, 20, 14, 42, 27, 788000),
        "requested_by": {"id": "http://localhost:8080/logistics-objects/_data-holder"},
        "original_logistics_object": {
            "id": "http://localhost:8080/logistics-objects/af680c8d-acf2-4490-b7d8-71071f4b2f3a",
            "type": "https://onerecord.iata.org/ns/cargo#Piece",
            "coload": False,
        },
        "updated_logistics_object": {
            "id": "http://localhost:8080/logistics-objects/af680c8d-acf2-4490-b7d8-71071f4b2f3a",
            "goods_description": "ONE Record Advertisement Materials2",
        },
        "recommendations": [],
        "approval_status": "PENDING",
    }

    change_request: ChangeRequest = ChangeRequest(**document)

    assert (
        change_request.change_request_id
        == "http://localhost:8080/action-requests/0494a4ff-ac91-44be-be0c-992fe8749176"
    )
