# byneer
byneer_prediction_model
Project Setup and Execution Guide

Prerequisites

Ensure you have the following installed on your system before proceeding:

Python (>=3.8)

Jupyter Notebook

MongoDB (For Windows installation, see below)

Step 1: Install Python and Jupyter Notebook

Windows / Linux / MacOS

Download and install Python from Python Official Website.

Verify installation:


python --version
#python --version
Install Jupyter Notebook:
#pip install jupyter


Launch Jupyter Notebook:
#jupyter notebook


Step 2: Set Up a Virtual Environment

Creating a virtual environment ensures that dependencies are managed properly.

#python -m venv env  # Create a virtual environment
#source env/bin/activate  # Activate for Linux/MacOS
#env\Scripts\activate  # Activate for Windows

Step 3: Install Required Dependencies

Run the following command to install the required Python packages:

#pip install -r requirements.txt

Ensure that requirements.txt includes all necessary libraries such as pymongo, selenium, numpy, pandas, etc.

Step 4: Run the Scraper to Collect Data

Execute the following command to run the scraper:

python ldp.py

This script will:

3Scrape data from the target website.

Store the historical data in MongoDB under the database newdb.

Store the latest sequence data in another collection called inputdata to be used for predictions.

Step 5: Run the Model Prediction Notebook

Open Jupyter Notebook:

jupyter notebook

Open modelprediction.ipynb and execute the cells in order.

This notebook includes:

Data Preprocessing

Feature Engineering

Data Visualization

Model Training & Prediction

Step 6: Install and Set Up MongoDB on Windows

Method 1: Install MongoDB via MSI Installer

Download MongoDB Community Edition from MongoDB Official Website.

Run the installer and follow the installation steps.

Ensure MongoDB Server and MongoDB Compass are selected.

After installation, open the Command Prompt (cmd) and start MongoDB:

#net start MongoDB

Verify MongoDB is running:

#mongo

Method 2: Install MongoDB using Windows Terminal

Open PowerShell as Administrator.

Run the following command to install MongoDB:

#choco install mongodb-community

Start the MongoDB service:

#net start MongoDB

To stop MongoDB:

#net stop MongoDB

After setting up MongoDB, verify data is stored correctly:

from pymongo import MongoClient

#client = MongoClient("mongodb://localhost:27017/")
#db = client["testdb"]
#collection = db["newdb"]

# Fetch and print the latest sequence
#latest_data = collection.find().sort("timestamp", -1).limit(1)
#for data in latest_data:
#    print("Latest Sequence:", data["sequence"])

Final Steps: Automating Predictions


If MongoDB doesn't start, check if another instance is running:


net start MongoDB  # Windows

If Python packages are missing, run:

pip install -r requirements.txt

If Jupyter Notebook fails to launch:

jupyter notebook --allow-root  # For Linux

Conclusion

This guide covers:
✅ Installing Python, Jupyter, and MongoDB
✅ Running the web scraper to collect data
✅ Setting up and querying MongoDB
✅ Running the prediction model
✅ Automating predictions for real-time updates

Now you’re ready to run the project successfully! 🚀

