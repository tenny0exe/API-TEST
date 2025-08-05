from pydantic import BaseModel, Field
from typing import Optional, Dict
from datetime import date

class WheelFields(BaseModel):
    treadDiameterNew: Optional[str]
    lastShopIssueSize: Optional[str]
    condemningDia: Optional[str]
    wheelGauge: Optional[str]
    variationSameAxle: Optional[str]
    variationSameBogie: Optional[str]
    variationSameCoach: Optional[str]
    wheelProfile: Optional[str]
    intermediateWWP: Optional[str]
    bearingSeatDiameter: Optional[str]
    rollerBearingOuterDia: Optional[str]
    rollerBearingBoreDia: Optional[str]
    rollerBearingWidth: Optional[str]
    axleBoxHousingBoreDia: Optional[str]
    wheelDiscWidth: Optional[str]

class WheelSpecificationBase(BaseModel):
    formNumber: str = Field(..., alias="formNumber")
    submittedBy: str = Field(..., alias="submittedBy")
    submittedDate: date = Field(..., alias="submittedDate")
    fields: WheelFields

class WheelSpecificationCreate(WheelSpecificationBase):
    pass

class WheelSpecificationResponse(BaseModel):
    formNumber: str
    submittedBy: str
    submittedDate: date
    status: str

    model_config = {
    "from_attributes": True
}
