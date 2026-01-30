from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/get-user/<userid>")
def get_user(userid):
    userData = {
        "userId": userid,
        "name": "John Down",
        "email": "johndown@email.com"
    }

    extra = request.args.get("extra")
    if extra:
        userData["extra"] = extra

    return jsonify(userData), 200

if __name__ == "__main__":
    app.run(debug=True)

