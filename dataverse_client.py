"""
Dataverse Client
Handles authentication and API calls to Microsoft Dataverse
"""
import os
import re
import requests
import hashlib
import json
from typing import List, Dict, Optional, Any, Tuple
from datetime import datetime, timedelta
import math


class SimpleCache:
    """Simple in-memory cache with TTL (Time To Live)"""
    
    def __init__(self, default_ttl_seconds: int = 300):
        """
        Initialize cache
        
        Args:
            default_ttl_seconds: Default time to live for cache entries (default: 5 minutes)
        """
        self._cache: Dict[str, Tuple[Any, datetime]] = {}
        self._default_ttl = default_ttl_seconds
    
    def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache if not expired
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None if not found or expired
        """
        if key in self._cache:
            value, expiry = self._cache[key]
            if datetime.now() < expiry:
                return value
            else:
                # Remove expired entry
                del self._cache[key]
        return None
    
    def set(self, key: str, value: Any, ttl_seconds: Optional[int] = None) -> None:
        """
        Set value in cache with TTL
        
        Args:
            key: Cache key
            value: Value to cache
            ttl_seconds: Time to live in seconds (uses default if not specified)
        """
        ttl = ttl_seconds if ttl_seconds is not None else self._default_ttl
        expiry = datetime.now() + timedelta(seconds=ttl)
        self._cache[key] = (value, expiry)
    
    def clear(self) -> None:
        """Clear all cache entries"""
        self._cache.clear()
    
    def cleanup_expired(self) -> None:
        """Remove all expired entries from cache"""
        now = datetime.now()
        expired_keys = [key for key, (_, expiry) in self._cache.items() if now >= expiry]
        for key in expired_keys:
            del self._cache[key]
    
    def get_stats(self) -> Dict[str, int]:
        """Get cache statistics"""
        self.cleanup_expired()
        return {
            "total_entries": len(self._cache),
            "cache_size_bytes": sum(len(str(v)) for v, _ in self._cache.values())
        }


class DataverseClient:
    """Client for interacting with Microsoft Dataverse API"""
    
    # GUID validation pattern
    GUID_PATTERN = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', re.IGNORECASE)
    
    # Field selections for complete entity returns
    ACCOUNT_FIELDS = (
        "accountid,name,accountnumber,new_cnpj,numberofemployees,revenue,"
        "address1_postalcode,address1_line1,address1_city,address1_stateorprovince,"
        "address1_country,address1_latitude,address1_longitude,"
        "new_lastvisitdate,new_lastcontactdate,telephone1,emailaddress1,websiteurl,"
        "createdon,modifiedon,statecode,statuscode"
    )
    
    CONTACT_FIELDS = (
        "contactid,firstname,lastname,fullname,emailaddress1,emailaddress2,"
        "telephone1,mobilephone,jobtitle,_parentcustomerid_value,"
        "createdon,modifiedon,statecode,statuscode,address1_line1,address1_city,"
        "address1_stateorprovince,address1_postalcode,address1_country"
    )
    
    OPPORTUNITY_FIELDS = (
        "opportunityid,name,_customerid_value,estimatedvalue,estimatedclosedate,"
        "actualvalue,actualclosedate,statuscode,statecode,description,"
        "createdon,modifiedon,closeprobability,budgetamount,purchasetimeframe,"
        "purchaseprocess,decisionmaker,timeline"
    )
    
    QUOTE_FIELDS = (
        "quoteid,name,quotenumber,_opportunityid_value,_customerid_value,"
        "totalamount,totaltax,totallineitemamount,statuscode,statecode,"
        "effectivefrom,effectiveto,createdon,modifiedon,discountamount,"
        "discountpercentage,freightamount"
    )
    
    OPPORTUNITY_PRODUCT_FIELDS = (
        "opportunityproductid,_opportunityid_value,_productid_value,"
        "quantity,priceperunit,baseamount,tax,extendedamount,"
        "createdon,modifiedon,description,lineitemnumber"
    )
    
    def __init__(self):
        self.base_url = os.getenv("DATAVERSE_URL", "").rstrip("/")
        self.client_id = os.getenv("DATAVERSE_CLIENT_ID")
        self.client_secret = os.getenv("DATAVERSE_CLIENT_SECRET")
        self.tenant_id = os.getenv("DATAVERSE_TENANT_ID")
        self.api_url = f"{self.base_url}/api/data/v9.2"
        self._access_token = None
        self._token_expires_at = None
        
        # Initialize cache with 5 minute TTL by default
        cache_ttl = int(os.getenv("DATAVERSE_CACHE_TTL", "300"))
        self._cache = SimpleCache(default_ttl_seconds=cache_ttl)
        self._cache_enabled = os.getenv("DATAVERSE_CACHE_ENABLED", "true").lower() == "true"
    
    @staticmethod
    def _generate_cache_key(entity: str, filter_query: Optional[str], 
                           select: Optional[str], top: int) -> str:
        """Generate a unique cache key based on query parameters"""
        key_data = {
            "entity": entity,
            "filter": filter_query or "",
            "select": select or "",
            "top": top
        }
        key_string = json.dumps(key_data, sort_keys=True)
        return hashlib.md5(key_string.encode()).hexdigest()
    
    @staticmethod
    def _sanitize_string(value: str) -> str:
        """Sanitize string values for OData queries by escaping single quotes"""
        if value is None:
            return ""
        return value.replace("'", "''")
    
    @staticmethod
    def _validate_guid(guid: str) -> str:
        """Validate and return GUID, raise ValueError if invalid"""
        if not DataverseClient.GUID_PATTERN.match(guid):
            raise ValueError(f"Invalid GUID format: {guid}")
        return guid
    
    def _get_access_token(self) -> str:
        """Get OAuth access token for Dataverse API"""
        if self._access_token and self._token_expires_at:
            if datetime.now() < self._token_expires_at:
                return self._access_token
        
        token_url = f"https://login.microsoftonline.com/{self.tenant_id}/oauth2/v2.0/token"
        
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "scope": f"{self.base_url}/.default",
            "grant_type": "client_credentials"
        }
        
        response = requests.post(token_url, data=data)
        response.raise_for_status()
        
        token_data = response.json()
        self._access_token = token_data["access_token"]
        expires_in = token_data.get("expires_in", 3600)
        self._token_expires_at = datetime.now() + timedelta(seconds=expires_in - 300)
        
        return self._access_token
    
    def _get_headers(self) -> Dict[str, str]:
        """Get headers for API requests"""
        return {
            "Authorization": f"Bearer {self._get_access_token()}",
            "OData-MaxVersion": "4.0",
            "OData-Version": "4.0",
            "Accept": "application/json",
            "Content-Type": "application/json; charset=utf-8",
            "Prefer": "return=representation"
        }
    
    def _query(self, entity: str, filter_query: Optional[str] = None, 
               select: Optional[str] = None, top: int = 100, use_cache: bool = True) -> List[Dict[str, Any]]:
        """
        Execute a query against Dataverse with optional caching
        
        Args:
            entity: Entity name to query
            filter_query: OData filter query
            select: Fields to select
            top: Maximum number of results
            use_cache: Whether to use cache for this query (default: True)
        
        Returns:
            List of entity records
        """
        # Generate cache key
        cache_key = self._generate_cache_key(entity, filter_query, select, top)
        
        # Try to get from cache if enabled
        if self._cache_enabled and use_cache:
            cached_result = self._cache.get(cache_key)
            if cached_result is not None:
                return cached_result
        
        # Execute query
        url = f"{self.api_url}/{entity}"
        params = {}
        
        if filter_query:
            params["$filter"] = filter_query
        if select:
            params["$select"] = select
        if top:
            params["$top"] = top
        
        response = requests.get(url, headers=self._get_headers(), params=params)
        response.raise_for_status()
        
        data = response.json()
        result = data.get("value", [])
        
        # Store in cache if enabled
        if self._cache_enabled and use_cache:
            self._cache.set(cache_key, result)
        
        return result
    
    def clear_cache(self) -> None:
        """Clear all cached query results"""
        self._cache.clear()
    
    def get_cache_stats(self) -> Dict[str, int]:
        """Get cache statistics"""
        return self._cache.get_stats()
    
    # Account (Company) operations
    def search_accounts_by_id(self, account_id: str) -> List[Dict[str, Any]]:
        """Search accounts by ID with complete field set"""
        account_id = self._validate_guid(account_id)
        return self._query(
            "accounts",
            filter_query=f"accountid eq {account_id}",
            select=self.ACCOUNT_FIELDS
        )
    
    def search_accounts_by_name(self, name: str) -> List[Dict[str, Any]]:
        """Search accounts by name"""
        name = self._sanitize_string(name)
        return self._query("accounts", filter_query=f"contains(name, '{name}')")
    
    def search_accounts_by_cnpj(self, cnpj: str) -> List[Dict[str, Any]]:
        """Search accounts by CNPJ"""
        cnpj = self._sanitize_string(cnpj)
        return self._query("accounts", filter_query=f"new_cnpj eq '{cnpj}'")
    
    def search_accounts_by_proximity(self, cep: str, radius_km: float = 50) -> List[Dict[str, Any]]:
        """
        Search accounts by proximity to a ZIP code (CEP)
        This is a simplified implementation. In production, you would:
        1. First geocode the CEP to get coordinates
        2. Then filter accounts by distance using geography functions
        """
        # First, get the coordinates for the CEP (this would need a geocoding service)
        # For this example, we'll search by CEP directly
        cep = self._sanitize_string(cep)
        accounts = self._query("accounts", filter_query=f"contains(address1_postalcode, '{cep}')")
        
        # In a real implementation, you would calculate distance using Haversine formula
        # and filter by radius_km
        return accounts
    
    def search_accounts_by_employees_and_revenue(
        self, min_employees: Optional[int] = None, max_employees: Optional[int] = None,
        min_revenue: Optional[float] = None, max_revenue: Optional[float] = None
    ) -> List[Dict[str, Any]]:
        """Search accounts by number of employees and revenue"""
        filters = []
        
        if min_employees is not None:
            filters.append(f"numberofemployees ge {min_employees}")
        if max_employees is not None:
            filters.append(f"numberofemployees le {max_employees}")
        if min_revenue is not None:
            filters.append(f"revenue ge {min_revenue}")
        if max_revenue is not None:
            filters.append(f"revenue le {max_revenue}")
        
        filter_query = " and ".join(filters) if filters else None
        return self._query("accounts", filter_query=filter_query)
    
    def search_accounts_by_days_without_visit(self, days: int) -> List[Dict[str, Any]]:
        """Search accounts by days without visit"""
        date_threshold = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        return self._query(
            "accounts",
            filter_query=f"new_lastvisitdate lt {date_threshold} or new_lastvisitdate eq null"
        )
    
    def search_accounts_by_days_without_contact(self, days: int) -> List[Dict[str, Any]]:
        """Search accounts by days without contact"""
        date_threshold = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        return self._query(
            "accounts",
            filter_query=f"new_lastcontactdate lt {date_threshold} or new_lastcontactdate eq null"
        )
    
    def list_accounts(self, top: int = 100) -> List[Dict[str, Any]]:
        """List all accounts"""
        return self._query("accounts", top=top)
    
    # Contact operations
    def search_contacts_by_id(self, contact_id: str) -> List[Dict[str, Any]]:
        """Search contacts by ID with complete field set"""
        contact_id = self._validate_guid(contact_id)
        return self._query(
            "contacts",
            filter_query=f"contactid eq {contact_id}",
            select=self.CONTACT_FIELDS
        )
    
    def search_contacts_by_name(self, name: str) -> List[Dict[str, Any]]:
        """Search contacts by name"""
        name = self._sanitize_string(name)
        return self._query(
            "contacts",
            filter_query=f"contains(fullname, '{name}') or contains(firstname, '{name}') or contains(lastname, '{name}')"
        )
    
    def search_contacts_by_email(self, email: str) -> List[Dict[str, Any]]:
        """Search contacts by email"""
        email = self._sanitize_string(email)
        return self._query(
            "contacts",
            filter_query=f"contains(emailaddress1, '{email}') or contains(emailaddress2, '{email}')"
        )
    
    # Opportunity operations
    def search_opportunities_by_id(self, opportunity_id: str) -> List[Dict[str, Any]]:
        """Search opportunities by ID with complete field set"""
        opportunity_id = self._validate_guid(opportunity_id)
        return self._query(
            "opportunities",
            filter_query=f"opportunityid eq {opportunity_id}",
            select=self.OPPORTUNITY_FIELDS
        )
    
    def search_opportunities_by_name(self, name: str) -> List[Dict[str, Any]]:
        """Search opportunities by name"""
        name = self._sanitize_string(name)
        return self._query("opportunities", filter_query=f"contains(name, '{name}')")
    
    def search_opportunities_by_account(self, account_id: str) -> List[Dict[str, Any]]:
        """Search opportunities by account"""
        account_id = self._validate_guid(account_id)
        return self._query("opportunities", filter_query=f"_customerid_value eq {account_id}")
    
    # Quote operations
    def search_quotes_by_opportunity(self, opportunity_id: str) -> List[Dict[str, Any]]:
        """Search quotes by opportunity with complete field set"""
        opportunity_id = self._validate_guid(opportunity_id)
        return self._query(
            "quotes",
            filter_query=f"_opportunityid_value eq {opportunity_id}",
            select=self.QUOTE_FIELDS
        )
    
    def search_quotes_by_code(self, quote_number: str) -> List[Dict[str, Any]]:
        """Search quotes by quote code/number with complete field set"""
        quote_number = self._sanitize_string(quote_number)
        return self._query(
            "quotes",
            filter_query=f"quotenumber eq '{quote_number}'",
            select=self.QUOTE_FIELDS
        )
    
    # Product operations
    def search_products_by_opportunity(self, opportunity_id: str) -> List[Dict[str, Any]]:
        """Search products from an opportunity with complete field set"""
        opportunity_id = self._validate_guid(opportunity_id)
        return self._query(
            "opportunityproducts",
            filter_query=f"_opportunityid_value eq {opportunity_id}",
            select=self.OPPORTUNITY_PRODUCT_FIELDS
        )
    
    def calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calculate distance between two coordinates using Haversine formula
        Returns distance in kilometers
        """
        R = 6371  # Earth's radius in kilometers
        
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lon = math.radians(lon2 - lon1)
        
        a = (math.sin(delta_lat / 2) ** 2 +
             math.cos(lat1_rad) * math.cos(lat2_rad) *
             math.sin(delta_lon / 2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        return R * c
