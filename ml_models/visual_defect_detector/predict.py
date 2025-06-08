from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import os

def predict_defect(image_path):
    model = load_model('model.h5')
    img = image.load_img(image_path, target_size=(150, 150))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    prediction = model.predict(img_array)
    return "Defect Detected" if prediction[0][0] > 0.5 else "No Defect"

if __name__ == "__main__":
    print(predict_defect('C:\Users\Pavithra\OneDrive\Dokumen\M.tech\sem_4\ui_guardian_project\screenshot.png'))
