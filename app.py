from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# 🏠 Home Page
@app.route('/')
def home():
    return render_template('index.html')


# 🔐 Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return redirect(url_for('home'))

    return render_template('login.html')


# ⭐ Features Page
@app.route('/features')
def features():
    return render_template('features.html')


# ⚙️ How It Works Page
@app.route('/how-it-works')
def how_it_works():
    return render_template('how-it-works.html')


# 📊 Scan Result Page
@app.route('/scan-result')
def scan_result():
    dummy_data = {
        "url": "No scan yet",
        "total": 0,
        "high": 0,
        "medium": 0,
        "low": 0,
        "risk": "None",
        "findings": []
    }

    return render_template('scan-result.html', data=dummy_data)


# 🔍 Scan Logic (from index page)

import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

@app.route('/scan', methods=['POST'])
def scan():
    url = request.form.get('url')

    if not url.startswith("http"):
        url = "https://" + url

    # 🔥 Manual demo findings
    findings = [
        {
            "name": "SQL Injection",
            "url": url + "?id=1'",
            "severity": "High",
            "status": "Detected"
        },
        {
            "name": "XSS",
            "url": url + "?search=<script>alert(1)</script>",
            "severity": "Medium",
            "status": "Not Found"
        },
        {
            "name": "Directory Traversal",
            "url": url + "/../../etc/passwd",
            "severity": "Low",
            "status": "Not Found"
        }
    ]

    result = {
        "url": url,
        "total": 3,
        "high": 1,
        "medium": 0,
        "low": 0,
        "risk": "High",
        "findings": findings
    }

    return render_template("scan-result.html", data=result)
@app.route('/download-report')
def download_report():
    from flask import send_file

    file_path = "report.txt"

    with open(file_path, "w") as file:
        file.write("TRISECURE SCAN REPORT\n")
        file.write("=====================\n\n")
        file.write("SQL Injection - High - Detected\n")
        file.write("XSS - Medium - Not Found\n")
        file.write("Directory Traversal - Low - Not Found\n")

    return send_file(file_path, as_attachment=True)

@app.route('/export-pdf')
def export_pdf():
    from flask import send_file
    from reportlab.pdfgen import canvas

    file_path = "scan_report.pdf"

    c = canvas.Canvas(file_path)

    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 800, "TriSecure Scan Report")

    c.setFont("Helvetica", 12)
    c.drawString(100, 750, "SQL Injection - High - Detected")
    c.drawString(100, 720, "XSS - Medium - Not Found")
    c.drawString(100, 690, "Directory Traversal - Low - Not Found")

    c.save()

    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)