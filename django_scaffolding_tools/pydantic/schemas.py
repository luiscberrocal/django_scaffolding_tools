from typing import Optional

from pydantic import BaseModel, Field


class StatusChangeEvent(BaseModel):
    """This model is used to send the status change event to the Kafka topic"""

    service_source: str = Field(
        alias="serviceSource", description="The service that is sending the event.", exanple="d_local_integration"
    )
    service_version: str = Field(
        alias="serviceVersion",
        description="The version of the service at the moment the event was sent.",
        example="1.0.0",
    )
    country: str = Field(description="The country code of the event", example="ZA")
    payment_provider: str = Field(
        alias="paymentProvider", description="The payment provider that processed the payment.", example="D_LOCAL"
    )
    payment_id: str = Field(alias="paymentId", description="The payment id that was processed")
    status: str = Field(description="The new status of the payment")
    previous_status: Optional[str] = Field(
        alias="previousStatus", description="The previous status of the payment", default=None
    )

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
