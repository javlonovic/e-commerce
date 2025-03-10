# store/management/commands/init_sample_data.py

import os
import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.core.files import File
from django.utils.text import slugify
from store.models import Category, Product, ProductImage

class Command(BaseCommand):
    help = 'Initialize sample data for the e-commerce store'
    
    def handle(self, *args, **kwargs):
        self.stdout.write('Creating sample data...')
        
        # Create superuser if it doesn't exist
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin')
            self.stdout.write(self.style.SUCCESS('Superuser created'))
        
        # Create categories
        categories = [
            {
                'name': 'Electronics',
                'description': 'Electronic devices and gadgets for everyday use',
            },
            {
                'name': 'Clothing',
                'description': 'Fashion items for men, women and children',
            },
            {
                'name': 'Books',
                'description': 'Physical and digital books across various genres',
            },
            {
                'name': 'Home & Kitchen',
                'description': 'Products for your home and kitchen appliances',
            },
            {
                'name': 'Sports & Outdoors',
                'description': 'Equipment and accessories for sports and outdoor activities',
            }
        ]
        
        created_categories = []
        for cat_data in categories:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'description': cat_data['description'],
                    'slug': slugify(cat_data['name'])
                }
            )
            created_categories.append(category)
            if created:
                self.stdout.write(f'Created category: {category.name}')
            else:
                self.stdout.write(f'Category exists: {category.name}')
        
        # Sample products for each category
        products_data = {
            'Electronics': [
                {
                    'name': 'Smartphone Pro X',
                    'price': 999.99,
                    'quantity': 50,
                    'description': 'Latest smartphone with advanced features and long battery life.'
                },
                {
                    'name': 'Wireless Earbuds',
                    'price': 129.99,
                    'quantity': 100,
                    'description': 'High-quality wireless earbuds with noise cancellation.'
                },
                {
                    'name': 'Smart Watch',
                    'price': 249.99,
                    'quantity': 30,
                    'description': 'Track your fitness and stay connected with this smart watch.'
                }
            ],
            'Clothing': [
                {
                    'name': 'Cotton T-Shirt',
                    'price': 19.99,
                    'quantity': 200,
                    'description': 'Comfortable cotton t-shirt for everyday wear.'
                },
                {
                    'name': 'Denim Jeans',
                    'price': 49.99,
                    'quantity': 150,
                    'description': 'Classic denim jeans with modern fit.'
                },
                {
                    'name': 'Winter Jacket',
                    'price': 79.99,
                    'quantity': 75,
                    'description': 'Warm winter jacket with water-resistant exterior.'
                }
            ],
            'Books': [
                {
                    'name': 'Python Programming',
                    'price': 34.99,
                    'quantity': 60,
                    'description': 'Comprehensive guide to Python programming for beginners and intermediates.'
                },
                {
                    'name': 'Science Fiction Anthology',
                    'price': 24.99,
                    'quantity': 40,
                    'description': 'Collection of the best science fiction short stories.'
                },
                {
                    'name': 'Cookbook: International Cuisine',
                    'price': 29.99,
                    'quantity': 25,
                    'description': 'Recipes from around the world for the home chef.'
                }
            ],
            'Home & Kitchen': [
                {
                    'name': 'Coffee Maker',
                    'price': 89.99,
                    'quantity': 45,
                    'description': 'Programmable coffee maker for the perfect brew every morning.'
                },
                {
                    'name': 'Knife Set',
                    'price': 69.99,
                    'quantity': 30,
                    'description': 'Professional grade knife set for your kitchen.'
                },
                {
                    'name': 'Bedding Set',
                    'price': 59.99,
                    'quantity': 60,
                    'description': 'Comfortable bedding set with duvet cover and pillowcases.'
                }
            ],
            'Sports & Outdoors': [
                {
                    'name': 'Yoga Mat',
                    'price': 29.99,
                    'quantity': 100,
                    'description': 'Non-slip yoga mat for your practice.'
                },
                {
                    'name': 'Hiking Backpack',
                    'price': 79.99,
                    'quantity': 40,
                    'description': 'Durable hiking backpack with multiple compartments.'
                },
                {
                    'name': 'Tennis Racket',
                    'price': 59.99,
                    'quantity': 25,
                    'description': 'Professional tennis racket for players of all levels.'
                }
            ]
        }
        
        # Create products
        for category in created_categories:
            category_products = products_data.get(category.name, [])
            
            for product_data in category_products:
                product, created = Product.objects.get_or_create(
                    name=product_data['name'],
                    defaults={
                        'category': category,
                        'slug': slugify(product_data['name']),
                        'price': product_data['price'],
                        'quantity': product_data['quantity'],
                        'description': product_data['description']
                    }
                )
                
                if created:
                    self.stdout.write(f'Created product: {product.name}')
                    for i in range(2):  # Create 2 dummy images per product
                        ProductImage.objects.create(
                            product=product,
                            is_primary=(i == 0)  
                        )
                else:
                    self.stdout.write(f'Product exists: {product.name}')
        
        self.stdout.write(self.style.SUCCESS('Sample data initialization complete!'))