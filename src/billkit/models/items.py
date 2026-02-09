from decimal import Decimal

from .enums import DiscountType

from pydantic import BaseModel, Field, model_validator


class ItemsBase(BaseModel):
    description: str = Field(..., min_length=1)
    qty: int = Field(..., gt=0)
    price: Decimal = Field(..., gt=0)
    tax: Decimal = Field(default=Decimal("0.00"), ge=0)
    discount_type: DiscountType | None = None
    discount_value: Decimal = Field(default=Decimal("0.00"), ge=0)

    @model_validator(mode="after")
    def validate_discount(self) -> "ItemsBase":
        if self.discount_type is None:
            self.discount_value = Decimal("0.00")
            return self
        if self.discount_type == DiscountType.Percentage and self.discount_value > 100:
            raise ValueError("Percentage discount must be 100 or less")
        return self
