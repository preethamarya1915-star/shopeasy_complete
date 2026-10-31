
from django.core.management.base import BaseCommand
from store.models import Product


PRODUCTS = [
    ("Wireless Headphones", "Premium wireless headphones", "Electronics", 1499, "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=700", 20),
    ("Smart Watch", "Smart watch with fitness tracking", "Electronics", 1999, "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=700", 15),
    ("Bluetooth Speaker", "Portable Bluetooth speaker", "Electronics", 1299, "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=700", 18),
    ("Laptop Backpack", "Durable laptop backpack", "Fashion", 999, "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=700", 25),
    ("Classic T-Shirt", "Comfortable cotton T-shirt", "Fashion", 599, "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=700", 30),
    ("Running Shoes", "Lightweight running shoes", "Sports", 2499, "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=700", 12),
    ("Yoga Mat", "Non-slip exercise mat", "Sports", 799, "https://images.unsplash.com/photo-1592432678016-e910b452f9a2?w=700", 20),
    ("Classic Novel", "Paperback novel", "Books", 299, "https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=700", 40),
    ("Desk Lamp", "Modern adjustable desk lamp", "Home", 799, "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=700", 14),
    ("Coffee Mug", "Ceramic coffee mug", "Home", 249, "https://images.unsplash.com/photo-1514228742587-6b1558f14893?w=700", 35),
    ("Face Wash", "Gentle daily face cleanser", "Beauty", 249, "https://images.unsplash.com/photo-1556229010-6c3f2c9ca5f8?w=700", 22),
    ("Sunglasses", "Classic everyday sunglasses", "Fashion", 899, "https://images.unsplash.com/photo-1511499767150-a48a237f0083?w=700", 16),
    ("Wireless Mouse", "Ergonomic wireless mouse", "Electronics", 699, "https://images.unsplash.com/photo-1527814050087-3793815479db?w=700", 20),
    ("Water Bottle", "Reusable steel water bottle", "Sports", 499, "https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=700", 28),
    ("Cushion Cover", "Decorative cushion cover", "Home", 349, "https://images.unsplash.com/photo-1584100936595-c0654b55a2e2?w=700", 24),
    ("Moisturizer", "Daily moisturizing lotion", "Beauty", 399, "https://images.unsplash.com/photo-1601612628452-9e99ced43524?w=700", 18),
    ("Football", "Football for practice", "Sports", 899, "https://images.unsplash.com/photo-1614632537423-1e6c2e7e0c5b?w=700", 10),
    ("Study Table Organizer", "Desk organizer for stationery", "Home", 449, "https://images.unsplash.com/photo-1499951360447-b19be8fe80f5?w=700", 15),
]


class Command(BaseCommand):
    help = "Add sample products to ShopEasy"

    def handle(self, *args, **kwargs):
        for name, description, category, price, image, stock in PRODUCTS:
            Product.objects.update_or_create(
                name=name,
                defaults={
                    "description": description,
                    "category": category,
                    "price": price,
                    "image_url": image,
                    "stock": stock,
                }
            )

        self.stdout.write(
            self.style.SUCCESS("18 sample products added successfully!")
        )
