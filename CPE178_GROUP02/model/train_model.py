import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sklearn.ensemble import RandomForestClassifier
from utils.preprocess import preprocess_data

import joblib

X,y = preprocess_data()

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X,y)

joblib.dump(model,"model/random_forest_model.pkl")

print("Model trained successfully!")