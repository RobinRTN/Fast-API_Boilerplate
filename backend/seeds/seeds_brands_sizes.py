import os
from flask import Flask
import sys

sys.path.append("..")

from extensions import db
from models import Brand, Size, MainCategory, SubCategory, Channel
from app import app

brands = [
    "Scotch and Soda",
    "Carhartt",
    "Carhartt WIP",
    "Yves Saint Laurent",
    "Fear of God",
    "Lemaire",
    "Acne Studios",
    "Arket",
    "Arc'teryx",
    "Mammut",
    "Peak Performance",
    "Levi's",
    "Levi Strauss",
    "Nike",
    "Courrèges",
    "Patagonia",
    "From Future",
    "AllSaints",
    "All Saints",
    "Dickies",
    "Dr. Martens",
    "Arte",
    "Ami Paris",
    "Encre",
    "Gildan",
    "Jerzees",
    "Fruit of the Loom",
    "Schott",
    "Hanes",
    "Tommy Hilfiger",
    "Yeezy",
    "Jack Wolfskin",
    "Nobis",
    "Maison Kitsuné",
    "Loewe",
    "Vetements",
    "Junya Watanabe",
    "Zegna",
    "Alexander McQueen",
    "Thierry Mugler",
    "Valentino",
    "Brunello Cucinelli",
    "Loro Piana",
    "Prada",
    "Fendi",
    "Bottega Veneta",
    "Parajumpers",
    "Nike ACG",
    "Pyrenex",
    "Salomon",
    "Cruel Pancake",
    "Autry",
]


def seed_data():
    # Add brands from BrandEnum
    for brand in brands:
       if not Brand.query.filter_by(name=brand).first():
           brand_entry = Brand(name=brand)
           db.session.add(brand_entry)
    
    print("Added all brands successfully")

    general_sizes = ["XS", "S", "M", "L", "XL", "XXL"]
    for size in general_sizes:
        for prefix in ["F_", "M_"]:
            size_name = f"{prefix}{size}"
            if not Size.query.filter_by(name=size_name).first():
                size_entry = Size(name=size_name)
                db.session.add(size_entry)
    
    print("Added all garment sizes successfully")

    for waist in range(23, 41):  # Waist sizes from 23 to 40
        size_name = f"W{waist}"
        if not Size.query.filter_by(name=size_name).first():
            size_entry = Size(name=size_name)
            db.session.add(size_entry)

    print("Added all pant sizes successfully")

    for shoe_size in range(33, 51):  # Shoe sizes from 33 to 50
        size_name = f"{shoe_size}"
        if not Size.query.filter_by(name=size_name).first():
            size_entry = Size(name=size_name)
            db.session.add(size_entry)
    
    print("Added all shoe sizes successfully")

    categories = {
        'boys': {
            'Vêtements': ['Manteaux et vestes', 'Costumes et blazers', 'Pantalons', 
                          'Sous-vêtements et chaussettes', 'Jeans', 'Shorts', 'Autres'],
            'Chaussures': ['Bottes', 'Baskets', 'Chaussures habillées', 'Sandales', 'Claquettes et tongs', 'Chaussures de sport'],
            'Accessoires': ['Ceintures', 'Chapeaux et casquettes', 'Lunettes de soleil', 'Montres', 'Parapluies', 'Écharpes et châles', 'Sacs à dos', 'Porte-clés'],
            'Soins': ['Soins du corps', 'Parfums', 'Accessoires']
        },
        'girls': {
            'Vêtements': ['Sweats et sweats à capuche', 'Robes', 'Jupes', 'Maillots de bain', 
                          'Hauts et t-shirts', 'Lingerie et pyjamas', 'Combinaisons et combishorts'],
            'Chaussures': ['Ballerines', 'Chaussures à talons', 'Espadrilles', 'Sandales', 'Baskets', 'Chaussures de sport'],
            'Accessoires': ['Bijoux', 'Écharpes et châles', 'Accessoires pour cheveux', 'Gants', 'Parapluies', 'Écharpes et châles', 'Sacs à dos', 'Porte-clés'],
            'Soins': ['Maquillage', 'Soins visage', 'Soins mains', 'Manucure', 'Soins cheveux']
        }
    }

    for gender, main_categories in categories.items():
        for main_cat_name, subcategories in main_categories.items():
            main_category = MainCategory.query.filter_by(name=main_cat_name).first()
            if not main_category:
                main_category = MainCategory(name=main_cat_name, gender=gender)
                db.session.add(main_category)
                db.session.commit()

            for sub_cat_name in subcategories:
                sub_category = SubCategory.query.filter_by(name=sub_cat_name)
                if not sub_category:
                    sub_category = SubCategory(name=sub_cat_name, gender=gender)
                    db.session.add(sub_category)
                    db.session.commit()

    print("Added the categories and subcategories successfully")

    channel_data = [
    {"name": "Nike - Men L/XL", "brands": ["Nike", "Nike ACG"], "sizes": ["M_L", "M_XL"], "user_id": None, "query_identifier": 1},
    {"name": "Carhartt - Men XL", "brands": ["Carhartt", "Carhartt WIP"], "sizes": ["M_XL"], "user_id": None, "query_identifier": 2},
    {"name": "Jack Wolveskin - Men L", "brands": ["Jack Wolveskin"], "sizes": ["M_L"], "user_id": None, "query_identifier": 3},
    {"name": "Arcteryx - Men L/XL", "brands": ["Arc'teryx"], "sizes": ["M_L", "M_XL"], "user_id": None, "query_identifier": 4},
    {"name": "Levis - 505", "search": "505", "brands": ["Levi's","Levi Strauss"], "sizes": ["W33", "W34"], "user_id": None, "query_identifier": 5},
    {"name": "Patagonia - Men L/XL", "brands": ["Patagonia"], "sizes": ["M_L", "M_XL"], "user_id": None, "query_identifier": 6},
]

    for channel_info in channel_data:
        if not Channel.query.filter_by(name=channel_info["name"]).first():
            channel = Channel(
            name=channel_info["name"],
            search=channel_info.get("search"),
            user_id=channel_info["user_id"],
            query_identifier=channel_info["query_identifier"],
        )

            db.session.add(channel)
            db.session.flush() 

            # Add brands to the channel
            for brand_name in channel_info["brands"]:
                brand = Brand.query.filter_by(name=brand_name).first()
                if brand:
                    channel.brands.append(brand)

            # Add sizes to the channel
            for size_name in channel_info["sizes"]:
                size = Size.query.filter_by(name=size_name).first()
                if size:
                    channel.sizes.append(size)

            db.session.add(channel)
    
    print("Added all channels successfully")

    db.session.commit()
    print("Seed data added successfully!")

if __name__ == "__main__":
    # Use app context to access the database
    with app.app_context():
        seed_data()
