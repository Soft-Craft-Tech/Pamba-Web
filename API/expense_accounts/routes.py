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


@accounts_blueprint.route("/delete/<int:account_id>")
@business_login_required
def delete_account(business, account_id):
    """
        Delete business's expense account
        :param business:
        :param account_id:
        :return:
    """
    payload = request.get_json()
    password = payload["password"].strip()

    if not bcrypt.check_password_hash(business.password, password):
        return jsonify({"message": "Incorrect password"}), 401

    account = ExpenseAccount.query.get(account_id)
    if not account:
        return jsonify({"message": "Account Not Found"}), 404

    if account.business_id != business.id:
        return jsonify({"message": "Not allowed"}), 400

    db.session.delete(account)
    db.session.commit()

    return jsonify({"message": "Account Deleted"}), 200

