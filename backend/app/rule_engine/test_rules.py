from app.data.test_data import change_request_piece_updated_goods_description
from models.one_record import ChangeRequest, Recommendation
from app.rule_engine.rules import rule_1, apply_rules


def test_rule_1_not_fired():
    change_request: ChangeRequest = change_request_piece_updated_goods_description()
    recommendation: Recommendation = rule_1(change_request)
    assert recommendation is None


# def test_rule_1_fired_():
#     change_request: ChangeRequest = change_request_waybill_updated_arrival_airport()
#     recommendation: Recommendation = rule_1(change_request)
#     assert recommendation is not None
#     assert recommendation.rule_id == "rule_1"
#     assert recommendation.outcome == Decision.ACCEPTED


def test_apply_rules():
    change_request: ChangeRequest = change_request_piece_updated_goods_description()
    recommendations = apply_rules(change_request)
    assert recommendations is not None
