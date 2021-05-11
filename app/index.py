from flask import Flask, jsonify, request
from flask_pymongo import PyMongo, MongoClient, ObjectId
from pymongo.errors import BulkWriteError
from dotenv import load_dotenv
import os, bson, json
from bson import json_util
from os.path import join, dirname
from app.util.json_encode import Encode

# Model
from app.model.expense import Expense, ExpenseSchema
from app.model.income import Income, IncomeSchema
from app.model.transaction_type import TransactionType

app = Flask(__name__)

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)


# MONGODB INIT
user = os.environ.get("MONGO_USER")
pw = os.environ.get("MONGO_PASSWORD")

print(user, pw)

mongodb_client = PyMongo(
    app,
    uri="mongodb+srv://arif:zubkHKBWRyYMjKSS@cluster0.afxa4.mongodb.net/myDb?retryWrites=true&w=majority",
    # uri="mongodb+srv://{user}:{pw}@cluster0.afxa4.mongodb.net/myDb?retryWrites=true&w=majority",
)
db = mongodb_client.db


transactions = [
    Income("Salary", 5000),
    Income("Dividends", 200),
    Expense("pizza", 50),
    Expense("Rock Concert", 100),
]


@app.route("/")
def hello():
    return "Hello"


def parse_json(data):
    return json.loads(json_util.dumps(data))


# API from DB
### GET
@app.route("/add_one")
def add_one():
    db.todos.insert_one({"title": "todo title", "body": "todo body"})
    return jsonify(message="success")


@app.route("/add_many")
def add_many():
    db.todos.insert_many(
        [
            {
                "title": "todo title one ",
                "body": "todo body one ",
            },
            {
                "title": "todo title two",
                "body": "todo body two",
            },
            {
                "title": "todo title three",
                "body": "todo body three",
            },
        ],
        ordered=False,
    )
    return jsonify(message="success")
    # try:
    # except BulkWriteError as e:
    #     return jsonify(
    #         message="duplicates encountered and ignored",
    #         details=e.details,
    #         inserted=e.details["nInserted"],
    #         duplicates=[x["op"] for x in e.details["writeErrors"]],
    #     )


@app.route("/get_data")
def home():
    todos = db.todos.find()
    # return jsonify([todo for todo in todos])
    return parse_json([todo for todo in todos])


### PATCH
@app.route("/replace_todo/<int:todoId>")
def replace_one(todoId):
    result = db.todos.replace_one({"_id": todoId}, {"title": "modified title"})
    return {"id": result.raw_result}


@app.route("/update_todo/<int:todoId>")
def update_one(todoId):
    result = db.todos.update_one({"_id": todoId}, {"$set": {"title": "updated title"}})
    return result.raw_result


@app.route("/update_many")
def update_many():
    todo = db.todos.update_many(
        {"title": "todo title two"}, {"$set": {"body": "updated body"}}
    )
    return todo.raw_result


###DELETE
@app.route("/delete_todo/<int:todoId>", methods=["DELETE"])
def delete_todo(todoId):
    todo = db.todos.delete_one({"_id": todoId})
    return todo.raw_result


@app.route("/delete_many", methods=["DELETE"])
def delete_many():
    todo = db.todos.delete_many({"title": "todo title two"})
    return todo.raw_result


### SAVE GRIDFS
@app.route("/save_file", methods=["POST", "GET"])
def save_file():
    upload_form = """<h1>Save file</h1>
                     <form method="POST" enctype="multipart/form-data">
                     <input type="file" name="file" id="file">
                     <br><br>
                     <input type="submit">
                     </form>"""

    if request.method == "POST":
        if "file" in request.files:
            file = request.files["file"]
            mongodb_client.save_file(file.filename, file)
            return {"file name": file.filename}
    return upload_form


# API local
@app.route("/incomes")
def get_incomes():
    schema = IncomeSchema(many=True)
    incomes = schema.dump(
        filter(lambda t: t.type == TransactionType.INCOME, transactions)
    )
    return jsonify(incomes)


@app.route("/incomes", methods=["POST"])
def add_income():
    income = IncomeSchema().load(request.get_json())
    transactions.append(income)
    return jsonify({"updated": "true"})
    # return "", 204


@app.route("/expenses")
def get_expenses():
    schema = ExpenseSchema(many=True)
    expenses = schema.dump(
        filter(lambda t: t.type == TransactionType.EXPENSE, transactions)
    )
    return jsonify(expenses)


@app.route("/expenses", methods=["POST"])
def add_expense():
    expense = ExpenseSchema().load(request.get_json())
    transactions.append(expense)
    return jsonify({"updated": "true"})
    # return "", 204


if __name__ == "__main__":
    app.run()
