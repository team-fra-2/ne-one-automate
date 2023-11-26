from models.one_record import LogisticsObject

a = {
    "@id": "http://localhost:8080/logistics-objects/waybill-1",
    "@type": "https://onerecord.iata.org/ns/cargo#Waybill",
    "https://onerecord.iata.org/ns/cargo#arrivalLocation": {
        "@id": "http://localhost:8080/logistics-objects/MIL"
    },
    "https://onerecord.iata.org/ns/cargo#departureLocation": {
        "@id": "http://localhost:8080/logistics-objects/FRA"
    },
    "https://onerecord.iata.org/ns/cargo#shipment": {
        "@id": "http://localhost:8080/logistics-objects/shipment-1"
    },
    "https://onerecord.iata.org/ns/cargo#waybillNumber": "12345675",
    "https://onerecord.iata.org/ns/cargo#waybillPrefix": "020",
    "https://onerecord.iata.org/ns/cargo#waybillType": {
        "@id": "https://onerecord.iata.org/ns/cargo#MASTER"
    },
}


def test_serialize_one_record():
    """Test serialization of a One Record object."""
    b = LogisticsObject(**a)
    assert b.id == "http://localhost:8080/logistics-objects/waybill-1"


def test_serialize_logistics_object():
    c = {
        "@id": "http://localhost:8080/logistics-objects/waybill-1",
        "@type": "https://onerecord.iata.org/ns/cargo#Waybill",
        "https://onerecord.iata.org/ns/cargo#arrivalLocation": [
            {"@id": "http://localhost:8080/logistics-objects/MIL"},
            {
                "@type": "https://onerecord.iata.org/ns/cargo#Location",
                "@value": "http://localhost:8080/logistics-objects/MXP",
            },
        ],
        "https://onerecord.iata.org/ns/cargo#departureLocation": {
            "@id": "http://localhost:8080/logistics-objects/FRA"
        },
    }
    d = LogisticsObject(**c)
