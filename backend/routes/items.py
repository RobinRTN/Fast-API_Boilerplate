from flask import Blueprint, request, jsonify
from flask import current_app as app
from flask_jwt_extended import jwt_required, get_jwt_identity, set_refresh_cookies, set_access_cookies, create_access_token, create_refresh_token
from models import db, User, Channel
from extensions import db, mongo, socketio
# from app import mongo_db  # Import mongo_db directly from app.py

items_bp = Blueprint("items", __name__)

@items_bp.route('/data', methods=['GET'])
def get_data():
    data = mongo.db.vinted_scraper_db.find()
    result = [doc for doc in data]
    return jsonify(result), 200

@items_bp.route("/canal/<canal_id>", methods=["GET"])
def canal_items(canal_id):
    try:
        collection_name = f"channel_{canal_id}_items"
        if collection_name not in mongo.db.list_collection_names():
            return jsonify({"msg": "No channel with this ID"}), 404

        result = mongo.db[f"channel_{canal_id}_items"].find()
        

        items = []

        for doc in result:
            doc["_id"] = str(doc["_id"])
            items.append(doc)

        return jsonify(items), 200


    except Exception as e:
        return jsonify({"msg": "Failed to retrieve the correct date"}), 400
    
@items_bp.route("scrapper_call", methods={"GET"})
@jwt_required()
def get_scrapper():
    request("")

@items_bp.route("/fresh_items", methods=["POST"])
def fresh_items():
    try:

        items = request.get_json()
        if not isinstance(items, list):
            app.logger.warning("Invalid request format")
            return jsonify({"msg": "Given body doesn't include the correct format or elements"}), 400

        app.logger.info("Received the request successfully")

        channels = Channel.get_all_channels()
        channel_mapping = {
            channel.query_identifier: {
                "brands": [brand.name for brand in channel.brands],
                "sizes": [size.name.split("_")[-1] for size in channel.sizes]
            }
            for channel in channels
        }

        matched_items = []

        for item in items:
            app.logger.info(item.get("title"))
            brand_title = item.get("brand_title")
            size_title = item.get("size_title")

            if not brand_title or not size_title:
                continue

            for channel_query_identifier, criteria in channel_mapping.items():
                if (brand_title in criteria["brands"]):
                    app.logger.info(f"Matching item found for channel {channel_query_identifier} : [[{brand_title}]], saving to MongoDB")

                    matched_item = {
                        "title": item.get("title", ""),
                        "brand_title": item.get("brand_title", ""),
                        "price": item.get("price", {}).get("amount", ""),
                        "garment_url": item.get("url", ""),
                        "photo_url": item.get("photo", {}).get("url", ""),
                        "status": item.get("status", ""),
                        "size_title": item.get("size_title", ""),
                        "favorite_count": item.get("favourite_count", 0),
                        "channel_id": channel_query_identifier,
                        "websocket": False
                    }

                    # Assuming `mongo` is initialized from Flask-PyMongo
                    result = mongo.db[f"channel_{channel_query_identifier}_items"].update_one(
                        {"title": matched_item["title"], "garment_url": matched_item["garment_url"]},
                        {"$setOnInsert": matched_item},  # Insert only if it doesn't already exist
                        upsert=True  # Create a new document if no match is found
                    )

                    if result.upserted_id:
                        app.logger.info(f"Inserted new item: {result.upserted_id}")
                    else:
                        app.logger.info("Item already exists in the collection.")
                        matched_item

                    matched_items.append(matched_item.copy())

                    matched_item["websocket"] = True
                    try:
                        socketio.emit(f"channel_{channel_query_identifier}_update", matched_item)
                    except Exception as e:
                        app.logger.error(f"WebSocket emit failed for channel {channel_query_identifier}: {e}")



        return jsonify({
            "msg": "Properly received and processed all fresh items",
            "matched_items_count": len(matched_items),
        }), 200

    except ValueError as e:
        return jsonify({"msg": str(e)}), 400

    except Exception as e:
        db.session.rollback()
        app.logger.warning("Error: %s", e)  # Use %s to format exception
        return jsonify({"msg": str(e)}), 500


