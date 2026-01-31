"""
Example script demonstrating how to use the MCP Dataverse server
"""
import requests
import json
from typing import Dict, Any


class MCPDataverseClient:
    """Client for interacting with MCP Dataverse server"""
    
    def __init__(self, base_url: str):
        """
        Initialize the client
        
        Args:
            base_url: Base URL of the Azure Function (e.g., https://your-app.azurewebsites.net/api/mcp)
        """
        self.base_url = base_url.rstrip("/")
        self.request_id = 0
    
    def _make_request(self, method: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Make a JSON-RPC request to the MCP server"""
        self.request_id += 1
        
        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "id": self.request_id
        }
        
        if params:
            payload["params"] = params
        
        response = requests.post(
            self.base_url,
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        
        return response.json()
    
    def list_tools(self) -> Dict[str, Any]:
        """List all available tools"""
        return self._make_request("tools/list")
    
    def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Call a specific tool with arguments"""
        return self._make_request(
            "tools/call",
            params={
                "name": tool_name,
                "arguments": arguments
            }
        )


def main():
    """Example usage of the MCP Dataverse client"""
    
    # Initialize client (replace with your Azure Function URL)
    client = MCPDataverseClient("http://localhost:7071/api/mcp")
    
    print("=" * 80)
    print("MCP Dataverse Client - Examples")
    print("=" * 80)
    
    # Example 1: List all available tools
    print("\n1. Listing all available tools:")
    print("-" * 80)
    try:
        tools_response = client.list_tools()
        tools = tools_response.get("result", {}).get("tools", [])
        print(f"Found {len(tools)} tools:")
        for tool in tools:
            print(f"  - {tool['name']}: {tool['description']}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 2: Search companies by name
    print("\n2. Searching companies by name 'Contoso':")
    print("-" * 80)
    try:
        result = client.call_tool(
            "search_companies_by_name",
            {"name": "Contoso"}
        )
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 3: Search contacts by email
    print("\n3. Searching contacts by email:")
    print("-" * 80)
    try:
        result = client.call_tool(
            "search_contacts_by_email",
            {"email": "john@example.com"}
        )
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 4: Search companies by CNPJ
    print("\n4. Searching companies by CNPJ:")
    print("-" * 80)
    try:
        result = client.call_tool(
            "search_companies_by_cnpj",
            {"cnpj": "12.345.678/0001-90"}
        )
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 5: Search companies by employees and revenue
    print("\n5. Searching companies with 50-500 employees:")
    print("-" * 80)
    try:
        result = client.call_tool(
            "search_companies_by_employees_revenue",
            {
                "min_employees": 50,
                "max_employees": 500
            }
        )
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 6: Search companies by days without visit
    print("\n6. Searching companies without visit in last 30 days:")
    print("-" * 80)
    try:
        result = client.call_tool(
            "search_companies_by_days_without_visit",
            {"days": 30}
        )
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 7: List all accounts
    print("\n7. Listing top 5 accounts:")
    print("-" * 80)
    try:
        result = client.call_tool(
            "list_accounts",
            {"top": 5}
        )
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 8: Search opportunities by account
    print("\n8. Searching opportunities for a specific account:")
    print("-" * 80)
    try:
        # Replace with actual account ID
        account_id = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
        result = client.call_tool(
            "search_opportunities_by_account",
            {"account_id": account_id}
        )
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 9: Search quotes by opportunity
    print("\n9. Searching quotes for a specific opportunity:")
    print("-" * 80)
    try:
        # Replace with actual opportunity ID
        opportunity_id = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
        result = client.call_tool(
            "search_quotes_by_opportunity",
            {"opportunity_id": opportunity_id}
        )
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 10: Search products from opportunity
    print("\n10. Searching products from an opportunity:")
    print("-" * 80)
    try:
        # Replace with actual opportunity ID
        opportunity_id = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
        result = client.call_tool(
            "search_products_by_opportunity",
            {"opportunity_id": opportunity_id}
        )
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n" + "=" * 80)
    print("Examples completed!")
    print("=" * 80)


if __name__ == "__main__":
    main()
