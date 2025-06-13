from flask import Flask, render_template, request, jsonify
from routes.ai_routes import ai_bp

app = Flask(__name__)
app.register_blueprint(ai_bp)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/hello", methods=["GET"])
def hello():
    return jsonify({"msg": "Hello, world!"})

if __name__ == "__main__":
    app.run(debug=True)


