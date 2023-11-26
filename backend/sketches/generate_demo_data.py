import requests
import json

client_id: str = "neone-client"
client_secret: str = "lx7ThS5aYggdsMm42BP3wMrVqKm9WpNY"
access_token_url: str = (
    "http://localhost:8989/realms/neone/protocol/openid-connect/token"
)

payload = "grant_type=client_credentials&client_id={client_id}&client_secret={client_secret}".format(
    client_id=client_id, client_secret=client_secret
)
headers = {"Content-Type": "application/x-www-form-urlencoded"}

response = requests.request("POST", access_token_url, headers=headers, data=payload)

access_token = response.json()["access_token"]

url = "http://localhost:8080/logistics-objects"

payload = json.dumps(
    {
        "@context": {"cargo": "https://onerecord.iata.org/ns/cargo#"},
        "@type": "cargo:Piece",
        "cargo:coload": False,
    }
)
headers = {
    "Content-Type": "application/ld+json",
    "Authorization": "Bearer {token}".format(token=access_token),
}

response = requests.request("POST", url, headers=headers, data=payload)
logistics_object_id = response.headers["Location"]
print(logistics_object_id)


payload = json.dumps(
    {
        "@context": {
            "cargo": "https://onerecord.iata.org/ns/cargo#",
            "api": "https://onerecord.iata.org/ns/api#",
        },
        "@type": "api:Change",
        "api:hasDescription": "asd",
        "api:hasLogisticsObject": {"@id": logistics_object_id},
        "api:hasOperation": [
            {
                "@type": "api:Operation",
                "api:op": {"@id": "api:ADD"},
                "api:s": logistics_object_id,
                "api:p": "https://onerecord.iata.org/ns/cargo#goodsDescription",
                "api:o": [
                    {
                        "@type": "api:OperationObject",
                        "api:hasDatatype": "http://www.w3.org/2001/XMLSchema#string",
                        "api:hasValue": "ONE Record Advertisement Materials2",
                    }
                ],
            }
        ],
        "api:hasRevision": {
            "@type": "http://www.w3.org/2001/XMLSchema#positiveInteger",
            "@value": "1",
        },
    }
)

response = requests.request("PATCH", logistics_object_id, headers=headers, data=payload)

print(response.headers["Location"])
