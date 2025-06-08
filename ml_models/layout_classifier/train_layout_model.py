from sklearn.ensemble import RandomForestClassifier
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

def train_layout_model():
    data = pd.read_csv('C:/Users/Pavithra/OneDrive/Dokumen/M.tech/sem_4/ui_guardian_project/ml_models/data/features.csv')
    X = data[['num_elements', 'avg_spacing', 'layout_score']]
    y = data['label']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

    model = RandomForestClassifier()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    print(f"Layout Classification Accuracy: {accuracy_score(y_test, y_pred)}")

    joblib.dump(model, 'ml_models/layout_classifier/layout_model.pkl')

if __name__ == "__main__":
    train_layout_model()
