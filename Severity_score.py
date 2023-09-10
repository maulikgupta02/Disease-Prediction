import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import f1_score, accuracy_score, confusion_matrix
from flask import Flask,jsonify
from flask import request


#reading csv files

df = pd.read_csv('diseases_dataset\dataset.csv')
# print(df.head())
# df.describe()
df1 = pd.read_csv('diseases_dataset\Symptom-severity.csv')
# print(df1.head())



# Dataset Cleaning

df.isna().sum()
df.isnull().sum()

cols = df.columns
data = df[cols].values.flatten()

s = pd.Series(data)
s = s.str.strip()
s = s.values.reshape(df.shape)

df = pd.DataFrame(s, columns=df.columns)

df = df.fillna(0)
df.head()




# Encoding Symptoms with severity score

vals = df.values
symptoms = df1['Symptom'].unique()

for i in range(len(symptoms)):
    vals[vals == symptoms[i]] = df1[df1['Symptom'] == symptoms[i]]['weight'].values[0]
    
d = pd.DataFrame(vals, columns=cols)

d = d.replace('dischromic _patches', 0)
d = d.replace('spotting_ urination',0)
df = d.replace('foul_smell_of urine',0)
# df.head()




# seperate dependent and independent variables

# (df[cols] == 0).all()

# df['Disease'].value_counts()

# df['Disease'].unique()

data = df.iloc[:,1:].values
labels = df['Disease'].values




# model training

model = SVC()
model.fit(data, labels)





# # train-test split

# x_train, x_test, y_train, y_test = train_test_split(data, labels, shuffle=True, train_size = 0.85)
# print(x_train.shape, x_test.shape, y_train.shape, y_test.shape)

# model = SVC()
# model.fit(x_train, y_train)

# preds = model.predict(x_test)
# print(preds)



# # checking accuracy of our model

# conf_mat = confusion_matrix(y_test, preds)
# df_cm = pd.DataFrame(conf_mat, index=df['Disease'].unique(), columns=df['Disease'].unique())
# print('F1-score% =', f1_score(y_test, preds, average='macro')*100, '|', 'Accuracy% =', accuracy_score(y_test, preds)*100)




# receive json file of symptoms






# disease prediction

def predict_disease(patient_symptoms):

    #patient_symptoms=['itching', 'vomiting', 'fatigue', 'weight_loss', 'high_fever', 'yellowish_skin']
    patient_symptoms_encoded=[]

    for i in range(len(patient_symptoms)):
        patient_symptoms_encoded.append(df1[df1['Symptom'] == patient_symptoms[i]]['weight'].values[0])

    for j in range(17-len(patient_symptoms_encoded)):
        patient_symptoms_encoded.append(0)

    # print(patient_symptoms_encoded)

    disease_prediction=model.predict([patient_symptoms_encoded])
    return (disease_prediction)





# POST json with predictions
# GET json with symptoms

app = Flask(__name__)

@app.route("/",methods=['POST','GET'])

def  receive_symptoms():
    global patient_symptoms
    
    data = request.get_json("")
    patient_symptoms=data


def send_predictions():
    disease_prediction=predict_disease(patient_symptoms)[0]
    temp_df=pd.read_csv("diseases_dataset\severity.csv")
    estimated_doc_time=temp_df[temp_df.disease==disease_prediction]["time"].values[0]
    severity=temp_df[temp_df.disease==disease_prediction]["severity"].values[0]
    spec=temp_df[temp_df.disease==disease_prediction]["specialisation"].values[0]
    dic={"disease_prediction":disease_prediction,"estimated_doc_time":estimated_doc_time,"severity":severity,"specialization":spec}
    return jsonify(dic)

if __name__=="__main__":
    app.run(host='0.0.0.0', port=4000)