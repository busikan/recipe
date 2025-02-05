import os
from flask import Flask, request, jsonify, render_template
import openai
import requests
import base64

# 初始化 Flask 应用
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# 确保上传目录存在
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# 设置 OpenAI API 密钥
openai.api_key = ""

# 设置 Google Cloud Vision API Key
GOOGLE_VISION_API_KEY = ""

def recognize_ingredients_with_google_vision(image_path):
    """Use Google Vision API to detect labels from the image."""
    try:
        with open(image_path, "rb") as image_file:
            # Convert image to base64
            image_data = base64.b64encode(image_file.read()).decode("utf-8")

        # Prepare Google Vision API request
        request_payload = {
            "requests": [
                {
                    "image": {"content": image_data},
                    "features": [{"type": "LABEL_DETECTION", "maxResults": 10}],
                }
            ]
        }
        url = f"https://vision.googleapis.com/v1/images:annotate?key={GOOGLE_VISION_API_KEY}"
        response = requests.post(url, json=request_payload)
        response_data = response.json()

        # Check if the response is valid
        if 'responses' not in response_data or not response_data['responses'][0]:
            raise ValueError("Invalid response from Google Vision API.")
        
        # Extract labels from API response
        labels = response_data["responses"][0].get("labelAnnotations", [])
        detected_labels = [label["description"] for label in labels]

        print(f"Detected Labels: {detected_labels}")

        # Post-processing: Define relevant ingredients and synonym mapping
        relevant_ingredients = [
            "Cucumber", "Pomegranate", "Egg", "Tomato", "Lettuce", "Carrot", "Potato", 
            "Apple", "Banana", "Onion", "Garlic", "Lemon", "Lime", "Mushroom", "Vegetable",
            "Lemon"
        ]

        # Define synonym mappings (e.g., map "Eggplant" to "Aubergine")
        synonym_mapping = {
            "Eggplant": "Aubergine",
            "Cucumbers": "Cucumber",
            "Limes": "Lime"
        }

        # Post-processing: Apply synonym mapping
        post_processed_labels = []
        for label in detected_labels:
            # Check if the label is in the synonym mapping, and replace it
            label = synonym_mapping.get(label, label)
            # Only include relevant ingredients
            if label in relevant_ingredients and label not in post_processed_labels:
                post_processed_labels.append(label)

        print(f"Recognized Ingredients: set({post_processed_labels}")
        return post_processed_labels
    except Exception as e:
        print(f"Error during ingredient recognition: {e}")
        return []

@app.route('/')
def index():
    return render_template('recipe.html')  
@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    # 保存图片到指定目录
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)
    print(f"File saved to: {file_path}")

    try:
        # 使用 Google Vision API 识别食材
        ingredients = recognize_ingredients_with_google_vision(file_path)
        if not ingredients:
            return jsonify({"error": "Failed to recognize ingredients."}), 500
        # 返回识别的食材
        return jsonify({"ingredients": ingredients})
    except Exception as e:
        print(f"Error during image processing: {e}")
        return jsonify({"error": "Failed to process image"}), 500

@app.route('/generate-recipe', methods=['POST'])
def generate_recipe():
    try:
        # 从前端接收食材列表和用户偏好
        ingredients = request.json.get('ingredients', [])
        preferences = request.json.get('preferences', '')

        if not ingredients:
            return jsonify({"error": "No ingredients provided"}), 400

        # 构造 GPT 提示语
        prompt = (
            f"Using the following ingredients: {', '.join(ingredients)}. "
            f"Consider the following preferences: {preferences}. "
            "Generate only one recipe with steps, cooking time, and serving suggestions."
        )

        # 调用 GPT API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Take on the role of a helpful chef assistant with worldwide culinary knowledge who generates easy and quick recipes."},
                {"role": "user", "content": prompt}
            ]
        )

        # 提取 GPT 返回的内容
        recipes = response['choices'][0]['message']['content'].strip()

        # Content Filtering
        if is_food_related(recipes):
            print(f"Generated Recipes: {recipes}")
            return jsonify({"recipes": recipes})
        else:
            print("Content does not appear to be food-related.")
            return jsonify({"error": "The generated content is not food-related"}), 400

    except Exception as e:
        print(f"Error during recipe generation: {e}")
        return jsonify({"error": "Failed to generate recipes"}), 500

def is_food_related(content):
    """
    Check if the content is related to food or cuisines.
    """
    food_keywords = [
        "recipe", "dish", "ingredient", "cuisine", "cook", "bake", "grill", "saute",
        "meal", "snack", "dessert", "soup", "salad", "pasta", "spice", "flavor"
    ]
    # Check if any keyword is present in the content
    return any(keyword.lower() in content.lower() for keyword in food_keywords)

if __name__ == '__main__':
    app.run(debug=True)
