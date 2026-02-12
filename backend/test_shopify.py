"""
Test Shopify Connection and Fetch Data
Run this after connecting your store to see what data is available
"""

from database.connection import SessionLocal
from database.models import Integration
from integrations.shopify_integration import ShopifyClient
import json

def test_shopify_connection():
    """Test Shopify connection and fetch data"""
    db = SessionLocal()
    
    try:
        # Get Shopify integration
        shopify = db.query(Integration).filter(
            Integration.platform == "shopify"
        ).first()
        
        if not shopify:
            print("❌ No Shopify integration found!")
            print("\nPlease connect your store first:")
            print("1. Go to http://localhost:3000/integrations")
            print("2. Click 'Connect Shopify'")
            print("3. Enter your store domain")
            print("4. Approve the connection")
            return
        
        print("✓ Shopify integration found!")
        print(f"  Store: {shopify.shop_domain}")
        print(f"  Status: {shopify.status}")
        print(f"  Connected: {shopify.created_at}")
        print()
        
        # Create Shopify client
        client = ShopifyClient(
            shop_domain=shopify.shop_domain,
            access_token=shopify.access_token
        )
        
        print("=" * 60)
        print("FETCHING SHOPIFY DATA...")
        print("=" * 60)
        print()
        
        # Test 1: Get Shop Info
        print("1. Shop Information:")
        shop_info = client.get_shop_info()
        if shop_info:
            print(f"   ✓ Shop Name: {shop_info.get('name', 'N/A')}")
            print(f"   ✓ Email: {shop_info.get('email', 'N/A')}")
            print(f"   ✓ Domain: {shop_info.get('domain', 'N/A')}")
            print(f"   ✓ Currency: {shop_info.get('currency', 'N/A')}")
        else:
            print("   ✗ Could not fetch shop info")
        print()
        
        # Test 2: Get Products
        print("2. Products:")
        products = client.get_products(limit=5)
        if products:
            print(f"   ✓ Found {len(products)} products")
            for p in products[:3]:
                print(f"      - {p.get('title', 'Unknown')} (${p.get('variants', [{}])[0].get('price', '0')})")
        else:
            print("   ✗ No products found")
            print("   → Add products in Shopify Admin to see them here")
        print()
        
        # Test 3: Get Orders
        print("3. Orders:")
        orders = client.get_orders(limit=5)
        if orders:
            print(f"   ✓ Found {len(orders)} orders")
            for o in orders[:3]:
                print(f"      - Order #{o.get('order_number', 'N/A')} - ${o.get('total_price', '0')}")
        else:
            print("   ✗ No orders found")
            print("   → Create test orders in Shopify Admin to see them here")
        print()
        
        # Test 4: Get Customers
        print("4. Customers:")
        customers = client.get_customers(limit=5)
        if customers:
            print(f"   ✓ Found {len(customers)} customers")
            for c in customers[:3]:
                print(f"      - {c.get('email', 'Unknown')} ({c.get('orders_count', 0)} orders)")
        else:
            print("   ✗ No customers found")
            print("   → Customers appear after they place orders")
        print()
        
        # Summary
        print("=" * 60)
        print("SUMMARY")
        print("=" * 60)
        print()
        
        has_data = bool(products or orders or customers)
        
        if has_data:
            print("✓ Your store has data!")
            print()
            print("Next steps:")
            print("1. Go to http://localhost:3000/integrations")
            print("2. Click 'Sync Now' to import all data")
            print("3. Go to http://localhost:3000/analytics to view analytics")
        else:
            print("⚠ Your store is empty (this is normal for a new store)")
            print()
            print("To get analytics:")
            print("1. Add products in Shopify Admin")
            print("2. Create test orders")
            print("3. Come back and run this script again")
            print("4. Or click 'Sync Now' in the integrations page")
        
        print()
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    print("=" * 60)
    print("  SHOPIFY CONNECTION TEST")
    print("=" * 60)
    print()
    
    test_shopify_connection()
    
    print()
    input("Press Enter to exit...")
