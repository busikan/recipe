# Food Recognition and Recipe Generator Web Application

## Project Overview
This is a web-based application that allows users to upload food images, recognize key ingredients using Google Vision API, and generate recipes using OpenAI GPT. Users can customize their recipes by entering preferences and interact with the interface through dynamically displayed modals.

## Features

### 1.Upload and Preview Food Image:
Users can upload an image of a dish, and the uploaded image will be previewed on the page.

### 2.Ingredient Recognition:
The application uses the Google Vision API to identify key ingredients in the uploaded image.

### 3.Recipe Generation:
Based on the recognized ingredients and user-defined preferences, the OpenAI GPT model generates customized recipes.

### 4.Interactive UI with Modals:
Dynamic modals are displayed for ingredient review, preference entry, and recipe display.

### 5.User Actions:
Users can retry generating recipes or confirm their selection using the "Try Again" and "I Like It" buttons.

## Project Structure
- **app.py**：Backend Flask application
- **requirements.txt**：Custom CSS for styling the frontend
- **static/**：Client-side JavaScript for handling interactions
- **templates/**：Main HTML file for rendering the web interface
- **uploads/**：Directory for storing uploaded images

## Setup and Installation

### Prerequisites
Python 3.8+
Virtual environment (optional, but recommended)
Google Cloud Vision API key
OpenAI API key

## Installation Steps

### 1.Clone the repository:
```bash
git clone https://github.com/busikan/recipe.git
cd food-recognition-app
```
### 2.Set up a virtual environment (optional):
```bash
python -m venv venv
source venv/bin/activate" # For Linux/Mac
.\venv\Scripts\activate    # For Windows
```
### 3.Install dependencies:
```bash
pip install -r requirements.txt
```
### 4.Configure API keys:
Replace the placeholders in app.py with your Google Vision and OpenAI API keys:
```python
openai.api_key = "YOUR_OPENAI_API_KEY"
GOOGLE_VISION_API_KEY = "YOUR_GOOGLE_CLOUD_VISION_API_KEY"
```
### 5.Run the application:
```bash
python app.py
```
### 6.Access the application:(shown in the terminal)
Open your browser and navigate to:
```cpp
http://127.0.0.1:5000/
```

## Detailed Explanation of Project Files

### 1.app.py (Backend)
This is the core Flask application that handles routes and backend logic:
Route / renders the main HTML page.
Route /upload processes uploaded images, invokes the Google Vision API to recognize ingredients, and returns them as JSON.
Route /generate-recipe sends the recognized ingredients and user preferences to OpenAI GPT for recipe generation and returns the result​app.

### 2.recipe.html (Frontend)
The main HTML page provides the structure and elements for user interaction:
Upload Section: Allows users to upload images.
Ingredient Modals: Displays recognized ingredients.
Recipe Modal: Displays the generated recipes along with user options to try again or confirm selection​recipe.

### 3. style.css (Frontend Styling)
Defines the layout and visual appearance of the web interface:
Hero Section: Displays the main title and upload button.
Image Preview: Styles for showing the uploaded image preview.
Modals: Centered, responsive modals for displaying ingredients and recipes​style.

### script.js (Frontend Logic)
Contains JavaScript functions for handling user interactions:
Image Upload and Preview: Handles image selection and previews it.
Ingredient Recognition: Sends the uploaded image to the backend and displays recognized ingredients.
Recipe Generation: Sends ingredients and preferences to the backend and displays the generated recipes.
Modal Controls: Manages opening and closing of dynamic modals​script.

## Screenshots
1.home Page
2.Image Upload and Preview
3.Ingredient Recognition and Recipe Generation

## API Flow
1.User Action: The user uploads an image.
2.Ingredient Recognition: The image is processed by the Google Vision API.
3.Preferences Entry: The user enters any dietary preferences.
4.Recipe Generation: OpenAI GPT generates recipes based on the recognized ingredients and preferences.
5.Display: The generated recipes are displayed in a modal.

## Improvements and Future Work
Add support for multiple languages in the interface.
Provide more customization options for recipes (e.g., serving size, cuisine type).
Improve ingredient detection using additional image processing libraries.

## Tips
We have added some filters in the script2 file. You can try to connect this file if you want to filter out some less accurate or standardized recognition results.





