from flask import Flask, jsonify, request
import jwt
import datetime


app = Flask(__name__)
app.config["SECRET_KEY"] = "hTOiVN7OD5eSTR28h9Mm7SJRRhJ6sa3i"


@app.route("/auth")
def generateToken():
    data = request.get_json()

    token = jwt.encode(
        {
            "user": data["username"],
            "exp": datetime.datetime.now() + datetime.timedelta(minutes=30),
        },
        app.config["SECRET_KEY"],
    )
    return jsonify({"token: ": token.decode("UTF-8")}), 200


@app.route("/hello")
def hello():
    token = request.args.get("token")

    if not token:
        return jsonify({"message": "Token is missing"}), 403

    try:
        data = jwt.decode(token, app.config["SECRET_KEY"])
    except Exception as e:
        if e:
            return jsonify({"Error": str(e)})
        return jsonify({"message": "Token is invalid"}), 403

    return "Hello World!"


if __name__ == "__main__":
    app.run(debug=True)
