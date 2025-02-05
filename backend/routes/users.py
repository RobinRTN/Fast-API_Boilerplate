import requests
from flask import Blueprint, request, jsonify, redirect, url_for, session, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity, set_refresh_cookies, set_access_cookies, create_access_token, create_refresh_token, unset_jwt_cookies, verify_jwt_in_request
from models import db, User
from datetime import timedelta
from authlib.integrations.flask_client import OAuth
import os
import urllib.parse
from extensions import get_google_oauth

users_bp = Blueprint("users", __name__)

@users_bp.route("/users/auth/google", methods=["POST"])
def auth_google():
    try:
        data = request.get_json()
        id_token = data.get("idToken")


        if not id_token:
            return jsonify({"msg": "no idToken given so no oauth possible!"}), 400
        
        google_url = "https://oauth2.googleapis.com/tokeninfo"
        response = requests.get(f"{google_url}?id_token={id_token}")


        user_info = response.json()



        if "email" not in user_info:
            return jsonify({"msg": "Invalid Google authentication"}), 401
        
        email = user_info["email"]

        
        user = User.get_user(email)


        if not user:
            print("Commiting a new user...", flush=True)
            user = User(email=email)
            db.session.add(user)
            db.session.commit()


        access_token = create_access_token(identity=email)
        refresh_token = create_refresh_token(identity=email)

        print("access_token", access_token, flush=True)
        print("refresh_token", refresh_token, flush=True)

        response = jsonify({"msg": "Google oauth successful"})
        set_access_cookies(response, access_token)
        set_refresh_cookies(response, refresh_token)

        return response, 200
    
    except Exception as e: 
        return jsonify({"msg": "Google Oauth failed"}), 500



@users_bp.route("/signup", methods=["POST"])
def signup():
    try:
        data = request.get_json() or {}
        email = data.get("email", None)
        password = data.get("password", None)

        User.verify_email(email)
        User.verify_password(password)

        if User.get_user(email):
            return jsonify({"msg": "Compte existant !"}), 409

        user = User(email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        access_token = create_access_token(identity=email)
        refresh_token = create_refresh_token(identity=email)

        response = jsonify({
            "msg": "User created successfully"
        })

        set_access_cookies(response, access_token)
        set_refresh_cookies(response, refresh_token)

        return response, 201

    
    except ValueError as e:
        return jsonify({"msg": str(e)}), 400
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": str(e)}), 500

@users_bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json() or {}
        email = data.get("email")
        password = data.get("password")

        user = User.get_user(email)
        print("printing ->", user)
        if not user or not user.check_password(password):
            return jsonify({"msg": "Identifiants incorrects !"}), 401
        
        access_token = create_access_token(identity=email)
        refresh_token = create_refresh_token(identity=email)

        response = jsonify({
            "msg": "Logged in successfully"
        })

        set_access_cookies(response, access_token)
        set_refresh_cookies(response, refresh_token)

        return response, 200
    
    except Exception as e:
        return jsonify({"msg": str(e)}), 500

@users_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    response = jsonify({"msg": "Successfully logged out"})
    unset_jwt_cookies(response)
    return response, 200

@users_bp.route("/delete_user", methods=["DELETE"])
@jwt_required()
def delete_user():
    try:
        current_email = get_jwt_identity()
        user = User.get_user(current_email)
        if not user:
            return jsonify({"msg": "user not found"}), 404

        db.session.delete(user)
        db.session.commit()
        response = jsonify({"msg": "Deleted the user successfully"})
        unset_jwt_cookies(response)
        return response, 200 
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": str(e)}), 500

@users_bp.route("/refresh", methods=["POST"])
def refresh():
    try:
        verify_jwt_in_request(refresh=True)
        current_user = get_jwt_identity()
        new_access_token = create_access_token(identity=current_user)
        response = jsonify({"msg": "Token refreshed successfully"})
        set_access_cookies(response, new_access_token)
        return response, 200
    except Exception:
        return jsonify({"msg": "Invalid refresh token, please log again"}), 401

@users_bp.route("/all_users", methods=["GET"])
@jwt_required()
def all_users():
    users = User.get_all_users()
    serialized_users = [user.to_dict() for user in users]
    return jsonify({"msg": serialized_users}), 200

@users_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    return jsonify({"msg": "User well connected"}), 200