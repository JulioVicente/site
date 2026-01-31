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
    
    class Config:
        populate_by_name = True
