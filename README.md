# Chatbot Project

## Overview

This project implements a simple web-based chatbot using Flask for the backend and a neural network model for natural language processing. The chatbot is trained to understand user queries and provide appropriate responses based on predefined intents.

## Project Structure

- **`app.py`:** Defines the Flask web application, handles HTTP requests and responses.
- **`chat.py`:** Contains the logic for generating responses based on user input.
- **`model.py`:** Defines the neural network model using PyTorch and trains it based on intents defined in `intents.json`.
- **`nltk_utils.py`:** Contains utility functions for natural language processing using NLTK.
- **`train.py`:** Processes data from `intents.json`, creates a PyTorch dataset, and trains the neural network.
- **`intents.json`:** Defines the intents, patterns, and responses for the chatbot.
- **`base.html`:** HTML template for rendering the web page.
- **`style.css`:** Stylesheet for styling the HTML elements.
- **`app.js`:** The app.js file contains the JavaScript code responsible for managing the frontend functionality of the chatbox. It leverages the browser's capabilities to interact with users, send messages to the server, and update the chatbox interface.

## Setup Instructions
**Python Version:**
Make sure you have Python version 3.10.9 installed to work with Torch properly.

**Setting up Virtual Environment:**
```bash 
 python -m venv venv
 venv\Scripts\activate
```

**To deactivate:**
```bash 
 deactivate
```

**Install Dependencies:**
```bash 
pip install Flask
pip install numpy
pip install pytorch
pip install torch torchvision
```


**Install NLTK Package:**
```bash 
pip install nltk
```

**In python file**
```bash
import nltk
nltk.download('punkt')
```

**PyCharm Configuration:**
If facing issues with NLTK or file access in PyCharm, set the correct Python interpreter:
- Open PyCharm.
- Go to "File" > "Settings" (or "PyCharm" > "Preferences" on macOS).
- In the left sidebar, select "Project: <Your Project Name>" > "Python Interpreter."
- Click on the gear icon and select "Add..."
- Choose "Existing Environment."
- Navigate to C:\Users\...Python310\python.exe and select it.
- Click "OK" to apply the changes.


**Access the Chatbot:**
Open your web browser and navigate to http://localhost:5000.

### Updating Intent File
If you make changes to the intent file (`intents.json`), it's important to follow these steps to reflect the changes in your chatbot:

1. **Modify Intent File:**
   - Open the `intents.json` file.
   - Make necessary changes, such as adding new patterns, responses, or introducing new intent tags.

2. **Retraining the Model:**
   - After modifying the intent file, it's crucial to retrain the model to incorporate the changes.
   - Run the `train.py` script to update the model based on the modified intents.
     ```bash
     python train.py
     ```

3. **Run the Chatbot App:**
   - Once the model is retrained, run the Flask app (`app.py`) to deploy the chatbot with the updated model.
     ```bash
     python app.py
     ```
   - The chatbot will now respond based on the modified intents.
Remember to repeat these steps whenever you make changes to the intent file to ensure that the chatbot stays up-to-date with your defined patterns and responses.

