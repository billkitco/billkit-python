from enum import StrEnum


class _DocumentStyle(StrEnum):
    ClassicLeftLogo = "Classic Left Logo"
    ModernCenteredLogo = "Modern Centered Logo"
    CompactSingleColumn = "Compact Single-Column"
    DetailedBusinessVatTaxHeavy = "Detailed Business (VAT/Tax Heavy)"
    ServicesTimeTrackingInvoice = "Services / Time-Tracking Invoice"
    ProductItemisedInvoice = "Product / Itemised Invoice"
    CreativeAgencyStyle = "Creative / Agency Style"
    RetainerSubscriptionInvoice = "Retainer / Subscription Invoice"
    MinimalMonochrome = "Minimal Monochrome"
    BoldRightLogoLayout = "Bold Right-Logo Layout"


    @classmethod
    def as_invoice_style(cls) -> type[StrEnum]:
        return StrEnum('InvoiceStyle', {name: value for name, value in cls.__members__.items()})
    
    @classmethod
    def as_quote_style(cls) -> type[StrEnum]:
        return StrEnum('QuoteStyle', {name: value for name, value in cls.__members__.items()})

InvoiceStyle = _DocumentStyle.as_invoice_style()
QuoteStyle = _DocumentStyle.as_quote_style()

class DiscountType(StrEnum):
    Percentage = "percentage"
    Fixed = "fixed"
