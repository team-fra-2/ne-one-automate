from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field

from models.one_record import ApprovalStatus


class LO_TYPES(str, Enum):
    piece = "piece"
    shipment = "shipment"
    waybill = "waybill"


class ChangeRequestApproval(BaseModel):
    approval_status: ApprovalStatus = Field(
        ..., description="The approval status object"
    )
    comment: str = Field(None, description="Comment on the decision")


class Rule(BaseModel):
    id: Optional[str] = Field(alias="_id", default=None)
    rule_id: str = Field(..., description="The rule id, e.g. rule-1, rule-2")
    active: bool = Field(True, description="Whether the rule is active or not")
    name: Optional[str] = Field(None, description="Name of the rule")
    description: Optional[str] = Field(None, description="Description of the rule")
    last_updated: datetime = Field(
        default_factory=datetime.utcnow, description="When the rule was last updated"
    )
    last_applied: Optional[datetime] = Field(
        default_factory=datetime.utcnow, description="When the rule was last applied"
    )
    workspace_xml: str = Field(..., description="The blockly workspace XML of the rule")
    function_code: str = Field(
        ..., description="The python function code of the rule ase base64 encoded"
    )
