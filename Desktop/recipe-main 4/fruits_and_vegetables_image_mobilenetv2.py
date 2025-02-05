import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
import numpy as np

def recognize_ingredients(image_path):
    try:
        print(f"Processing image at: {image_path}")  # 确认输入图片路径

        # 加载模型
        model = tf.keras.applications.MobileNetV2(weights='imagenet')

        # 加载并预处理图片
        img = image.load_img(image_path, target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = tf.keras.applications.mobilenet_v2.preprocess_input(img_array)

        # 模型预测
        predictions = model.predict(img_array)
        decoded_predictions = tf.keras.applications.mobilenet_v2.decode_predictions(predictions, top=5)

        # 返回前 5 个预测结果
        ingredients = [item[1] for item in decoded_predictions[0]]
        print(f"Model output: {ingredients}")  # 打印模型预测结果
        return ingredients

    except Exception as e:
        print(f"Error during prediction: {e}")
        return []
