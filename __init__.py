"""
Azure Function HTTP Trigger for MCP Dataverse Server
"""
import azure.functions as func
import json
import logging
from mcp_server import MCPDataverseServer

# Initialize MCP server
mcp_server = MCPDataverseServer()

# Configure logging
logger = logging.getLogger(__name__)


def main(req: func.HttpRequest) -> func.HttpResponse:
    """
    Main Azure Function handler for MCP requests
    """
    logger.info('MCP Dataverse function received a request.')
    
    try:
        # Get request body
        req_body = req.get_json()
        
        # Handle MCP request
        response = mcp_server.handle_request(req_body)
        
        # Return response
        return func.HttpResponse(
            json.dumps(response, default=str),
            mimetype="application/json",
            status_code=200
        )
    
    except ValueError as e:
        logger.error(f"Invalid request body: {str(e)}")
        return func.HttpResponse(
            json.dumps({
                "error": {
                    "code": -32700,
                    "message": "Parse error: Invalid JSON"
                }
            }),
            mimetype="application/json",
            status_code=400
        )
    
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return func.HttpResponse(
            json.dumps({
                "error": {
                    "code": -32603,
                    "message": f"Internal error: {str(e)}"
                }
            }),
            mimetype="application/json",
            status_code=500
        )
