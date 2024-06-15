import tensorflow as tf
from flask import Flask, jsonify, request, render_template
import numpy as np
import traceback
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS

# Load your Keras model
model = tf.keras.models.load_model('saved_model.h5')

print("Model input shape:", model.input_shape)  # Print the model's expected input shape

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        print("Received data:", data)  # Log received data

        if not data or 'winning_numbers' not in data:
            print("Invalid input data. Please provide winning_numbers.")
            return jsonify({'error': 'Invalid input data. Please provide winning_numbers.'}), 400

        winning_numbers = data['winning_numbers']

        print("Received winning_numbers:", winning_numbers) 

        # Enhanced Input Validation (type, length, positive values)
        if not isinstance(winning_numbers, list) or not all(
            isinstance(num, (int, float)) and 1 <= num <= 80 for num in winning_numbers
        ):
            print("Winning numbers must be a list of positive integers between 1 and 80.")
            return jsonify({'error': 'Winning numbers must be a list of positive integers between 1 and 80.'}), 400

        if len(winning_numbers) != 20:  # Assuming you need 20 lottery numbers
            print(f'Expected 20 winning numbers, but got {len(winning_numbers)}.')
            return jsonify({'error': f'Expected 20 winning numbers, but got {len(winning_numbers)}.'}), 400

        # Data Preparation (one-hot encoding the input numbers)
        input_vector = np.zeros(80)
        for number in winning_numbers:
            input_vector[int(number)-1] = 1
        
        input_data = np.array([input_vector], dtype=np.float32)

        print("Input data to model:", input_data) 
        print("Input data shape:", input_data.shape) 

        # Model Prediction
        prediction = model.predict(input_data)

        print("Raw prediction from model:", prediction)
        print("Prediction shape:", prediction.shape) 

        # Post-Processing (Extract probabilities for months and find the highest)
        month_probabilities = prediction[0][:12]  # Assuming first 12 outputs correspond to months
        best_month_index = np.argmax(month_probabilities)
        best_month = best_month_index + 1  # Months are 1-indexed
        best_month_probability = month_probabilities[best_month_index]

        return jsonify({'best_month': best_month, 'best_month_probability': best_month_probability})

    except Exception as e:
        print("Error during prediction:")
        traceback.print_exc()
        return jsonify({'error': 'An error occurred during prediction'}), 500

if __name__ == '__main__':
    app.run(debug=True)
    