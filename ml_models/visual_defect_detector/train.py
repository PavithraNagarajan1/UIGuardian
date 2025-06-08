import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from model import build_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.optimizers import Adam

def train_model():
    train_datagen = ImageDataGenerator(rescale=1./255, shear_range=0.2, zoom_range=0.2, horizontal_flip=True)
    train_generator = train_datagen.flow_from_directory('data/raw/train', target_size=(150, 150), batch_size=32, class_mode='binary')
    
    model = build_model(input_shape=(150, 150, 3))
    model.compile(optimizer=Adam(), loss='binary_crossentropy', metrics=['accuracy'])

    model.fit(train_generator, steps_per_epoch=200, epochs=10)
    model.save('model.h5')
    print("Model saved as model.h5 in visual_defect_detector directory.")
    
if __name__ == "__main__":
    train_model()
