"""
Dataverse Entity Models
Defines the structure of Microsoft Dataverse entities
"""
from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime


class Account(BaseModel):
    """
    Account (Company/Empresa) entity in Dataverse
    """
    accountid: Optional[str] = Field(None, description="Unique identifier for the account")
    name: Optional[str] = Field(None, description="Company name")
    accountnumber: Optional[str] = Field(None, description="Account number")
    # CNPJ - Brazilian company tax identification number
    cnpj: Optional[str] = Field(None, alias="new_cnpj", description="CNPJ (Brazilian company tax ID)")
    numberofemployees: Optional[int] = Field(None, description="Number of employees")
    revenue: Optional[float] = Field(None, description="Annual revenue")
    address1_postalcode: Optional[str] = Field(None, description="ZIP code / CEP")
    address1_line1: Optional[str] = Field(None, description="Address line 1")
    address1_city: Optional[str] = Field(None, description="City")
    address1_stateorprovince: Optional[str] = Field(None, description="State")
    address1_country: Optional[str] = Field(None, description="Country")
    address1_latitude: Optional[float] = Field(None, description="Latitude")
    address1_longitude: Optional[float] = Field(None, description="Longitude")
    # Custom fields for tracking
    lastvisitdate: Optional[datetime] = Field(None, alias="new_lastvisitdate", description="Last visit date")
    lastcontactdate: Optional[datetime] = Field(None, alias="new_lastcontactdate", description="Last contact date")
    telephone1: Optional[str] = Field(None, description="Main phone number")
    emailaddress1: Optional[str] = Field(None, description="Email address")
    websiteurl: Optional[str] = Field(None, description="Website URL")
    # Standard Dataverse fields
    createdon: Optional[datetime] = Field(None, description="Date and time when the record was created")
    modifiedon: Optional[datetime] = Field(None, description="Date and time when the record was last modified")
    statecode: Optional[int] = Field(None, description="Status of the account (0=Active, 1=Inactive)")
    statuscode: Optional[int] = Field(None, description="Reason for the status of the account")
    
    class Config:
        populate_by_name = True


class Contact(BaseModel):
    """
    Contact (Contato) entity in Dataverse
    """
    contactid: Optional[str] = Field(None, description="Unique identifier for the contact")
    firstname: Optional[str] = Field(None, description="First name")
    lastname: Optional[str] = Field(None, description="Last name")
    fullname: Optional[str] = Field(None, description="Full name")
    emailaddress1: Optional[str] = Field(None, description="Primary email address")
    emailaddress2: Optional[str] = Field(None, description="Secondary email address")
    telephone1: Optional[str] = Field(None, description="Business phone")
    mobilephone: Optional[str] = Field(None, description="Mobile phone")
    jobtitle: Optional[str] = Field(None, description="Job title")
    parentcustomerid: Optional[str] = Field(None, alias="_parentcustomerid_value", description="Parent account ID")
    # Address fields
    address1_line1: Optional[str] = Field(None, description="Street address")
    address1_city: Optional[str] = Field(None, description="City")
    address1_stateorprovince: Optional[str] = Field(None, description="State or province")
    address1_postalcode: Optional[str] = Field(None, description="ZIP/postal code")
    address1_country: Optional[str] = Field(None, description="Country")
    # Standard Dataverse fields
    createdon: Optional[datetime] = Field(None, description="Date and time when the record was created")
    modifiedon: Optional[datetime] = Field(None, description="Date and time when the record was last modified")
    statecode: Optional[int] = Field(None, description="Status of the contact (0=Active, 1=Inactive)")
    statuscode: Optional[int] = Field(None, description="Reason for the status of the contact")
    
    class Config:
        populate_by_name = True


class Opportunity(BaseModel):
    """
    Opportunity (Oportunidade) entity in Dataverse
    """
    opportunityid: Optional[str] = Field(None, description="Unique identifier for the opportunity")
    name: Optional[str] = Field(None, description="Opportunity name")
    customerid: Optional[str] = Field(None, alias="_customerid_value", description="Customer account ID")
    estimatedvalue: Optional[float] = Field(None, description="Estimated value")
    estimatedclosedate: Optional[datetime] = Field(None, description="Estimated close date")
    actualvalue: Optional[float] = Field(None, description="Actual value")
    actualclosedate: Optional[datetime] = Field(None, description="Actual close date")
    statuscode: Optional[int] = Field(None, description="Status code")
    statecode: Optional[int] = Field(None, description="State code")
    description: Optional[str] = Field(None, description="Description")
    # Additional opportunity fields
    closeprobability: Optional[int] = Field(None, description="Probability of closing the opportunity")
    budgetamount: Optional[float] = Field(None, description="Budget amount")
    purchasetimeframe: Optional[int] = Field(None, description="Purchase timeframe")
    purchaseprocess: Optional[int] = Field(None, description="Purchase process")
    decisionmaker: Optional[bool] = Field(None, description="Whether contact is the decision maker")
    timeline: Optional[int] = Field(None, description="Timeline for the opportunity")
    # Standard Dataverse fields
    createdon: Optional[datetime] = Field(None, description="Date and time when the record was created")
    modifiedon: Optional[datetime] = Field(None, description="Date and time when the record was last modified")
    
    class Config:
        populate_by_name = True


class Quote(BaseModel):
    """
    Quote (Cotação) entity in Dataverse
    """
    quoteid: Optional[str] = Field(None, description="Unique identifier for the quote")
    name: Optional[str] = Field(None, description="Quote name")
    quotenumber: Optional[str] = Field(None, description="Quote number")
    opportunityid: Optional[str] = Field(None, alias="_opportunityid_value", description="Related opportunity ID")
    customerid: Optional[str] = Field(None, alias="_customerid_value", description="Customer account ID")
    totalamount: Optional[float] = Field(None, description="Total amount")
    totaltax: Optional[float] = Field(None, description="Total tax")
    totallineitemamount: Optional[float] = Field(None, description="Total line item amount")
    statuscode: Optional[int] = Field(None, description="Status code")
    statecode: Optional[int] = Field(None, description="State code")
    effectivefrom: Optional[datetime] = Field(None, description="Effective from date")
    effectiveto: Optional[datetime] = Field(None, description="Effective to date")
    # Additional quote fields
    discountamount: Optional[float] = Field(None, description="Discount amount")
    discountpercentage: Optional[float] = Field(None, description="Discount percentage")
    freightamount: Optional[float] = Field(None, description="Freight amount")
    # Standard Dataverse fields
    createdon: Optional[datetime] = Field(None, description="Date and time when the record was created")
    modifiedon: Optional[datetime] = Field(None, description="Date and time when the record was last modified")
    
    class Config:
        populate_by_name = True


class Product(BaseModel):
    """
    Product (Produto) entity in Dataverse
    """
    productid: Optional[str] = Field(None, description="Unique identifier for the product")
    name: Optional[str] = Field(None, description="Product name")
    productnumber: Optional[str] = Field(None, description="Product number")
    price: Optional[float] = Field(None, description="Price")
    description: Optional[str] = Field(None, description="Description")
    quantityonhand: Optional[float] = Field(None, description="Quantity on hand")
    
    class Config:
        populate_by_name = True


class OpportunityProduct(BaseModel):
    """
    OpportunityProduct (Product of an Opportunity) entity in Dataverse
    """
    opportunityproductid: Optional[str] = Field(None, description="Unique identifier")
    opportunityid: Optional[str] = Field(None, alias="_opportunityid_value", description="Opportunity ID")
    productid: Optional[str] = Field(None, alias="_productid_value", description="Product ID")
    quantity: Optional[float] = Field(None, description="Quantity")
    priceperunit: Optional[float] = Field(None, description="Price per unit")
    baseamount: Optional[float] = Field(None, description="Base amount")
    tax: Optional[float] = Field(None, description="Tax")
    extendedamount: Optional[float] = Field(None, description="Extended amount")
    # Additional fields
    description: Optional[str] = Field(None, description="Product description")
    lineitemnumber: Optional[int] = Field(None, description="Line item number")
    # Standard Dataverse fields
    createdon: Optional[datetime] = Field(None, description="Date and time when the record was created")
    modifiedon: Optional[datetime] = Field(None, description="Date and time when the record was last modified")
    
    class Config:
        populate_by_name = True


class Order(BaseModel):
    """
    Order (Pedido) entity in Dataverse
    Represents an actual purchase/order from a customer
    """
    orderid: Optional[str] = Field(None, description="Unique identifier for the order")
    ordernumber: Optional[str] = Field(None, description="Order number")
    name: Optional[str] = Field(None, description="Order name")
    
    # Relationships
    customerid: Optional[str] = Field(None, alias="_customerid_value", description="Customer account ID")
    opportunityid: Optional[str] = Field(None, alias="_opportunityid_value", description="Related opportunity ID")
    quoteid: Optional[str] = Field(None, alias="_quoteid_value", description="Related quote ID")
    
    # Values
    totalamount: Optional[float] = Field(None, description="Total amount")
    totaltax: Optional[float] = Field(None, description="Total tax")
    totallineitemamount: Optional[float] = Field(None, description="Total line items")
    discountamount: Optional[float] = Field(None, description="Discount amount")
    freightamount: Optional[float] = Field(None, description="Freight amount")
    
    # Dates
    orderdate: Optional[datetime] = Field(None, alias="new_orderdate", description="Order date")
    requesteddeliverydate: Optional[datetime] = Field(None, description="Requested delivery date")
    actualdeliverydate: Optional[datetime] = Field(None, description="Actual delivery date")
    
    # Status
    statecode: Optional[int] = Field(None, description="State code (0=Active, 1=Submitted, etc)")
    statuscode: Optional[int] = Field(None, description="Status reason code")
    orderstatus: Optional[str] = Field(None, description="Order status")
    
    # Type
    ordertype: Optional[str] = Field(None, description="Order type (new, renewal, upsell)")
    
    # Payment
    paymentterms: Optional[str] = Field(None, description="Payment terms")
    paymentstatus: Optional[str] = Field(None, description="Payment status")
    
    # Standard Dataverse fields
    createdon: Optional[datetime] = Field(None, description="Date and time when the record was created")
    modifiedon: Optional[datetime] = Field(None, description="Date and time when the record was last modified")
    
    class Config:
        populate_by_name = True


class OrderProduct(BaseModel):
    """
    OrderProduct (Item do Pedido) entity in Dataverse
    Represents a line item in an order
    """
    orderproductid: Optional[str] = Field(None, description="Unique identifier for the order product")
    orderid: Optional[str] = Field(None, alias="_orderid_value", description="Order ID")
    productid: Optional[str] = Field(None, alias="_productid_value", description="Product ID")
    
    # Quantities
    quantity: Optional[float] = Field(None, description="Quantity ordered")
    shippedquantity: Optional[float] = Field(None, description="Quantity shipped")
    
    # Values
    priceperunit: Optional[float] = Field(None, description="Price per unit")
    baseamount: Optional[float] = Field(None, description="Base amount")
    tax: Optional[float] = Field(None, description="Tax amount")
    extendedamount: Optional[float] = Field(None, description="Extended amount")
    manualdiscount: Optional[float] = Field(None, description="Manual discount")
    
    # Details
    description: Optional[str] = Field(None, description="Product description")
    lineitemnumber: Optional[int] = Field(None, description="Line item number")
    
    # Standard Dataverse fields
    createdon: Optional[datetime] = Field(None, description="Date and time when the record was created")
    modifiedon: Optional[datetime] = Field(None, description="Date and time when the record was last modified")
    
    class Config:
        populate_by_name = True


class Contract(BaseModel):
    """
    Contract (Contrato) entity in Dataverse
    Represents contracts with customers
    """
    contractid: Optional[str] = Field(None, description="Unique identifier for the contract")
    contractnumber: Optional[str] = Field(None, description="Contract number")
    title: Optional[str] = Field(None, description="Contract title")
    
    # Relationships
    customerid: Optional[str] = Field(None, alias="_customerid_value", description="Customer account ID")
    billingaccountid: Optional[str] = Field(None, alias="_billingaccountid_value", description="Billing account ID")
    
    # Dates
    contractstartdate: Optional[datetime] = Field(None, description="Contract start date")
    contractenddate: Optional[datetime] = Field(None, description="Contract end date")
    renewaldate: Optional[datetime] = Field(None, description="Renewal date")
    cancellationdate: Optional[datetime] = Field(None, description="Cancellation date")
    
    # Values
    totalcontractvalue: Optional[float] = Field(None, description="Total contract value")
    monthlyrecurringrevenue: Optional[float] = Field(None, alias="new_mrr", description="Monthly recurring revenue (MRR)")
    annualrecurringrevenue: Optional[float] = Field(None, alias="new_arr", description="Annual recurring revenue (ARR)")
    
    # Renewal
    contractterm: Optional[int] = Field(None, description="Contract term in months")
    renewalnoticerequired: Optional[int] = Field(None, description="Renewal notice required (days)")
    autorenewal: Optional[bool] = Field(None, description="Auto-renewal enabled")
    renewalstatus: Optional[str] = Field(None, description="Renewal status (pending, renewed, not_renewed)")
    
    # Status
    statecode: Optional[int] = Field(None, description="State code")
    statuscode: Optional[int] = Field(None, description="Status reason code")
    contractstatus: Optional[str] = Field(None, description="Contract status")
    
    # Type
    contracttype: Optional[str] = Field(None, description="Contract type (standard, custom, framework)")
    paymentterms: Optional[str] = Field(None, description="Payment terms")
    billingfrequency: Optional[str] = Field(None, description="Billing frequency (monthly, quarterly, annual)")
    
    # Standard Dataverse fields
    createdon: Optional[datetime] = Field(None, description="Date and time when the record was created")
    modifiedon: Optional[datetime] = Field(None, description="Date and time when the record was last modified")
    
    class Config:
        populate_by_name = True

