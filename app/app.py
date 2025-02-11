from flask import Flask, render_template
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import os


app = Flask(__name__)

# Google Sheets API Setup
CREDENTIALS_PATH = os.getenv("CREDENTIALS_PATH")
SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
CREDS = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_PATH, SCOPE)
client = gspread.authorize(CREDS)

# Open the Google Sheet (Replace with your Sheet name)
SHEET_NAME = "Skill Dataset"
sheet = client.open(SHEET_NAME).sheet1

@app.route("/")
def index():
    data = sheet.get_all_records()
    df = pd.DataFrame(data)
    records = df.to_dict(orient="records")
    return render_template("index.html", records=records, headers=df.columns)

@app.route("/profile/<name>")
def profile(name):
    data = sheet.get_all_records()
    df = pd.DataFrame(data)

    # Find the selected profile
    profile_data = df[df['Name'] == name].to_dict(orient="records")
    if not profile_data:
        return "Profile not found", 404

    return render_template("profile.html", profile=profile_data[0])

if __name__ == "__main__":
    app.run(debug=True)
