from app.utils import normalize_logistics_object, normalize_action_request


def test_convert_action_request_to_change_request():
    action_request = {}
    normalize_action_request(action_request)
    pass


def test_normalize_logistics_object():
    logistics_object: dict = {
        "@graph": [
            {
                "@id": "http://localhost:8080/logistics-objects/a3e84659-b4b7-4738-9960-fe221836127a",
                "@type": "Piece",
                "goodsDescription": "ONE Record Advertisement Materials",
                "grossWeight": {"@id": "neone:2fcb744d-ccea-4102-b52d-edff818ba198"},
            },
            {
                "@id": "neone:2fcb744d-ccea-4102-b52d-edff818ba198",
                "@type": "Value",
                "numericalValue": {
                    "@type": "http://www.w3.org/2001/XMLSchema#double",
                    "@value": "100.0",
                },
                "unit": {
                    "@id": "https://onerecord.iata.org/ns/coreCodeLists#MeasurementUnitCode_KGM"
                },
            },
        ],
        "@context": {"@vocab": "https://onerecord.iata.org/ns/cargo#"},
    }
    normalized_logistics_object = normalize_logistics_object(logistics_object)
    assert "@id" in normalized_logistics_object
    assert "@type" in normalized_logistics_object
    assert (
        "https://onerecord.iata.org/ns/cargo#goodsDescription"
        in normalized_logistics_object
    )


def test_apply_change_request():
    original_logistics_object: dict = {
        "id": "http://localhost:8080/logistics-objects/af680c8d-acf2-4490-b7d8-71071f4b2f3a",
        "type": "https://onerecord.iata.org/ns/cargo#Piece",
    }
    pass
