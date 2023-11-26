from datetime import datetime
from enum import Enum
from typing import List, Union, Optional

from pydantic import BaseModel, Field, model_validator, ConfigDict
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated

from models import Thing

# Represents an ObjectId field in the database.
# It will be represented as a `str` on the model so that it can be serialized to JSON.
PyObjectId = Annotated[str, BeforeValidator(str)]


class ErrorDetails(BaseModel):
    code: Optional[str] = Field(None, alias="https://onerecord.iata.org/ns/api#hasCode")
    message: Optional[str] = Field(
        None, alias="https://onerecord.iata.org/ns/api#hasMessage"
    )
    property: Optional[str] = Field(
        None, alias="https://onerecord.iata.org/ns/api#hasProperty"
    )
    resource: Optional[str] = Field(
        None, alias="https://onerecord.iata.org/ns/api#hasResource"
    )


class Error(BaseModel):
    title: Optional[str] = Field(
        None, alias="https://onerecord.iata.org/ns/api#hasTitle"
    )
    errorDetails: Optional[List[ErrorDetails]] = Field(
        None, alias="https://onerecord.iata.org/ns/api#hasErrorDetail"
    )


class ActionRequest(BaseModel):
    id: Optional[PyObjectId] = Field(alias="@id", default=None)
    errors: Optional[List[Error]] = Field(
        None, alias="https://onerecord.iata.org/ns/api#hasError"
    )


class OperationObject(BaseModel):
    datatype: str = Field(alias="https://onerecord.iata.org/ns/api#hasDatatype")
    value: str = Field(alias="https://onerecord.iata.org/ns/api#hasValue")


class MeasurementUnit(BaseModel):
    id: str = Field(..., alias="@id")


class Value(BaseModel):
    id: str = Field(..., alias="@id")
    type: str = Field(..., alias="@type")
    numerical_value: float = Field(
        ..., alias="https://onerecord.iata.org/ns/cargo#numericalValue"
    )
    unit: MeasurementUnit = Field(..., alias="https://onerecord.iata.org/ns/cargo#unit")


class LinkedLogisticsObject(Thing):
    id: str = Field(..., alias="@id")


class CodeListElement(Thing):
    code: Optional[str] = Field(None, alias="https://onerecord.iata.org/ns/cargo#code")
    codeDescription: Optional[str] = Field(
        None, alias="https://onerecord.iata.org/ns/cargo#codeDescription"
    )
    codeLevel: Optional[int] = Field(
        None, alias="https://onerecord.iata.org/ns/cargo#codeLevel"
    )
    codeListName: Optional[str] = Field(
        None, alias="https://onerecord.iata.org/ns/cargo#codeListName"
    )
    codeListReference: Optional[str] = Field(
        None, alias="https://onerecord.iata.org/ns/cargo#codeListReference"
    )
    codeListVersion: Optional[str] = Field(
        None, alias="https://onerecord.iata.org/ns/cargo#codeListVersion"
    )


class Location(BaseModel):
    id: Optional[str] = Field(alias="@id", default=None)
    type: Optional[str] = Field(None, alias="@type")
    locationName: Optional[str] = Field(
        None, alias="https://onerecord.iata.org/ns/cargo#locationName"
    )
    locationType: Optional[str] = Field(
        None, alias="https://onerecord.iata.org/ns/cargo#locationType"
    )
    locationCodes: List[CodeListElement] = Field(
        None, alias="https://onerecord.iata.org/ns/cargo#locationCodes"
    )


class CarrierProduct(Thing):
    productCode: Optional[CodeListElement] = Field(
        None, alias="https://onerecord.iata.org/ns/cargo#productCode"
    )
    productDescription: Optional[str] = Field(
        None, alias="https://onerecord.iata.org/ns/cargo#productDescription"
    )
    serviceLevelCode: Optional[CodeListElement] = Field(
        None, alias="https://onerecord.iata.org/ns/cargo#serviceLevelCode"
    )


class LogisticsObject(BaseModel):
    id: str = Field(..., alias="@id")
    type: Optional[str] = Field(None, alias="@type")
    goods_description: Optional[str] = Field(
        None, alias="https://onerecord.iata.org/ns/cargo#goodsDescription"
    )
    gross_weight: Optional[Value] = Field(
        None, alias="https://onerecord.iata.org/ns/cargo#grossWeight"
    )
    arrivalLocation: Optional[Location] = Field(
        None, alias="https://onerecord.iata.org/ns/cargo#arrivalLocation"
    )
    departureLocation: Optional[Location] = Field(
        None, alias="https://onerecord.iata.org/ns/cargo#departureLocation"
    )
    coload: Optional[bool] = Field(
        None, alias="https://onerecord.iata.org/ns/cargo#coload"
    )
    carrierProduct: Optional[CarrierProduct] = Field(
        None, alias="https://onerecord.iata.org/ns/cargo#carrierProduct"
    )
    securityStatus: Optional[CodeListElement] = Field(
        None, alias="https://onerecord.iata.org/ns/cargo#securityStatus"
    )
    pieces: Optional[LinkedLogisticsObject] = Field(
        None, alias="https://onerecord.iata.org/ns/cargo#pieces"
    )
    total_gross_weight: Optional[Union[Value, LinkedLogisticsObject]] = Field(
        None, alias="https://onerecord.iata.org/ns/cargo#totalGrossWeight"
    )
    waybill: Optional[LinkedLogisticsObject] = Field(
        None, alias="https://onerecord.iata.org/ns/cargo#waybill"
    )
    shipment: Optional[LinkedLogisticsObject] = Field(
        None, alias="https://onerecord.iata.org/ns/cargo#shipment"
    )
    waybill_number: Optional[str] = Field(
        None, alias="https://onerecord.iata.org/ns/cargo#waybillNumber"
    )
    waybill_prefix: Optional[str] = Field(
        None, alias="https://onerecord.iata.org/ns/cargo#waybillPrefix"
    )
    waybill_type: Optional[LinkedLogisticsObject] = Field(
        None, alias="https://onerecord.iata.org/ns/cargo#waybillType"
    )
    booking_to_update: Optional[LinkedLogisticsObject] = Field(
        None, alias="https://onerecord.iata.org/ns/cargo#bookingToUpdate"
    )
    carrier_product: Optional[CarrierProduct] = Field(
        None, alias="https://onerecord.iata.org/ns/cargo#carrierProduct"
    )
    issued_for_piece: Optional[LinkedLogisticsObject] = Field(
        None, alias="https://onerecord.iata.org/ns/cargo#issuedForPiece"
    )

    model_config = ConfigDict(
        populate_by_name=True,
    )

    @model_validator(mode="before")
    def pre_process(self: dict):
        if (
            "https://onerecord.iata.org/ns/cargo#coload" in self
            and isinstance(self["https://onerecord.iata.org/ns/cargo#coload"], dict)
            and "@value" in self["https://onerecord.iata.org/ns/cargo#coload"]
        ):
            self["https://onerecord.iata.org/ns/cargo#coload"] = str(
                self["https://onerecord.iata.org/ns/cargo#coload"]["@value"]
            )
        if (
            "https://onerecord.iata.org/ns/cargo#goodsDescription" in self
            and isinstance(
                self["https://onerecord.iata.org/ns/cargo#goodsDescription"], dict
            )
            and "@value" in self["https://onerecord.iata.org/ns/cargo#goodsDescription"]
        ):
            self["https://onerecord.iata.org/ns/cargo#goodsDescription"] = str(
                self["https://onerecord.iata.org/ns/cargo#goodsDescription"]["@value"]
            )
        if (
            "https://onerecord.iata.org/ns/cargo#goodsDescription" in self
            and isinstance(
                self["https://onerecord.iata.org/ns/cargo#goodsDescription"], list
            )
        ):
            self["https://onerecord.iata.org/ns/cargo#goodsDescription"] = self[
                "https://onerecord.iata.org/ns/cargo#goodsDescription"
            ][0]
        if (
            "https://onerecord.iata.org/ns/cargo#goodsDescription" in self
            and isinstance(
                self["https://onerecord.iata.org/ns/cargo#goodsDescription"], list
            )
            and "@value"
            in self["https://onerecord.iata.org/ns/cargo#goodsDescription"][0]
        ):
            self["https://onerecord.iata.org/ns/cargo#goodsDescription"] = str(
                self["https://onerecord.iata.org/ns/cargo#goodsDescription"][0][
                    "@value"
                ]
            )
        if (
            "https://onerecord.iata.org/ns/cargo#arrivalLocation" in self
            and isinstance(
                self["https://onerecord.iata.org/ns/cargo#arrivalLocation"], list
            )
        ):
            self["https://onerecord.iata.org/ns/cargo#arrivalLocation"] = self[
                "https://onerecord.iata.org/ns/cargo#arrivalLocation"
            ][0]
        if (
            "https://onerecord.iata.org/ns/cargo#departureLocation" in self
            and isinstance(
                self["https://onerecord.iata.org/ns/cargo#departureLocation"], list
            )
        ):
            self["https://onerecord.iata.org/ns/cargo#departureLocation"] = self[
                "https://onerecord.iata.org/ns/cargo#departureLocation"
            ][0]
        return self


class OperationDetail(BaseModel):
    id: str = Field(..., alias="@id")
    datatype: Optional[str] = Field(
        None, alias="https://onerecord.iata.org/ns/api#hasDatatype"
    )
    value: Optional[str] = Field(
        None, alias="https://onerecord.iata.org/ns/api#hasValue"
    )

    model_config = ConfigDict(
        populate_by_name=True,
    )


class PatchOperation(BaseModel):
    id: str = Field(..., alias="@id")

    model_config = ConfigDict(
        populate_by_name=True,
    )


class Operation(BaseModel):
    id: str = Field(..., alias="@id")
    o: Optional[OperationDetail] = Field(
        None, alias="https://onerecord.iata.org/ns/api#o"
    )
    op: PatchOperation = Field(None, alias="https://onerecord.iata.org/ns/api#op")
    p: str = Field(..., alias="https://onerecord.iata.org/ns/api#p")
    s: str = Field(..., alias="https://onerecord.iata.org/ns/api#s")

    model_config = ConfigDict(
        populate_by_name=True,
    )


class Revision(BaseModel):
    type: str = Field(..., alias="@type")
    value: str = Field(..., alias="@value")


class Change(BaseModel):
    id: str = Field(..., alias="@id")
    type: str = Field(..., alias="@type")
    description: str = Field(
        ..., alias="https://onerecord.iata.org/ns/api#hasDescription"
    )
    logistics_object: LogisticsObject = Field(
        ..., alias="https://onerecord.iata.org/ns/api#hasLogisticsObject"
    )
    operations: List[Operation] = Field(
        ..., alias="https://onerecord.iata.org/ns/api#hasOperation"
    )
    revision: int = Field(..., alias="https://onerecord.iata.org/ns/api#hasRevision")
    notify_request_status_change: bool = Field(
        ..., alias="https://onerecord.iata.org/ns/api#notifyRequestStatusChange"
    )

    model_config = ConfigDict(
        populate_by_name=True,
    )

    @model_validator(mode="before")
    def preproces(self: dict):
        if "https://onerecord.iata.org/ns/api#hasRevision" in self:
            if isinstance(self["https://onerecord.iata.org/ns/api#hasRevision"], int):
                return self["https://onerecord.iata.org/ns/api#hasRevision"]
            else:
                self["https://onerecord.iata.org/ns/api#hasRevision"] = int(
                    self["https://onerecord.iata.org/ns/api#hasRevision"]["@value"]
                )
        if "https://onerecord.iata.org/ns/api#hasOperation" in self and isinstance(
            self["https://onerecord.iata.org/ns/api#hasOperation"], dict
        ):
            self["https://onerecord.iata.org/ns/api#hasOperation"] = [
                self["https://onerecord.iata.org/ns/api#hasOperation"]
            ]
        return self


class RequestStatus(BaseModel):
    id: str = Field(..., alias="@id")

    model_config = ConfigDict(
        populate_by_name=True,
    )


class RequestedAt(BaseModel):
    type: str = Field(..., alias="@type")
    value: str = Field(..., alias="@value")


class Organization(BaseModel):
    id: str = Field(..., alias="@id")

    model_config = ConfigDict(
        populate_by_name=True,
    )


class ApprovalStatus(str, Enum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    AUTO_ACCEPTED = "AUTO_ACCEPTED"
    AUTO_REJECTED = "AUTO_REJECTED"
    MANUAL_CHECK_REQUIRED = "MANUAL_CHECK_REQUIRED"


class Decision(str, Enum):
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    MANUAL_CHECK_REQUIRED = "MANUAL_CHECK_REQUIRED"


class Recommendation(BaseModel):
    rule_id: str
    decision: Decision = Field(..., alias="decision")


class ChangeRequest(ActionRequest):
    id: Optional[str] = Field(alias="_id", default=None)
    change_request_id: str = Field(..., alias="@id")
    type: str = Field(..., alias="@type")
    change: Change = Field(..., alias="https://onerecord.iata.org/ns/api#hasChange")
    request_status: RequestStatus = Field(
        ..., alias="https://onerecord.iata.org/ns/api#hasRequestStatus"
    )
    requested_at: datetime = Field(
        ..., alias="https://onerecord.iata.org/ns/api#isRequestedAt"
    )
    requested_by: Organization = Field(
        ..., alias="https://onerecord.iata.org/ns/api#isRequestedBy"
    )
    original_logistics_object: Optional[LogisticsObject] = Field(
        None, alias="originalLogisticsObject"
    )
    updated_logistics_object: Optional[LogisticsObject] = Field(
        None, alias="updatedLogisticsObject"
    )
    recommendations: List[Recommendation] = Field(
        default_factory=list, alias="recommendations"
    )
    approval_status: ApprovalStatus = Field(
        ApprovalStatus.PENDING, alias="approvalStatus"
    )

    model_config = ConfigDict(
        populate_by_name=True,
    )

    @model_validator(mode="before")
    def extract_datetime(self: dict):
        datetime_str = None
        if (
            "https://onerecord.iata.org/ns/api#isRequestedAt" in self
            and "@value" in self["https://onerecord.iata.org/ns/api#isRequestedAt"]
        ):
            datetime_str = self["https://onerecord.iata.org/ns/api#isRequestedAt"][
                "@value"
            ]
        elif "https://onerecord.iata.org/ns/api#isRequestedAt" in self and isinstance(
            self["https://onerecord.iata.org/ns/api#isRequestedAt"], str
        ):
            datetime_str = self["https://onerecord.iata.org/ns/api#isRequestedAt"]
        # Handle 'Z' for UTC if present
        if datetime_str is not None:
            datetime_str = datetime_str.replace("Z", "+00:00")
            self[
                "https://onerecord.iata.org/ns/api#isRequestedAt"
            ] = datetime.fromisoformat(datetime_str)
        return self
