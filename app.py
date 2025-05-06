from flask import Flask, jsonify

from flaskr import create_app

app = create_app()


@app.route("/")
def hello_world():
    return jsonify(message="Welcome to this custom api")

if __name__ == "__main__":
    app.run(debug=True)

