import flask_cors
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from chat import get_response
import nltk

app = Flask(__name__)
# FOR RENDER DEPLOYMENT
#
# CORS(app,origins="https://chatbot-moodle.onrender.com")
#
# # @app.before_first_request
# def download_nltk_resources():
#     nltk.download('punkt')
# #     calling the function
# download_nltk_resources()

@app.route("/")
def index():
    return render_template("base.html")

# # for Deployment NEW
# @app.post("/predict")
# def predict():
#     try:
#         data = request.get_json()
#         if "message" not in data:
#             raise ValueError("Message field is missing")
#         text = data["message"]
#         # Perform input validation if necessary
#         response = get_response(text)
#         message = {"answer": response}
#         return jsonify(message)
#     except Exception as e:
#         error_message = {"error": str(e)}
#         return jsonify(error_message), 400

# For Local
@app.post("/predict")
def predict():
    text = request.get_json().get("message")

    response = get_response(text)
    message = {"answer": response}
    return jsonify(message)


if __name__ == "__main__":
    app.run(debug=True)

