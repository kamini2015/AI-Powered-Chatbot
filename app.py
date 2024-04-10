import flask_cors
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from chat import get_response
from datetime import datetime
import nltk
app = Flask(__name__)

from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/sqlservice.admin']
SERVICE_ACCOUNT_FILE = 'google sheet keys.json'

SCOPES=['https://www.googleapis.com/auth/spreadsheets']
creds = None
creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

SAMPLE_SPREADSHEET_ID = "1Okcq4SdHTkLqI4__qc2rErsR6wFWyUrK77ovuKUJ1JE"

# FOR RENDER DEPLOYMENT

CORS(app,origins="https://chatbot-moodle.onrender.com")

@app.before_first_request
def download_resources():
    nltk.download('punkt')
    nltk.download('wordnet')

#     calling the function
download_resources()


# Function to update Google Sheets
def update_google_sheets(data):
    service = build("sheets", "v4", credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = (
            sheet.values()
            .get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range="LOGS!A1:G5")
            .execute()
        )
    print(result)

    service = build("sheets", "v4", credentials=creds)
    sheet = service.spreadsheets()

    # Prepare the data to be inserted into the spreadsheet
    values = [
        [data["timestamp"], data["tag"], data["question"], data["message"],  data["confidence"],data["words_understood"]]
    ]

    # Call the Sheets API to update the spreadsheet
    request = sheet.values().append(
        spreadsheetId=SAMPLE_SPREADSHEET_ID,
        range="LOGS!A1",  # Specify the range where you want to insert the data
        valueInputOption="USER_ENTERED",
        body={"values": values}
    ).execute()
    print(request)

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

    # Return the response to the client
    message = {"answer": message}
    # Update Google Sheets with the data
    update_google_sheets(data)

    return jsonify(message)


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

if __name__ == "__main__":
    app.run(debug=True)
