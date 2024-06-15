from flask import Flask, request, jsonify
from flask_cors import CORS


app = Flask(__name__)
CORS(app)  # Enable CORS

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()

        print("Received data:", data)  # Print the raw data for debugging

        # Basic input validation (adjust as needed for your model)
        if not data or 'winning_numbers' not in data:
            return jsonify({'error': 'Missing winning_numbers data.'}), 400
        if not isinstance(data['winning_numbers'], list):
            return jsonify({'error': 'winning_numbers must be a list.'}), 400
        if len(data['winning_numbers']) != 64:
            return jsonify({'error': 'Must provide exactly 64 winning numbers.'}), 400

        # Echo back the received winning numbers for testing
        return jsonify({'received_numbers': data['winning_numbers']})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
