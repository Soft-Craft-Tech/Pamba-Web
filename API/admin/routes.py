from flask import Blueprint, jsonify, request
from API.models import BusinessCategory, ServiceCategories
from API import db

admin_blueprint = Blueprint("admin", __name__, url_prefix="/API/admin")


@admin_blueprint.route("/add-categories", methods=["POST"])
def add_business_categories():
    """
        Add Business Categories
        :return: 201
    """
    try:
        payload = request.get_json()
        categories = payload["categories"]

        for category in categories:
            business_category = BusinessCategory(
                category_name=category.strip().title()
            )
            db.session.add(business_category)
        
        db.session.commit()
        return jsonify({"message": "Categories have been Created Successfully"}), 201
    
    except KeyError:
        return jsonify({"message": "Invalid payload: 'categories' key is required"}), 400
    except AttributeError:
        return jsonify({"message": "Invalid payload: JSON format required"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Failed to add categories", "error": str(e)}), 400 

@admin_blueprint.route("/add-service-categories", methods=["POST"])
def add_service_categories():
    """
        Add Service Categories
        :return: 201
    """
    payload = request.get_json()
    categories = payload["categories"]
    try:
        for category in categories:
            service_category = ServiceCategories(
                category_name=category.strip().title()
            )
            db.session.add(service_category)

        db.session.commit()
        return jsonify({"message": "Service Categories added successfully"}), 201
    except KeyError:
        return jsonify({"message": "Invalid payload: 'categories' key is required"}), 400
    except AttributeError:
        return jsonify({"message": "Invalid payload: JSON format required"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Failed to add service categories", "error": str(e)}), 400

