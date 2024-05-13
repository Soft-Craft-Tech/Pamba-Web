from flask import jsonify, request, Blueprint
from API import db
from API.lib.auth import business_login_required
from API.lib.data_serializer import serialize_expenses
from API.models import Expense, ExpenseAccount
from datetime import datetime

expenses_blueprint = Blueprint("expenses", __name__, url_prefix="/API/expenses")


@expenses_blueprint.route("/record-expense", methods=["POST"])
@business_login_required
def record_expenses(business):
    """
        Record new expenses
        :param business:
        :return: 400, 200
    """
    payload = request.get_json()
    expense = payload["expenseTitle"].strip().title()
    amount = payload["expenseAmount"]
    description = payload["description"].strip().capitalize()
    account_id = payload["accountID"]

    account = ExpenseAccount.query.get(account_id)
    if not account:
        return jsonify({"message": "Expense account does not exist"}), 400

    if account.business.id != business.id:
        return jsonify({"message": "Not Allowed"}), 403

    new_expense = Expense(
        expense=expense,
        amount=amount,
        description=description,
        expense_account=account_id,
        business_id=business.id
    )

    db.session.add(new_expense)
    db.session.commit()

    return jsonify({"message": "Expense Recorded", "expense": serialize_expenses(new_expense)}), 201


@expenses_blueprint.route("/delete-expense/<int:expense_id>", methods=["DELETE"])
@business_login_required
def delete_expense(business, expense_id):
    """
        Delete expense with given id
        :param business: Logged in Business/Owner
        :param expense_id: ID of expense to be deleted
        :return: 404, 400, 200
    """

    expense = Expense.query.get(expense_id)
    if not expense:
        return jsonify({"message": "Expense not found"}), 404

    db.session.delete(expense)
    db.session.commit()

    return jsonify({"message": "Expense deleted", "deleted": serialize_expenses(expense)}), 200


@expenses_blueprint.route("/update-expense/<int:expense_id>", methods=["PUT"])
@business_login_required
def update_expense(business, expense_id):
    """
        Update an expense
        :param business:
        :param expense_id:
        :return: 400, 404, 200
    """
    payload = request.get_json()
    expense = payload["expenseTitle"].strip().title()
    amount = payload["expenseAmount"]
    description = payload["description"].strip().capitalize()
    account_id = payload["accountID"]

    expense_record = Expense.query.get(expense_id)
    if not expense_record:
        return jsonify({"message": "Expense record not found"}), 404

    expense_record.expense = expense
    expense_record.amount = amount
    expense_record.description = description,
    expense_record.account_id = account_id
    expense_record.modified_at = datetime.utcnow()
    db.session.commit()

    return jsonify({"message": "Update Successful", "updated": serialize_expenses(expense_record)}), 200


@expenses_blueprint.route("/my-expenses", methods=["GET"])
@business_login_required
def fetch_business_expenses(business):
    """
        Fetch Expenses for the current logged in business.
        :param business:
        :return: 400, 200
    """
    all_expenses = []
    for expense in business.expenses.all():
        serialized_expense = serialize_expenses(expense)
        serialized_expense["category"] = expense.account.account_name
        all_expenses.append(serialized_expense)

    return jsonify({"expenses": all_expenses}), 200


@expenses_blueprint.route("/expense/<int:expense_id>", methods=["GET"])
@business_login_required
def fetch_single_expense(business, expense_id):
    """
        Fetcha single expense given expense_ID
        :param business: User
        :param expense_id: ID of the expense
        :return: 404, 400, 200
    """
    expense = Expense.query.get(expense_id)
    if not expense:
        return jsonify({"message": "Expense Not Found"}), 404

    account_ids = [account.id for account in business.expense_accounts.all()]
    if expense.expense_account not in account_ids:
        return jsonify({"message": "Not Allowed"}), 403

    return jsonify({"expense": serialize_expenses(expense)}), 200

