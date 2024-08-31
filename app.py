from flask import Flask, request, jsonify, render_template, redirect, url_for, flash  # Import Flask and related functions
from chatbot import handle_user_input  # Import the function to handle user input from chatbot.py
from datetime import datetime  # Import datetime for timestamping
import json  # Import JSON module for handling JSON data
import os  # Import OS module for interacting with the operating system
import logging  # Import logging module for logging messages

# Configure logging to display INFO level messages
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')



app = Flask(__name__)  # Create a Flask application instance
app.secret_key = 'your_secret_key'  # Set a secret key for session management and flash messages



# Route for the home page
@app.route('/')
def home():
    return render_template('index.html')  # Render the index.html template for the home page



# Route for handling chat
@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')  # Get the user message from the JSON payload
    response = handle_user_input(user_input)  # Call your chatbot function to get the response
    return jsonify({"response": response})  # Return the response as JSON


# Route for displaying chat history
@app.route('/history')
def history():
    if os.path.exists('conversation_history.json'):  # Check if the history file exists
        with open('conversation_history.json', 'r') as file:  # Open the file in read mode
            raw_history = json.load(file)  # Load the JSON data into raw_history
        
        # Convert raw history into a list of dictionaries with timestamp
        chat_history = []
        for entry in raw_history:  # Iterate through the history entries
            chat_history.append({
                "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),  # Use the current timestamp
                "user": "User",  # Placeholder for user; modify based on your needs
                "message": entry[0],  # User message from history
                "response": entry[1]  # AI response from history
            })
    else:
        chat_history = []  # Initialize an empty list if the file does not exist

    return render_template('history.html', chat_history=chat_history)  # Render the history.html template with chat history

# Error handling route for 404 errors
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404  # Render the 404.html template for page not found errors

if __name__ == '__main__':  # Check if this script is being run directly
    app.run(debug=True, port=8000)  # Run the Flask application in debug mode in port 8000