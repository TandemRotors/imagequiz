import os
import random
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from flask_frozen import Freezer

app = Flask(__name__)

# Define the path to the Excel file
excel_file = 'selections.xlsx'


# Define the path to the images folder (inside the 'static' folder)
images_folder = 'static/images/'


# Function to get a random list of images from the 'images_folder'
def get_random_images():
    image_files = os.listdir(images_folder)
    random.shuffle(image_files)
    return image_files[:4]  # Get the first 4 randomly shuffled images

# Define the route for the index page
@app.route('/')
def index():
    return render_template('index.html')

# Define the route for storing image selections
@app.route('/store_selection/<user_name>/<selected_image>', methods=['GET'])
def store_selection(user_name, selected_image):
    # Get the current date and time
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Create a dictionary to store the user's data
    user_data = {
        'Name': [user_name],
        'SelectedImage': [selected_image],
        'SelectionDateTime': [current_datetime]
    }

    # Convert the dictionary to a pandas DataFrame
    df = pd.DataFrame(user_data)

    # Check if the Excel file exists, if not, create a new one
    if not os.path.exists(excel_file):
        df.to_excel(excel_file, index=False)
    else:
        # If the Excel file already exists, load it and append the new data
        existing_df = pd.read_excel(excel_file)
        updated_df = pd.concat([existing_df, df], ignore_index=True)
        updated_df.to_excel(excel_file, index=False)

    # Redirect the user back to the index page
    return redirect(url_for('index'))

# Define the route for the result page
@app.route('/result', methods=['POST'])
def result():
    if request.method == 'POST':
        user_name = request.form.get('name')  # Get the name from the form
        images = get_random_images()
        return render_template('result.html', user_name=user_name, images=images)

if __name__ == '__main__':
    app.run()
    
if __name__ == '__main__':
    app.config['FREEZER_RELATIVE_URLS'] = True
    freezer = Freezer(app)
    freezer.freeze()
