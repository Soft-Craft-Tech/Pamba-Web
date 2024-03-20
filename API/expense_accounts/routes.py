from flask import jsonify, request, Blueprint
from API import db, bcrypt
from API.lib.auth import business_login_required
from API.models import ExpenseAccount

accounts_blueprint = Blueprint("accounts", __name__, url_prefix="/API/accounts")


@accounts_blueprint.route("/create-account", methods=["POST"])
@business_login_required
def create_expense_account(business):
    """
        Create expense accounts for the business
        :param business:
        :return: 200
    """
    payload = request.get_json()
    name = payload["accountName"].strip().title()
    description = payload["description"].strip().captialize()

    # Check if the business has another business with the same name.
    existing_account = ExpenseAccount.query.filter_by(account_name=name, business_id=business.id).firs()
    if existing_account:
        return jsonify({"message": "This account already exists"}), 409

    new_account = ExpenseAccount(
        account_name=name,
        description=description,
        business_id=business.id
    )
    db.session.add(new_account)
    db.session.commit()

    return jsonify({"message": "Account has been created"}), 200

