import joblib
import pandas as pd

# Load the trained model
model = joblib.load('ml_models/layout_classifier/layout_model.pkl')

# Example input for prediction (with feature names)
sample = pd.DataFrame([[12, 34.5, 0.82]], columns=['num_elements', 'avg_spacing', 'layout_score'])

# Predict using the loaded model
prediction = model.predict(sample)
print("Predicted label:", prediction[0])