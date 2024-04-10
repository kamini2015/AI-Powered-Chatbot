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
    print("TESTING TO STORE THE DATA\n")
    text = request.get_json().get("message")
    print(text)
    response = get_response(text)
    print(response)
    message = {"answer": response}
    print(response)
    return jsonify(message)


if __name__ == "__main__":
    app.run(debug=True)

-------

import flask_cors
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from chat import get_response
from datetime import datetime
import requests

app = Flask(__name__)

# Replace these variables with your SharePoint site URL and credentials
SHAREPOINT_SITE_URL = "https://tbcollege0-my.sharepoint.com"
SHAREPOINT_USERNAME = "PowerBI.Dashboard@tbcollege.com"
SHAREPOINT_PASSWORD = "Lux73474"

def add_to_sharepoint(data):
    # Define SharePoint API endpoint
    endpoint = f"{SHAREPOINT_SITE_URL}/_api/lists/getbytitle('ChatBot_Logs.xlsx')/items"

    # Prepare data to be sent to SharePoint
    item_data = {
        "Title": data["message"],
        "Timestamp": data["timestamp"],
        "Tag": data["tag"],
        "Confidence": data["confidence"],
        "WordsUnderstood": data["words_understood"],
        "Question": data["question"]
    }

    # Make a POST request to SharePoint API to add the item
    response = requests.post(endpoint, json=item_data, auth=(SHAREPOINT_USERNAME, SHAREPOINT_PASSWORD))
    if response.status_code == 201:
        print("Data added to SharePoint successfully")
    else:
        print("Failed to add data to SharePoint")
        print(response.text)

@app.route("/")
def index():
    return render_template("base.html")

@app.post("/predict")
def predict():
    text = request.get_json().get("message")
    # Get the current timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Call the function to get the response from the chatbot
    response = get_response(text)
    print("RESPONSE",response,type(response))
    print(response[0])
    message=response[0]
    tag=response[1]
    confidence=response[2]
    words_understood=str(response[3])
    question=response[4]
    print("TESTING : ",message,tag,confidence,words_understood,question)

    # Prepare the data to be stored
    data = {
        "timestamp": timestamp,
        "message": message,
        "tag": tag,
        "confidence": confidence,
        "words_understood": words_understood,
        "question": question
    }

    # Add data to SharePoint
    add_to_sharepoint(data)

    # Return the response to the client
    message = {"answer": message}
    return jsonify(message)

if __name__ == "__main__":
    app.run(debug=True)
