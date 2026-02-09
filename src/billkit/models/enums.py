from enum import Enum


class InvoiceStyle(str, Enum):
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


class DiscountType(str, Enum):
    Percentage = "percentage"
    Fixed = "fixed"
