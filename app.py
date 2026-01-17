from flask import Flask, render_template, jsonify
from scanner import NetworkScanner

app = Flask(__name__)
scanner = NetworkScanner()

@app.route('/')
def home():
    return render_template('dashboard.html')

@app.route('/api/scan')
def trigger_scan():
    try:
        results = scanner.scan()
        return jsonify({"status": "success", "devices": results})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    # '0.0.0.0' allows you to see the dashboard from your phone too!
    app.run(debug=True, host='0.0.0.0', port=5000)