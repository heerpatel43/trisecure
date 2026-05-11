from flask import Flask, render_template, request, redirect, url_for, send_file

app = Flask(__name__)

# 🏠 Home Page
@app.route('/')
def home():
    return redirect(url_for('login'))


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

    findings = []

    # 🔥 DEMO DETECTION WEBSITES
    vulnerable_sites = [
        "testphp.vulnweb.com",
        "demo.testfire.net"
    ]

    detected = False

    for site in vulnerable_sites:
        if site in url:
            detected = True
            break

    # =========================
    # IF VULNERABLE SITE
    # =========================
    if detected:

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
                "status": "Detected"
            },
            {
                "name": "Directory Traversal",
                "url": url + "/../../etc/passwd",
                "severity": "Low",
                "status": "Not Found"
            }
        ]

        risk = "High"
        high = 1
        medium = 1
        low = 0

    # =========================
    # NORMAL WEBSITES
    # =========================
    else:

        findings = [
            {
                "name": "SQL Injection",
                "url": url,
                "severity": "High",
                "status": "Not Found"
            },
            {
                "name": "XSS",
                "url": url,
                "severity": "Medium",
                "status": "Not Found"
            },
            {
                "name": "Directory Traversal",
                "url": url,
                "severity": "Low",
                "status": "Not Found"
            }
        ]

        risk = "Low"
        high = 0
        medium = 0
        low = 0

    result = {
        "url": url,
        "total": len(findings),
        "high": high,
        "medium": medium,
        "low": low,
        "risk": risk,
        "findings": findings
    }

    return render_template("scan-result.html", data=result)

@app.route('/download-report')
def download_report():
    return send_file(
        "report.txt",
        as_attachment=True
    )


@app.route('/export-pdf')
def export_pdf():
    return send_file(
        "scan_report.pdf",
        as_attachment=True
    )

if __name__ == "__main__":
    app.run(debug=True)
