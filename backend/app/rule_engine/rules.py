import inspect
from typing import List

from models.one_record import Recommendation, Decision
from rule_engine.functions import *


def rule_1(change_request: ChangeRequest) -> Optional[Recommendation]:
    """
    LogisticsObjectType is Waybill AND arrival airport in waybill changed AND airports are in same city
    """
    if (
        change_request.original_logistics_object.type
        == "https://onerecord.iata.org/ns/cargo#Waybill"
        and change_request.original_logistics_object.arrivalLocation.locationCodes[
            0
        ].code
        != change_request.updated_logistics_object.arrivalLocation.locationCodes[0].code
        and get_city_of_airport(
            change_request.original_logistics_object.arrivalLocation.locationCodes[
                0
            ].code
        )
        == get_city_of_airport(
            change_request.updated_logistics_object.arrivalLocation.locationCodes[
                0
            ].code
        )
    ):
        return Recommendation(
            rule_id="rule_1",
            decision=Decision.ACCEPTED,
            comment="Airports are in same city",
        )
    return None


def rule_2(change_request: ChangeRequest) -> Optional[Recommendation]:
    """
    GoodsDescription in Shipment is changed
    """
    if (
        change_request.original_logistics_object.type
        == "https://onerecord.iata.org/ns/cargo#Shipment"
        and change_request.original_logistics_object.goods_description
        != change_request.updated_logistics_object.goods_description
    ):
        return Recommendation(rule_id="rule_2", decision=Decision.MANUAL_CHECK_REQUIRED)
    return None


def rule_3(change_request: ChangeRequest) -> Optional[Recommendation]:
    """
    Piece gross weight is changed by less than 1kg
    """
    if (
        change_request.original_logistics_object.type
        == "https://onerecord.iata.org/ns/cargo#Piece"
        and (
            change_request.original_logistics_object.gross_weight.numerical_value
            != change_request.updated_logistics_object.gross_weight.numerical_value
            and (
                abs(
                    change_request.original_logistics_object.gross_weight.numerical_value
                    - change_request.updated_logistics_object.gross_weight.numerical_value
                )
                < 1
                or abs(
                    change_request.original_logistics_object.gross_weight.numerical_value
                    / change_request.updated_logistics_object.gross_weight.numerical_value
                )
                < 0.05
            )
        )
    ):
        return Recommendation(rule_id="rule_3", decision=Decision.ACCEPTED)
    else:
        return Recommendation(rule_id="rule_3", decision=Decision.MANUAL_CHECK_REQUIRED)
    return None


def rule_4(change_request: ChangeRequest) -> Optional[Recommendation]:
    """
    CarrierProduct in BookingOptionRequest is changed
    """
    if (
        change_request.original_logistics_object.type
        == "https://onerecord.iata.org/ns/cargo#BookingOptionRequest"
        and change_request.original_logistics_object.carrierProduct
        != change_request.updated_logistics_object.carrierProduct
    ):
        return Recommendation(rule_id="rule_4", decision=Decision.MANUAL_CHECK_REQUIRED)
    return None


def rule_5(change_request: ChangeRequest) -> Optional[Recommendation]:
    """
    SecurityStatus in SecurityDeclaration is changed from not SPX to SPX
    """
    if (
        change_request.original_logistics_object.type
        == "https://onerecord.iata.org/ns/cargo#SecurityDeclaration"
        and change_request.original_logistics_object.securityStatus.code != "SPX"
        and change_request.updated_logistics_object.securityStatus.code == "SPX"
    ):
        return Recommendation(rule_id="rule_5", decision=Decision.ACCEPTED)
    return None


def rule_6(change_request: ChangeRequest) -> Optional[Recommendation]:
    """
    Auto-Accept ChangeRequest from TrustedParty
    """
    if change_request.requested_by.id == "https://onerecord.iata.org/ids/TrustedParty":
        return Recommendation(rule_id="rule_6", decision=Decision.ACCEPTED)
    return None


def rule_7(change_request: ChangeRequest) -> Optional[Recommendation]:
    """
    ChangeRequest is typo correction in goods description
    """

    if is_typo_correction(
        (get_goods_description((get_original_logistics_object(change_request)))),
        (get_goods_description((get_updated_logistics_object(change_request)))),
    ):
        return Recommendation(rule_id="rule_7", decision=Decision.ACCEPTED)


def apply_rules(change_request: ChangeRequest) -> List[Recommendation]:
    recommendations = []
    for rule in [rule_1, rule_2, rule_3, rule_4, rule_5, rule_6]:
        recommendation = rule(change_request)
        if recommendation is not None:
            recommendations.append(recommendation)
    return recommendations


def get_func_str_repr(func_name):
    func_str = inspect.getsource(func_name)
    return func_str
