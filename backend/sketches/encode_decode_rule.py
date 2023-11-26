rule: str = """
def rule_1(change_request: ChangeRequest) -> Optional[Recommendation]:
    \"""
    LogisticsObjectType is Waybill AND arrival airport in waybill changed AND airports are in same city
    \"""
    if (
        change_request.original_logistics_object.type
        == "https://onerecord.iata.org/ns/cargo#Waybill"
        and change_request.original_logistics_object.arrivalLocation.locationCodes[
            0
        ].code
        != change_request.updated_logistics_object.arrivalLocation.locationCodes[0].code
        and same_airport_city(
            change_request.original_logistics_object.arrivalLocation.locationCodes[
                0
            ].code,
            change_request.updated_logistics_object.arrivalLocation.locationCodes[
                0
            ].code,
        )
    ):
        return Recommendation(
            rule_id="rule_1",
            decision=Decision.ACCEPTED,
            comment="Airports are in same city",
        )
    return None
"""
# base64 encode rule
import base64

rule_encoded: str = base64.b64encode(rule.encode("utf-8"))
rule_decoded: str = rule_encoded.decode("utf-8")


def load_rule(encoded_function):
    decoded_function = base64.b64decode(encoded_function).decode("utf-8")
    exec(decoded_function, globals())
    return globals()[get_rule_name(decoded_function)]


# Helper function to extract the function name
def get_rule_name(func_code):
    lines = func_code.splitlines()
    for line in lines:
        if line.startswith("def "):
            return line.split("def ")[1].split("(")[0]
    return None


loaded_rule = load_rule(rule_encoded)
print(loaded_rule(None))
