import pandas as pd

def preprocess_data():

    data = pd.read_csv("dataset/expenses_sample.csv")

    data["overspending"] = data["overspending"].map({
        "No":0,
        "Yes":1
    })

    X = data.drop("overspending",axis=1)

    y = data["overspending"]

    return X,y