"""
MCP Server for Microsoft Dataverse
Implements Model Context Protocol server for Dataverse operations
"""
import json
import logging
from typing import Any, Dict, List, Optional
from dataverse_client import DataverseClient
from dataverse_models import Account, Contact, Opportunity, Quote, Product, OpportunityProduct

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MCPDataverseServer:
    """MCP Server for Dataverse operations"""
    
    def __init__(self):
        self.client = DataverseClient()
        self.tools = self._register_tools()
    
    def _register_tools(self) -> List[Dict[str, Any]]:
        """Register all available MCP tools"""
        return [
            {
                "name": "search_companies_by_id",
                "description": "Search companies (accounts) by ID",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "account_id": {
                            "type": "string",
                            "description": "The account ID to search for"
                        }
                    },
                    "required": ["account_id"]
                }
            },
            {
                "name": "search_companies_by_name",
                "description": "Search companies (accounts) by name",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "The company name to search for (partial match supported)"
                        }
                    },
                    "required": ["name"]
                }
            },
            {
                "name": "search_companies_by_cnpj",
                "description": "Search companies (accounts) by CNPJ (Brazilian company tax ID)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "cnpj": {
                            "type": "string",
                            "description": "The CNPJ number to search for"
                        }
                    },
                    "required": ["cnpj"]
                }
            },
            {
                "name": "search_companies_by_proximity",
                "description": "Search companies (accounts) by proximity to a ZIP code (CEP)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "cep": {
                            "type": "string",
                            "description": "The ZIP code (CEP) to search around"
                        },
                        "radius_km": {
                            "type": "number",
                            "description": "The search radius in kilometers (default: 50)",
                            "default": 50
                        }
                    },
                    "required": ["cep"]
                }
            },
            {
                "name": "search_companies_by_employees_revenue",
                "description": "Search companies by number of employees and revenue",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "min_employees": {
                            "type": "integer",
                            "description": "Minimum number of employees"
                        },
                        "max_employees": {
                            "type": "integer",
                            "description": "Maximum number of employees"
                        },
                        "min_revenue": {
                            "type": "number",
                            "description": "Minimum annual revenue"
                        },
                        "max_revenue": {
                            "type": "number",
                            "description": "Maximum annual revenue"
                        }
                    }
                }
            },
            {
                "name": "search_companies_by_days_without_visit",
                "description": "Search companies by days without visit",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "days": {
                            "type": "integer",
                            "description": "Number of days without visit"
                        }
                    },
                    "required": ["days"]
                }
            },
            {
                "name": "search_companies_by_days_without_contact",
                "description": "Search companies by days without contact",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "days": {
                            "type": "integer",
                            "description": "Number of days without contact"
                        }
                    },
                    "required": ["days"]
                }
            },
            {
                "name": "list_accounts",
                "description": "List all accounts",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "top": {
                            "type": "integer",
                            "description": "Maximum number of results to return (default: 100)",
                            "default": 100
                        }
                    }
                }
            },
            {
                "name": "search_contacts_by_id",
                "description": "Search contacts by ID",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "contact_id": {
                            "type": "string",
                            "description": "The contact ID to search for"
                        }
                    },
                    "required": ["contact_id"]
                }
            },
            {
                "name": "search_contacts_by_name",
                "description": "Search contacts by name",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "The contact name to search for (partial match supported)"
                        }
                    },
                    "required": ["name"]
                }
            },
            {
                "name": "search_contacts_by_email",
                "description": "Search contacts by email",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "email": {
                            "type": "string",
                            "description": "The email address to search for (partial match supported)"
                        }
                    },
                    "required": ["email"]
                }
            },
            {
                "name": "search_opportunities_by_id",
                "description": "Search opportunities by ID",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "opportunity_id": {
                            "type": "string",
                            "description": "The opportunity ID to search for"
                        }
                    },
                    "required": ["opportunity_id"]
                }
            },
            {
                "name": "search_opportunities_by_name",
                "description": "Search opportunities by name",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "The opportunity name to search for (partial match supported)"
                        }
                    },
                    "required": ["name"]
                }
            },
            {
                "name": "search_opportunities_by_account",
                "description": "Search opportunities by company/account",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "account_id": {
                            "type": "string",
                            "description": "The account ID to search opportunities for"
                        }
                    },
                    "required": ["account_id"]
                }
            },
            {
                "name": "search_quotes_by_opportunity",
                "description": "Search quotes by opportunity",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "opportunity_id": {
                            "type": "string",
                            "description": "The opportunity ID to search quotes for"
                        }
                    },
                    "required": ["opportunity_id"]
                }
            },
            {
                "name": "search_quotes_by_code",
                "description": "Search quotes by quote code/number",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "quote_number": {
                            "type": "string",
                            "description": "The quote number to search for"
                        }
                    },
                    "required": ["quote_number"]
                }
            },
            {
                "name": "search_products_by_opportunity",
                "description": "Search products from an opportunity",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "opportunity_id": {
                            "type": "string",
                            "description": "The opportunity ID to search products for"
                        }
                    },
                    "required": ["opportunity_id"]
                }
            },
            {
                "name": "clear_cache",
                "description": "Clear all cached query results",
                "inputSchema": {
                    "type": "object",
                    "properties": {}
                }
            },
            {
                "name": "get_cache_stats",
                "description": "Get cache statistics (total entries and size)",
                "inputSchema": {
                    "type": "object",
                    "properties": {}
                }
            }
        ]
    
    def handle_request(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle MCP request"""
        method = request_data.get("method")
        
        if method == "tools/list":
            return {
                "tools": self.tools
            }
        
        elif method == "tools/call":
            tool_name = request_data.get("params", {}).get("name")
            arguments = request_data.get("params", {}).get("arguments", {})
            
            try:
                result = self._execute_tool(tool_name, arguments)
                return {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps(result, indent=2, default=str)
                        }
                    ]
                }
            except Exception as e:
                logger.error(f"Error executing tool {tool_name}: {str(e)}")
                return {
                    "error": {
                        "code": -32603,
                        "message": str(e)
                    }
                }
        
        else:
            return {
                "error": {
                    "code": -32601,
                    "message": f"Method not found: {method}"
                }
            }
    
    def _execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """Execute a tool with given arguments"""
        
        # Company/Account operations
        if tool_name == "search_companies_by_id":
            return self.client.search_accounts_by_id(arguments["account_id"])
        
        elif tool_name == "search_companies_by_name":
            return self.client.search_accounts_by_name(arguments["name"])
        
        elif tool_name == "search_companies_by_cnpj":
            return self.client.search_accounts_by_cnpj(arguments["cnpj"])
        
        elif tool_name == "search_companies_by_proximity":
            return self.client.search_accounts_by_proximity(
                arguments["cep"],
                arguments.get("radius_km", 50)
            )
        
        elif tool_name == "search_companies_by_employees_revenue":
            return self.client.search_accounts_by_employees_and_revenue(
                arguments.get("min_employees"),
                arguments.get("max_employees"),
                arguments.get("min_revenue"),
                arguments.get("max_revenue")
            )
        
        elif tool_name == "search_companies_by_days_without_visit":
            return self.client.search_accounts_by_days_without_visit(arguments["days"])
        
        elif tool_name == "search_companies_by_days_without_contact":
            return self.client.search_accounts_by_days_without_contact(arguments["days"])
        
        elif tool_name == "list_accounts":
            return self.client.list_accounts(arguments.get("top", 100))
        
        # Contact operations
        elif tool_name == "search_contacts_by_id":
            return self.client.search_contacts_by_id(arguments["contact_id"])
        
        elif tool_name == "search_contacts_by_name":
            return self.client.search_contacts_by_name(arguments["name"])
        
        elif tool_name == "search_contacts_by_email":
            return self.client.search_contacts_by_email(arguments["email"])
        
        # Opportunity operations
        elif tool_name == "search_opportunities_by_id":
            return self.client.search_opportunities_by_id(arguments["opportunity_id"])
        
        elif tool_name == "search_opportunities_by_name":
            return self.client.search_opportunities_by_name(arguments["name"])
        
        elif tool_name == "search_opportunities_by_account":
            return self.client.search_opportunities_by_account(arguments["account_id"])
        
        # Quote operations
        elif tool_name == "search_quotes_by_opportunity":
            return self.client.search_quotes_by_opportunity(arguments["opportunity_id"])
        
        elif tool_name == "search_quotes_by_code":
            return self.client.search_quotes_by_code(arguments["quote_number"])
        
        # Product operations
        elif tool_name == "search_products_by_opportunity":
            return self.client.search_products_by_opportunity(arguments["opportunity_id"])
        
        # Cache operations
        elif tool_name == "clear_cache":
            self.client.clear_cache()
            return {"status": "success", "message": "Cache cleared successfully"}
        
        elif tool_name == "get_cache_stats":
            return self.client.get_cache_stats()
        
        else:
            raise ValueError(f"Unknown tool: {tool_name}")
