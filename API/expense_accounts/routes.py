from flask import jsonify, request, Blueprint
from API import db, bcrypt
from API.lib.auth import business_login_required
from API.models import ExpenseAccount
from API.lib.data_serializer import serialize_account

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
    accounts = payload["accounts"]

    for acc in accounts:
        # Check if the business has another business with the same name.
        existing_account = ExpenseAccount.query.filter_by(account_name=acc["accountName"], business_id=business.id).first()
        if existing_account:
            continue
        new_account = ExpenseAccount(
            account_name=acc["accountName"],
            description=acc["description"],
            business_id=business.id
        )
        db.session.add(new_account)
    db.session.commit()

    return jsonify({"message": "Account has been created"}), 200


@accounts_blueprint.route("/delete/<int:account_id>", methods=["DELETE"])
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
        return jsonify({"message": "Not allowed"}), 403

    db.session.delete(account)
    db.session.commit()

    return jsonify({"message": "Account Deleted"}), 200


@accounts_blueprint.route("/update/<int:account_id>", methods=["PUT"])
@business_login_required
def update_account(business, account_id):
    """
        Update Expense account
        :param business:
        :param account_id:
        :return: 404, 401, 409, 200
    """
    payload = request.get_json()
    name = payload["accountName"].strip().title()
    description = payload["description"].strip().capitalize()
    password = payload["password"].strip()

    if not bcrypt.check_password_hash(business.password, password):
        return jsonify({"message": "Incorrect password"}), 401

    account = ExpenseAccount.query.get(account_id)
    if not account:
        return jsonify({"message": "Account doesn't exist"}), 404

    # Check if an account exists with the same name for the same business
    same_name = ExpenseAccount.query.filter_by(account_name=name, business_id=business.id).first()
    if same_name and same_name.id != account.id:
        return jsonify({"message": "This account name already exists"}), 409

    if account.business_id != business.id:
        return jsonify({"message": "Not allowed"}), 403

    account.account_name = name
    account.description = description
    db.session.commit()

    return jsonify({"message": "Account Updated"}), 200


@accounts_blueprint.route("/all", methods=["GET"])
@business_login_required
def fetch_all_business_account(business):
    """
        Fetch all accounts for the logged in business
        :param business:
        :return: 200
    """

    accounts = ExpenseAccount.query.filter_by(business_id=business.id).all()
    my_accounts = []

    for account in accounts:
        my_accounts.append(serialize_account(account))

    return jsonify({"account": my_accounts}), 200
