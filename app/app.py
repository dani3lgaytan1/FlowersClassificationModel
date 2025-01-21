from fastapi import FastAPI, File, UploadFile
import os
import json
import numpy as np
from typing import List
from tensorflow.keras.preprocessing import image
import tensorflow as tf

# Deshabilitar el uso de la GPU si no es necesario
tf.config.set_visible_devices([], 'GPU')  # Deshabilitar GPU
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"  # Esto desactiva CUDA completamente
print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))

def load_model():
    model_path = "./flowersModel.h5"
    try:
        loaded_model = tf.keras.models.load_model(model_path)
        loaded_model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
        print("Model loaded successfully")
    except Exception as e:
        print(f"Error loading model: {e}")
        raise e
    return loaded_model

app = FastAPI(
    title="FLOWERS API",
    description="API to classify five flowers class dataset",
    version="0.1",
)

UPLOAD_FOLDER = "./app/uploads/"
CLASS_NAMES =["rose", "tulip", "daisy", "dandelion", "sunflower"]

# Crear directorio de carga si no existe
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.get("/")
def main():
    return {"message": "Welcome to the flowers API"}

@app.post("/model/predict/")
async def predict(files: List[UploadFile] = File(...)):
    predictions = []
    model = load_model()
    for file in files:
        filename = file.filename
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        
        # Guardar archivo subido
        with open(file_path, "wb") as f:
            f.write(file.file.read())
        
        # Procesar imagen
        img = image.load_img(file_path, target_size=(128, 128), color_mode="rgb")
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)  # Añadir batch dimension
        img_array = img_array / 255.0  # Normalización
        print(img_array.shape)
        
        # Hacer predicción
        prediction = model.predict(img_array)
        predicted_class = CLASS_NAMES[np.argmax(prediction)]
        predictions.append({"filename": filename, "class": predicted_class, "prediction": prediction.tolist()})
    
    return {"predictions": predictions}
