"""
Shopify Integration - Connect to Shopify stores and sync data
"""

import shopify
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from loguru import logger

from database.models import Integration, Campaign, CampaignAnalytics
from utils.config import settings


class ShopifyClient:
    """Shopify API client wrapper"""
    
    def __init__(self, shop_domain: str, access_token: str):
        self.shop_domain = shop_domain
        self.access_token = access_token
        self.shop_url = f"https://{shop_domain}"
        self._activate_session()
    
    def _activate_session(self):
        """Activate Shopify session"""
        shopify.ShopifyResource.set_site(self.shop_url)
        shopify.ShopifyResource.activate_session(
            shopify.Session(self.shop_url, settings.SHOPIFY_API_KEY, self.access_token)
        )
    
    def test_connection(self) -> bool:
        """Test Shopify API connection"""
        try:
            shop = shopify.Shop.current()
            return shop is not None
        except Exception as e:
            logger.error(f"Shopify connection test failed: {e}")
            return False
    
    def get_shop_info(self) -> Dict[str, Any]:
        """Get shop information"""
        try:
            shop = shopify.Shop.current()
            return {
                "id": shop.id,
                "name": shop.name,
                "email": shop.email,
                "domain": shop.domain,
                "currency": shop.currency,
                "timezone": shop.timezone,
                "plan_name": shop.plan_name,
                "created_at": shop.created_at
            }
        except Exception as e:
            logger.error(f"Error fetching shop info: {e}")
            return {}
    
    def get_products(self, limit: int = 250) -> List[Dict[str, Any]]:
        """Get products from Shopify"""
        try:
            products = shopify.Product.find(limit=limit)
            return [
                {
                    "id": p.id,
                    "title": p.title,
                    "handle": p.handle,
                    "vendor": p.vendor,
                    "product_type": p.product_type,
                    "tags": p.tags,
                    "variants": [
                        {
                            "id": v.id,
                            "title": v.title,
                            "price": float(v.price),
                            "inventory_quantity": v.inventory_quantity,
                            "sku": v.sku
                        }
                        for v in p.variants
                    ],
                    "images": [img.src for img in p.images] if p.images else [],
                    "created_at": p.created_at,
                    "updated_at": p.updated_at
                }
                for p in products
            ]
        except Exception as e:
            logger.error(f"Error fetching products: {e}")
            return []
    
    def get_orders(self, start_date: Optional[datetime] = None, limit: int = 250) -> List[Dict[str, Any]]:
        """Get orders from Shopify"""
        try:
            params = {"limit": limit, "status": "any"}
            if start_date:
                params["created_at_min"] = start_date.isoformat()
            
            orders = shopify.Order.find(**params)
            return [
                {
                    "id": o.id,
                    "order_number": o.order_number,
                    "email": o.email,
                    "created_at": o.created_at,
                    "updated_at": o.updated_at,
                    "total_price": float(o.total_price),
                    "subtotal_price": float(o.subtotal_price) if o.subtotal_price else 0,
                    "total_tax": float(o.total_tax) if o.total_tax else 0,
                    "currency": o.currency,
                    "financial_status": o.financial_status,
                    "fulfillment_status": o.fulfillment_status,
                    "line_items_count": len(o.line_items) if o.line_items else 0,
                    "customer": {
                        "id": o.customer.id if o.customer else None,
                        "email": o.customer.email if o.customer else None,
                        "first_name": o.customer.first_name if o.customer else None,
                        "last_name": o.customer.last_name if o.customer else None
                    } if o.customer else None,
                    "line_items": [
                        {
                            "id": item.id,
                            "product_id": item.product_id,
                            "variant_id": item.variant_id,
                            "title": item.title,
                            "quantity": item.quantity,
                            "price": float(item.price)
                        }
                        for item in o.line_items
                    ] if o.line_items else []
                }
                for o in orders
            ]
        except Exception as e:
            logger.error(f"Error fetching orders: {e}")
            return []
    
    def get_customers(self, limit: int = 250) -> List[Dict[str, Any]]:
        """Get customers from Shopify"""
        try:
            customers = shopify.Customer.find(limit=limit)
            return [
                {
                    "id": c.id,
                    "email": c.email,
                    "first_name": c.first_name,
                    "last_name": c.last_name,
                    "orders_count": c.orders_count,
                    "total_spent": float(c.total_spent) if c.total_spent else 0,
                    "created_at": c.created_at,
                    "updated_at": c.updated_at
                }
                for c in customers
            ]
        except Exception as e:
            logger.error(f"Error fetching customers: {e}")
            return []
    
    def get_analytics_data(self, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """Get analytics data for date range"""
        try:
            orders = self.get_orders(start_date=start_date)
            
            # Filter orders by date range
            filtered_orders = [
                o for o in orders 
                if start_date <= datetime.fromisoformat(o["created_at"].replace("Z", "+00:00")) <= end_date
            ]
            
            # Calculate metrics
            total_revenue = sum(float(o["total_price"]) for o in filtered_orders)
            total_orders = len(filtered_orders)
            total_items = sum(o["line_items_count"] for o in filtered_orders)
            
            average_order_value = total_revenue / total_orders if total_orders > 0 else 0
            
            return {
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
                "total_revenue": total_revenue,
                "total_orders": total_orders,
                "total_items": total_items,
                "average_order_value": average_order_value,
                "orders": filtered_orders
            }
        except Exception as e:
            logger.error(f"Error fetching analytics: {e}")
            return {}
    
    def create_product(self, product_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a new product in Shopify"""
        try:
            product = shopify.Product()
            product.title = product_data.get("title")
            product.body_html = product_data.get("description", "")
            product.vendor = product_data.get("vendor", "")
            product.product_type = product_data.get("product_type", "")
            product.tags = product_data.get("tags", [])
            
            # Add variants
            if "variants" in product_data:
                product.variants = [
                    shopify.Variant(
                        price=v.get("price"),
                        sku=v.get("sku", ""),
                        inventory_quantity=v.get("inventory_quantity", 0)
                    )
                    for v in product_data["variants"]
                ]
            
            success = product.save()
            if success:
                return {"id": product.id, "title": product.title}
            return None
        except Exception as e:
            logger.error(f"Error creating product: {e}")
            return None
    
    def close(self):
        """Close Shopify session"""
        shopify.ShopifyResource.clear_session()


async def sync_shopify_data(integration_id: int, db: Session) -> bool:
    """Sync data from Shopify store"""
    try:
        # Get integration details
        integration = db.query(Integration).filter(Integration.id == integration_id).first()
        if not integration or integration.platform != "shopify":
            logger.error(f"Invalid integration: {integration_id}")
            return False
        
        # Initialize Shopify client
        client = ShopifyClient(
            shop_domain=integration.shop_domain,
            access_token=integration.access_token
        )
        
        # Test connection
        if not client.test_connection():
            integration.status = "error"
            integration.sync_errors = {"error": "Connection failed"}
            db.commit()
            return False
        
        # Fetch data
        logger.info(f"Syncing Shopify data for integration {integration_id}")
        
        products = client.get_products()
        orders = client.get_orders(start_date=datetime.now() - timedelta(days=30))
        customers = client.get_customers()
        
        # Update integration settings with latest data
        integration.settings = {
            "products_count": len(products),
            "orders_count": len(orders),
            "customers_count": len(customers),
            "last_sync_at": datetime.utcnow().isoformat()
        }
        integration.last_sync = datetime.utcnow()
        integration.sync_status = "success"
        integration.status = "connected"
        
        db.commit()
        
        logger.info(f"Shopify sync completed: {len(products)} products, {len(orders)} orders")
        
        client.close()
        return True
        
    except Exception as e:
        logger.error(f"Error syncing Shopify data: {e}")
        if integration:
            integration.sync_status = "error"
            integration.sync_errors = {"error": str(e)}
            db.commit()
        return False


def calculate_shopify_roas(orders: List[Dict[str, Any]], ad_spend: float) -> float:
    """Calculate ROAS from Shopify orders"""
    total_revenue = sum(float(o["total_price"]) for o in orders)
    if ad_spend > 0:
        return total_revenue / ad_spend
    return 0.0
