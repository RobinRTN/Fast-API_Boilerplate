from pymongo import MongoClient

try:
    # Specify the URI with the database name
    uri = "mongodb+srv://robinrettien:uZyJE7EfSKlWnVnd@vintedscraper.eqode.mongodb.net/vinted_scraper_db?retryWrites=true&w=majority&appName=VintedScraper"
    
    client = MongoClient(uri)

    # Specify the database explicitly
    db = client["vinted_scraper_db"]
    collections = db.list_collection_names()
    
    print("MongoDB connection successful. Collections:", collections)
except Exception as e:
    print("MongoDB connection failed:", e)
