from flask import Flask, request, jsonify


app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "Hello world"


@app.route("/user/<username>", methods=["GET"])
def greet_user(username):
    t = str(type(username))
    print(t)
    return f"Hello {username}"


@app.route("/sum/<float:num1>/<float:num2>", methods=["GET"])
def sum_fun(num1, num2):
    s = num1 + num2
    return f"Sum is {s}"

@app.route("/files/<path:filename>", methods=["GET"])
def filepath(filename):
    return f"{filename}"


@app.route("/query", methods=["POST"])
def get_response():
    data = request.json

    return jsonify({"status": "ok", **data})

if __name__ == '__main__':
    app.run(debug=True)