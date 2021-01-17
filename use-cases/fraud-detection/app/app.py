from flask import Flask, request
from fraud_checks import FraudChecks

app = Flask(__name__)


@app.route('/', methods=['POST'])
def check_fraud():
    # Sample Request
    # curl --location --request POST 'localhost:5000' \
    # --header 'Content-Type: application/json' \
    # --data-raw '{
    #     "device_id": "111-000-000",
    #     "ip": "1.1.1.2",
    #     "transaction_id": "3e4fad5fs"
    # }'

    return FraudChecks().check_fraud(request.get_json())


if __name__ == '__main__':
    app.run(port=5000, debug=True)
