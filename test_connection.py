"""
Test connection to Dataverse
Use this script to verify your Dataverse credentials and connection
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))

from dataverse_client import DataverseClient


def test_connection():
    """Test connection to Dataverse"""
    print("=" * 80)
    print("Testing Dataverse Connection")
    print("=" * 80)
    
    # Check environment variables
    print("\n1. Checking environment variables...")
    print("-" * 80)
    
    required_vars = [
        "DATAVERSE_URL",
        "DATAVERSE_CLIENT_ID",
        "DATAVERSE_CLIENT_SECRET",
        "DATAVERSE_TENANT_ID"
    ]
    
    missing_vars = []
    for var in required_vars:
        value = os.getenv(var)
        if not value:
            missing_vars.append(var)
            print(f"  ✗ {var}: NOT SET")
        else:
            # Mask sensitive values
            if "SECRET" in var:
                display_value = value[:4] + "*" * (len(value) - 4)
            else:
                display_value = value
            print(f"  ✓ {var}: {display_value}")
    
    if missing_vars:
        print(f"\n✗ Missing required environment variables: {', '.join(missing_vars)}")
        print("Please set them in your .env file or environment.")
        return False
    
    # Test OAuth token acquisition
    print("\n2. Testing OAuth authentication...")
    print("-" * 80)
    try:
        client = DataverseClient()
        token = client._get_access_token()
        print(f"  ✓ Successfully obtained access token")
        print(f"  Token (first 20 chars): {token[:20]}...")
    except Exception as e:
        print(f"  ✗ Failed to obtain access token: {str(e)}")
        return False
    
    # Test listing accounts
    print("\n3. Testing Dataverse API access...")
    print("-" * 80)
    try:
        accounts = client.list_accounts(top=5)
        print(f"  ✓ Successfully retrieved {len(accounts)} accounts")
        
        if accounts:
            print("\n  Sample accounts:")
            for i, account in enumerate(accounts, 1):
                name = account.get("name", "N/A")
                account_id = account.get("accountid", "N/A")
                print(f"    {i}. {name} (ID: {account_id})")
        else:
            print("  Note: No accounts found in the Dataverse environment")
    except Exception as e:
        print(f"  ✗ Failed to retrieve accounts: {str(e)}")
        return False
    
    # Test querying contacts
    print("\n4. Testing contact retrieval...")
    print("-" * 80)
    try:
        contacts = client._query("contacts", top=3)
        print(f"  ✓ Successfully retrieved {len(contacts)} contacts")
        
        if contacts:
            print("\n  Sample contacts:")
            for i, contact in enumerate(contacts, 1):
                name = contact.get("fullname", "N/A")
                email = contact.get("emailaddress1", "N/A")
                print(f"    {i}. {name} ({email})")
        else:
            print("  Note: No contacts found in the Dataverse environment")
    except Exception as e:
        print(f"  ✗ Failed to retrieve contacts: {str(e)}")
        return False
    
    # Test querying opportunities
    print("\n5. Testing opportunity retrieval...")
    print("-" * 80)
    try:
        opportunities = client._query("opportunities", top=3)
        print(f"  ✓ Successfully retrieved {len(opportunities)} opportunities")
        
        if opportunities:
            print("\n  Sample opportunities:")
            for i, opp in enumerate(opportunities, 1):
                name = opp.get("name", "N/A")
                value = opp.get("estimatedvalue", "N/A")
                print(f"    {i}. {name} (Value: {value})")
        else:
            print("  Note: No opportunities found in the Dataverse environment")
    except Exception as e:
        print(f"  ✗ Failed to retrieve opportunities: {str(e)}")
        return False
    
    print("\n" + "=" * 80)
    print("✓ All tests passed! Connection is working correctly.")
    print("=" * 80)
    return True


if __name__ == "__main__":
    success = test_connection()
    sys.exit(0 if success else 1)
