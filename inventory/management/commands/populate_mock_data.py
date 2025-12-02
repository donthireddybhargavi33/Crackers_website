import os
import random
from django.core.management.base import BaseCommand
from django.conf import settings
from inventory.models import Category, Product
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
import requests

class Command(BaseCommand):
    help = 'Populate database with mock data'

    def create_mock_image(self, category_name, index):
        # Use placeholder images from Lorem Picsum
        width = 800
        height = 600
        img_url = f'https://picsum.photos/{width}/{height}?random={index}'
        
        try:
            # Download the image
            response = requests.get(img_url)
            if response.status_code == 200:
                # Create the media directory if it doesn't exist
                media_dir = os.path.join(settings.MEDIA_ROOT, 'products')
                os.makedirs(media_dir, exist_ok=True)
                
                # Create filename
                filename = f"{category_name.lower().replace(' ', '_')}_{index}.jpg"
                file_path = os.path.join(media_dir, filename)
                
                # Save the image directly to the media directory
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                
                # Return the relative path for the model
                return f'products/{filename}'
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'Failed to create image: {str(e)}'))
            return None

    def handle(self, *args, **kwargs):
        # Complete product catalog with all categories and products in order
        products_data = [
            ("Sparklers", [
                {"name": "10 CM ELECTRIC SPARKLER", "content": "1 BOX", "price": 55},
                {"name": "10 CM COLOUR SPARKLER", "content": "1 BOX", "price": 65},
                {"name": "10 CM GREEN SPARKLERS", "content": "1 BOX", "price": 75},
                {"name": "12 CM ELECTRIC SPARKLERS", "content": "1 BOX", "price": 90},
                {"name": "12 CM COLOUR SPARKLERS", "content": "1 BOX", "price": 105},
                {"name": "12 CM GREEN SPARKLER", "content": "1 BOX", "price": 110},
                {"name": "15 CM ELECTRIC SPARKLERS", "content": "1 BOX", "price": 150},
                {"name": "15 CM COLOUR SPARKLER", "content": "1 BOX", "price": 160},
                {"name": "15 CM GREEN SPARKLER", "content": "1 BOX", "price": 170},
                {"name": "30 CM ELECTRIC SPARKLER", "content": "1 BOX", "price": 150},
                {"name": "30 CM COLOUR SPARKLER", "content": "1 BOX", "price": 160},
                {"name": "30 CM GREEN SPARKLER", "content": "1 BOX", "price": 170},
                {"name": "50 CM ELECTRIC SPARKLER", "content": "1 BOX", "price": 750},
                {"name": "50 CM COLOUR SPARKLERS", "content": "1 BOX", "price": 800},
                {"name": "ROTATE SPARKLERS", "content": "1 BOX", "price": 800},
            ]),
            ("Flower Pots", [
                {"name": "FLOWER POT BIG (10 PCS)", "content": "1 BOX", "price": 300},
                {"name": "FLOWER POTS SPECIAL (10 PCS)", "content": "1 BOX", "price": 425},
                {"name": "FLOWER POTS ASHOKA (10 PCS)", "content": "1 BOX", "price": 500},
                {"name": "COLOUR KOTI (10 PCS)", "content": "1 BOX", "price": 850},
                {"name": "TRI COLOUR FOUNTAIN (5 PCS)", "content": "1 BOX", "price": 1150},
                {"name": "FLOWER POTS DELUXE (5 PCS)", "content": "1 BOX", "price": 875},
                {"name": "5 IN ONE FUNCTIONS (1 PCS)", "content": "1 BOX", "price": 1750},
                {"name": "PANCHANGARA (5 PCS)", "content": "1 BOX", "price": 500},
            ]),
            ("Chakkar", [
                {"name": "CHAKKAR BIG (10 PCS)", "content": "1 BOX", "price": 150},
                {"name": "GROUND CHAKKAR SPECIAL (10 PCS)", "content": "1 BOX", "price": 310},
                {"name": "GROUND CHAKKAR DELUXE (10 PCS)", "content": "1 BOX", "price": 450},
                {"name": "SPINNER CHAKKAR PLASTIC (10 PCS)", "content": "1 BOX", "price": 600},
                {"name": "DISCO WHEEL (10 PCS)", "content": "1 BOX", "price": 840},
                {"name": "WIRE CHAKKAR SPECIAL (10 PCS)", "content": "1 BOX", "price": 800},
            ]),
            ("Bijili", [
                {"name": "RED BIJILI (100 PCS)", "content": "1 PKT", "price": 130},
                {"name": "VARI BIJILI (100 PCS)", "content": "1 PKT", "price": 160},
            ]),
            ("Enjoy Pencil", [
                {"name": "ULTRA PENCIL (3 PCS)", "content": "1 BOX", "price": 350},
                {"name": "POPCORN PENCIL (2 PCS)", "content": "1 BOX", "price": 840},
                {"name": "MAGIC LIGHT, FIRE LIGHT (3 PCS)", "content": "1 BOX", "price": 750},
            ]),
            ("One Sound Crackers", [
                {"name": "2 3/4' KURUVI CRACKERS", "content": "1 PKT", "price": 30},
                {"name": "4' LAKSHMI CRACKERS", "content": "1 PKT", "price": 100},
                {"name": "4' LAKSHMI GOLD CRACKERS", "content": "1 PKT", "price": 140},
                {"name": "5' MEGA DELUXE(12 PLY)", "content": "1 PKT", "price": 225},
            ]),
            ("Rocket Bombs", [
                {"name": "ROCKET BOMB (10 PCS)", "content": "1 BOX", "price": 240},
                {"name": "TWO SOUND ROCKET(10 PCS)", "content": "1 BOX", "price": 475},
                {"name": "LUNIK ROCKET(10 PCS)", "content": "1 BOX", "price": 450},
                {"name": "WHISTLING ROCKET (10 PCS)", "content": "1 BOX", "price": 800},
            ]),
            ("Bombs Items", [
                {"name": "KING OF KING BOMB GREEN (10 PCS)", "content": "1 BOX", "price": 450},
                {"name": "CLASSIC BOMB (10 PCS)", "content": "1 BOX", "price": 500},
            ]),
            ("Giant & Deluxe", [
                {"name": "28 GIANT CRACKERS", "content": "1 PKT", "price": 125},
                {"name": "56 GIANT CRACKERS", "content": "1 PKT", "price": 250},
                {"name": "24 DELUXE CRACKERS", "content": "1 PKT", "price": 250},
                {"name": "50 DELUXE CRACKERS", "content": "1 PKT", "price": 500},
                {"name": "100 DELUXE CRACKERS", "content": "1 PKT", "price": 1000},
            ]),
            ("Baby Fancy Novelties", [
                {"name": "KIT KAT (10 PCS)", "content": "1 BOX", "price": 200},
            ]),
            ("Peacock Varieties", [
                {"name": "PEACOCK FEATHER (5 PCS)", "content": "1 BOX", "price": 525},
                {"name": "LITTLE PEACOCK (1 PCS)", "content": "1 BOX", "price": 500},
                {"name": "MAGIC PEACOCK (1 PCS)", "content": "1 BOX", "price": 700},
                {"name": "BADA PEACOCK 5 FEATHER (1 PCS)", "content": "1 BOX", "price": 2250},
            ]),
            ("Mega Shower", [
                {"name": "TIN FOUNTAIN (1 PCS)", "content": "1 BOX", "price": 550},
                {"name": "6'' MEGA SHOWER FOUNTAIN (1 PCS)", "content": "1 BOX", "price": 1000},
                {"name": "FUN ZONE FOUNTAIN (5 PCS)", "content": "1 BOX", "price": 1775},
            ]),
            ("Multicolour Shots (Brand)", [
                {"name": "12 SHOT FULL CRACKLING (BRAND)", "content": "1 BOX", "price": 800},
                {"name": "30 SHOT MULTICOLOUR (BRAND)", "content": "1 BOX", "price": 2000},
                {"name": "60 SHOT MULTICOLOUR (BRAND)", "content": "1 BOX", "price": 4000},
                {"name": "120 SHOT MULTICOLOUR (BRAND)", "content": "1 BOX", "price": 8000},
                {"name": "240 SHOT MULTICOLOUR (BRAND)", "content": "1 BOX", "price": 16000},
            ]),
            ("Multicolour Shot", [
                {"name": "30 SHOT MULTI COLOUR (OTHER)", "content": "1 BOX", "price": 1800},
                {"name": "60 SHOT MULTI COLOUR (OTHER)", "content": "1 BOX", "price": 3600},
                {"name": "120 SHOT MULTI COLOUR (OTHER)", "content": "1 BOX", "price": 7200},
            ]),
            ("Mini Aerial Chotta Fancy", [
                {"name": "CHOTTA FANCY (1 PCS)", "content": "1 BOX", "price": 185},
                {"name": "7 SHOT (5 PCS)", "content": "1 BOX", "price": 550},
            ]),
            ("Mega Display Series", [
                {"name": "2'' AERIAL FANCY(1 PCS)", "content": "1 BOX", "price": 350},
                {"name": "2 1/2 '' AERIAL FANCY (1 PCS)", "content": "1 BOX", "price": 630},
                {"name": "2 1/2'' AERIAL FANCY(3 PCS) (BRAND)", "content": "1 BOX", "price": 1100},
                {"name": "3 1/2 '' AERIAL FANCY(1 PCS)", "content": "1 BOX", "price": 1150},
                {"name": "4 '' NAYAGARA BALLS (1 PCS)", "content": "1 BOX", "price": 1500},
                {"name": "4'' AERIAL FANCY (1 PCS)", "content": "1 BOX", "price": 1475},
                {"name": "4'' AERIAL FANCY 7 STEP (1 PCS)", "content": "1 BOX", "price": 1550},
                {"name": "4'' AERIAL FANCY DOUBLE BALL (1 PCS)", "content": "1 BOX", "price": 2150},
                {"name": "6'' AERIAL FANCY (2 PCS)", "content": "1 BOX", "price": 4100},
                {"name": "3 1/2'' AERIAL FANCY (3 PCS)", "content": "1 BOX", "price": 4200},
                {"name": "4 1/2 '' AERIAL FANCY WOW BLUE (1 PCS)", "content": "1 BOX", "price": 2000},
                {"name": "3 1/2'' AERIAL FANCY GUN OUT", "content": "1 BOX", "price": 1150},
                {"name": "2 1/2 '' DANCING SHOOTER (1 PCS)", "content": "1 BOX", "price": 1200},
            ]),
            ("Colour Fountain Big", [
                {"name": "COLOUR RAIN (5 PCS)", "content": "5 BOX", "price": 475},
                {"name": "GOLDEN GLOBE (5 PCS)", "content": "1 BOX", "price": 475},
                {"name": "BUTTERFLY (10 PCS)", "content": "1 BOX", "price": 475},
                {"name": "PHOTO FLASH", "content": "1 BOX", "price": 250},
                {"name": "DISCO SHOWER (5 PCS)", "content": "1 BOX", "price": 425},
                {"name": "MOON LIGHT (5 PCS)", "content": "1 BOX", "price": 375},
            ]),
            ("Mega Wonder Fountain (Window)", [
                {"name": "SING POP", "content": "1 BOX", "price": 650},
                {"name": "FOX STAR CRACKLING (1 PCS)", "content": "1 BOX", "price": 500},
                {"name": "MOON LIGHT, HIFI, GOLD STAR (5 PCS)", "content": "1 BOX", "price": 660},
                {"name": "FLY MAGIC FOUNTAIN (6 PCS)", "content": "1 BOX", "price": 625},
                {"name": "TWIX (5 COLOUR FOUNTAIN)", "content": "1 BOX", "price": 650},
                {"name": "TEDDY FOUNTAIN (1 PCS)", "content": "1 BOX", "price": 235},
                {"name": "CRACKLING TIN FOUNTAIN (2 PCS)", "content": "1 BOX", "price": 1050},
            ]),
            ("Colour Smoke", [
                {"name": "RAINBOW COLOUR SMOKE (3 PCS)", "content": "1 BOX", "price": 630},
            ]),
            ("Gujarat Flower Pots", [
                {"name": "TIM TIM (5 PCS)", "content": "1 BOX", "price": 875},
                {"name": "KO KO (5 PCS)", "content": "1 BOX", "price": 900},
                {"name": "2 IN 1 (10 PCS)", "content": "1 BOX", "price": 1750},
                {"name": "COLOUR CHANGING (5 PCS)", "content": "1 BOX", "price": 1700},
            ]),
            ("Naatu Vedi", [
                {"name": "1/4 JOKER PAPER BOMB (1 PCS)", "content": "1 BOX", "price": 225},
                {"name": "1/2 KG PAPER BOMB(1 PCS)", "content": "1 BOX", "price": 450},
                {"name": "1 KG PAPER BOMB (1 PCS)", "content": "1 BOX", "price": 900},
                {"name": "MONEY BANK (3PCS)", "content": "1 BOX", "price": 500},
            ]),
            ("Matches Boxs", [
                {"name": "FLASH MATCHES (5 PCS)", "content": "1 BOX", "price": 225},
                {"name": "WONDER MATCHES(10 PCS)", "content": "1 BOX", "price": 275},
                {"name": "POKE MAN MATCHES", "content": "1 BOX", "price": 650},
                {"name": "MEGA DELUXE LAPTOP (10 PCS)", "content": "1 BOX", "price": 850},
            ]),
            ("Gun", [
                {"name": "SONY GUN SMALL", "content": "1 BOX", "price": 250},
                {"name": "SONY GUN BIG", "content": "1 PCS", "price": 350},
                {"name": "RING CAB", "content": "1 BOX", "price": 50},
                {"name": "ROLL CAP GUN SMALL", "content": "1 BOX", "price": 250},
                {"name": "ROLL CAB", "content": "1 BOX", "price": 400},
            ]),
            ("Twinkling Star", [
                {"name": "1 1/2' TWINKLING STAR", "content": "1 BOX", "price": 125},
                {"name": "4' TWINKLING STAR", "content": "1 BOX", "price": 275},
            ]),
            ("New Fancy", [
                {"name": "2 1/2 ' AERIAL FANCY (1 PCS)", "content": "1 BOX", "price": 500},
            ]),
            ("Setout", [
                {"name": "T -20 (BHARAT RATHNA)", "content": "1 BOX", "price": 12500},
                {"name": "10 * 10 SHOT CELEBRATION", "content": "1 BOX", "price": 18000},
            ]),
            ("Spinner", [
                {"name": "BAMBARAM (10 PCS)", "content": "1 BOX", "price": 475},
                {"name": "HELICOPTOR (5 PCS)", "content": "1 BOX", "price": 375},
                {"name": "DRONE (5 PCS)", "content": "1 BOX", "price": 650},
            ]),
            ("New Varieties 2025", [
                {"name": "SIREN (3 PCS)", "content": "1 BOX", "price": 725},
                {"name": "SELFI STICK (5 PCS)", "content": "1 BOX", "price": 500},
                {"name": "LOLLIPOP (5 PCS)", "content": "1 BOX", "price": 750},
                {"name": "GUITAR (1 PCS)", "content": "1 BOX", "price": 1050},
                {"name": "CYCLINDER BOMB (1 PCS)", "content": "1 PCS", "price": 1000},
                {"name": "CAR (1 PCS)", "content": "1 BOX", "price": 800},
                {"name": "APPLE, ORANGE, PINEAPPLE, STRAWBERRY, PUMPKIN (1 PCS)", "content": "1 BOX", "price": 1000},
            ]),
            ("Family Pack", [
                {"name": "3000 FAMILY PACK", "content": "1 BOX", "price": 17500},
                {"name": "5000 FAMILY PACK", "content": "1 BOX", "price": 27500},
            ]),
            ("G (Other)", [
                {"name": "1 G (OTHER)", "content": "1 BOX", "price": 625},
                {"name": "2 G (OTHER)", "content": "1 BOX", "price": 1250},
                {"name": "5 G (OTHER)", "content": "1 BOX", "price": 3125},
            ]),
            ("G (Brand)", [
                {"name": "5 G (BRAND)", "content": "1 BOX", "price": 6250},
            ]),
            ("Crackling Fountain", [
                {"name": "STAR SHOW CRACKLING, POP FUN, GREEN CITY, RED MELA (1 PCS)", "content": "1 BOX", "price": 650},
            ]),
            ("Gift Box 2025", [
                {"name": "20 ITEM GIFT BOX", "content": "1 BOX", "price": 1250},
                {"name": "25 ITEM GIFT BOX", "content": "1 BOX", "price": 1750},
                {"name": "30 ITEM GIFT BOX", "content": "1 BOX", "price": 2250},
                {"name": "35 ITEM GIFT BOX", "content": "1 BOX", "price": 2750},
            ]),
        ]

        self.stdout.write('Deleting existing categories and products...')
        
        # Delete all existing products and categories
        Product.objects.all().delete()
        Category.objects.all().delete()
        
        self.stdout.write(self.style.SUCCESS('Deleted all existing data'))
        self.stdout.write('Creating categories and products...')

        for order, (category_name, products_list) in enumerate(products_data, start=1):
            # Create or get category
            category, created = Category.objects.get_or_create(
                name=category_name,
                defaults={
                    "description": f"Premium {category_name} collection for Diwali celebrations",
                    "order": order
                }
            )
            
            if created:
                self.stdout.write(f'Created category: {category_name} (Order: {order})')
            
            # Create products for this category
            for idx, product_info in enumerate(products_list):
                product_name = product_info["name"]
                content = product_info["content"]
                actual_price = product_info["price"]
                
                # Create product with actual price from data
                product, created = Product.objects.get_or_create(
                    name=product_name,
                    category=category,
                    defaults={
                        "price": actual_price,
                        "stock_quantity": random.randint(10, 100),
                        "description": f"{product_name} - {content}. Perfect for Diwali celebrations.",
                        "is_active": True
                    }
                )
                
                if created:
                    # Add image to product
                    image_path = self.create_mock_image(category_name, idx)
                    if image_path:
                        product.image = image_path
                        product.save()
                    self.stdout.write(f'Created product: {product_name} - ₹{actual_price}')

        self.stdout.write(self.style.SUCCESS('Successfully created mock data with all products and categories in order!'))