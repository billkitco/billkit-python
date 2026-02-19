from collections.abc import Sequence
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class Summary(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    total: Decimal = Field(..., alias="total")
    count: int = Field(..., alias="count")
    overdue_count: int = Field(..., alias="overdueCount")


class PeriodItem(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    period: str
    total: Decimal
    count: int


class ByClientItem(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    label: str
    total: Decimal
    count: int


class ByStatusItem(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    label: str
    total: Decimal
    count: int


class Currency(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    code: str
    name: str
    symbol: str


class ByPeriod(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    daily: Sequence[PeriodItem] = Field(..., alias="daily")
    weekly: Sequence[PeriodItem] = Field(..., alias="weekly")
    monthly: Sequence[PeriodItem] = Field(..., alias="monthly")
    yearly: Sequence[PeriodItem] = Field(..., alias="yearly")


class RevenueReportResponse(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    currency_code: str = Field(..., alias="currencyCode")
    currency_symbol: str = Field(..., alias="currencySymbol")
    summary: Summary
    by_period: ByPeriod = Field(..., alias="byPeriod")
    by_client: Sequence[ByClientItem] = Field(..., alias="byClient")
    by_status: Sequence[ByStatusItem] = Field(..., alias="byStatus")
    available_currencies: Sequence[Currency] = Field(..., alias="availableCurrencies")
    """
    This is a Sequence of currencies used in the saved created invoices.
    """
