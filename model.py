import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle

data = {
    "glucose":[80,90,120,150,180,200],
    "haemoglobin":[13,12,11,10,9,8],
    "cholesterol":[150,180,220,250,280,300],
    "risk":[0,0,1,1,1,1]
}

df = pd.DataFrame(data)

X = df[['glucose','haemoglobin','cholesterol']]
y = df['risk']

model = RandomForestClassifier()

model.fit(X,y)

pickle.dump(model, open("health_model.pkl","wb"))

print("Model Saved Successfully")