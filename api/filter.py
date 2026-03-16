import pandas as pd
from io import BytesIO
from flask import Flask, request, send_file

app = Flask(__name__)

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
