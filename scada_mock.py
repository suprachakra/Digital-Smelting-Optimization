"""
scada_mock.py
A mock SCADA service to accept setpoints from the optimization engine.
Run: python scada_mock.py
Then POST to http://localhost:5000/api/scada/setpoint with JSON like:
{
  "voltage": 4.5,
  "current": 130.0
}
"""

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/scada/setpoint', methods=['POST'])
def set_setpoint():
    data = request.json
    voltage = data.get('voltage', 4.0)
    current = data.get('current', 100.0)

    # Basic safety checks
    if voltage < 4.0 or voltage > 5.0:
        return jsonify({"status": "OVERRIDE", "reason": "Voltage out of safe range"}), 400
    if current < 90.0 or current > 150.0:
        return jsonify({"status": "OVERRIDE", "reason": "Current out of safe range"}), 400

    # Otherwise accept
    return jsonify({"status": "OK", "applied_voltage": voltage, "applied_current": current}), 200

if __name__ == '__main__':
    app.run(port=5000, debug=True)

