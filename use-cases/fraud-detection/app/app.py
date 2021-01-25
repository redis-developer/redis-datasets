from flask import Flask, request
from fraud_checks import FraudChecks
from setup import Setup
app = Flask(__name__)


@app.route('/', methods=['POST'])
def check_fraud():
    try:
        response = FraudChecks().check_fraud(request.get_json())
        code = 200
    except Exception as e:
        print("Error occurred ", e)
        response = str(e)
        code = 500

    return response, code


if __name__ == '__main__':
    Setup().init()
    app.run(port=5000, debug=False, host='0.0.0.0')
