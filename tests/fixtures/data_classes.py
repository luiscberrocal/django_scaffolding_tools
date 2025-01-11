from decimal import Decimal
from typing import List, Union

from pydantic import BaseModel, Field


class APIResponse(BaseModel):
    """
    Not used with responses for BCP so that we can use the __dict__ attribute without issues
    """

    status_code: int
    message: str

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


class PaymentAmount(BaseModel):
    amount_type: str = Field(alias="amountType")
    amount: str

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


class PaymentDocument(BaseModel):
    """
    Document ID must identify a payment uniquely as it will be used as a key
    in the payment endpoint.
    For now, we are using: {ContractId}-{shouldBeRepaidOn}
    This respects the restriction that document id must be at most 28 characters long.
    shouldBeRepaidOn comes from Zoral in the format %m-%d-%Y.
    We convert it and use it in the format: %Y-%m-%d for internal use and for the id.
    """

    document_id: str = Field(alias="documentId")
    expiration_date: str = Field(alias="expirationDate")
    payment_detail: str = Field(alias="paymentDetail")
    amounts: List[PaymentAmount]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


class ClientLookupResponse(BaseModel):
    rqUUID: str
    result_code: str = Field(alias="resultCode")
    result_description: str = Field(alias="resultDescription")
    operation_date: str = Field(
        alias="operationDate", description="This is the time and date the transaction was processed"
    )
    operation_number_company: Union[str, None] = Field(
        alias="operationNumberCompany",
        description="The field below follows the format:" " LU-{ClientLookupTransaction.id} Where LU stands for Lookup",
    )
    customer_name: Union[str, None] = Field(alias="customerName")
    documents: Union[List[PaymentDocument], None]
    result_code_company: Union[str, None] = Field(alias="resultCodeCompany")
    result_description_company: Union[str, None] = Field(alias="resultDescriptionCompany")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


class ZoralPaymentSchedule(BaseModel):
    amount: Decimal
    should_be_repaid_on: str = Field(alias="shouldBeRepaidOn")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


class GraphQLPaymentScheduleResponse(APIResponse):
    data: List[ZoralPaymentSchedule]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


class ZoralClientBalance(BaseModel):
    contract_id: str = Field(alias="ContractId")
    first_name: str = Field(alias="firstname")
    last_name: str = Field(alias="lastname")
    next_payment_date: str = Field(alias="nextpaymentdate")
    loan_repayment_amount: Decimal = Field(alias="loanrepaymentamount")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


class GraphQLClientBalanceResponse(APIResponse):
    data: Union[ZoralClientBalance, None]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


class ClientDataLookupResult(BaseModel):
    successful: bool
    message: str
    customer_name: str
    financial_product_id: str
    documents: List[PaymentDocument]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


class PaymentResponse(BaseModel):
    rqUUID: str
    result_code: str = Field(alias="resultCode")
    result_description: str = Field(alias="resultDescription")
    operation_date: str = Field(alias="operationDate")
    operation_number_company: Union[str, None] = Field(alias="operationNumberCompany")
    endorsement: Union[str, None]
    result_code_company: Union[str, None] = Field(alias="resultCodeCompany")
    result_description_company: Union[str, None] = Field(alias="resultDescriptionCompany")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


class RefundResponse(BaseModel):
    rqUUID: str
    resultCode: str
    resultDescription: str
    operationDate: str
    result_code_company: Union[str, None] = Field(alias="resultCodeCompany")
    result_description_company: Union[str, None] = Field(alias="resultDescriptionCompany")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
