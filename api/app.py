import pandas as pd
from flask import Flask, request, send_file
from io import BytesIO

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <h2>JSW Agent Filter Tool</h2>
    <form action="/api/filter" method="post" enctype="multipart/form-data">
    
    Agent File:
    <input type="file" name="agent_file"><br><br>
    
    Login File:
    <input type="file" name="login_file"><br><br>
    
    <button type="submit">Generate Excel</button>
    
    </form>
    """

@app.route("/api/filter", methods=["POST"])
def filter_file():

    agent_file = request.files['agent_file']
    login_file = request.files['login_file']

    jsw = pd.read_excel(agent_file)

    if login_file.filename.endswith(".csv"):
        jsw_login = pd.read_csv(login_file)
    else:
        jsw_login = pd.read_excel(login_file)

    jsw_data = jsw['agent_email']

    filter_data = jsw_login[jsw_login['agent_email'].isin(jsw_data)]

    output = BytesIO()
    filter_data.to_excel(output, index=False)
    output.seek(0)

    return send_file(
        output,
        download_name="jsw_agent_data.xlsx",
        as_attachment=True
    )
