import pandas as pd
import random

df=pd.read_csv("diseases_dataset\dataset.csv")
unique_diseases=(df.Disease.unique())

# print(unique_diseases)

d={'disease':unique_diseases,'severity':[],"time":[],"specialisation":[]}

high_severity=['Heart attack','Paralysis','Malaria','Dengue','Typhoid','Hepatitis A','Hepatitis B','Hepatitis C','Hepatitis D','Hepatitis E','Alcoholic hepatitis','Tuberculosis','Pneumonia','Dimorphic hemorrhoids (piles)','Varicose veins','Hypoglycemia']

spec={
'Fungal infection':'Dermatologist',
'Allergy': 'Allergist',
'GERD':'Gastroenterologist',
'Chronic cholestasis':'Gastroenterologist',
'Drug Reaction':'Dermatologist',
'Peptic ulcer diseae':'Gastroenterologist',
'AIDS':'Immunologist',
'Diabetes ':'Endocrinologist',
'Gastroenteritis':'Gastroenterologist',
'Bronchial Asthma':'Allergist',
'Hypertension ':'Cardiologist',
'Migraine':'Neurologist',
'Cervical spondylosis':'Neurologist',
'Paralysis (brain hemorrhage)':'Neurologist',
'Jaundice':'Gastroenterologist',
'Malaria':'General Physician',
'Chicken pox':'General Physician',
'Dengue':'General Physician',
'Typhoid':'General Physician',
'hepatitis A':'Gastroenterologis', 
'Hepatitis B':'Gastroenterologist',
'Hepatitis C':'Gastroenterologist',
'Hepatitis D':'Gastroenterologist',
'Hepatitis E':'Gastroenterologist',
'Alcoholic hepatitis':'Gastroenterologist',
'Tuberculosis':'Pulmonologist',
'Common Cold':'General Physician',
'Pneumonia':'Pulmonologist',
'Dimorphic hemmorhoids(piles)':'Proctologist',
'Heart attack':'Cardiologist',
'Varicose veins':'Dermatologist',
'Hypothyroidism':'Endocrinologist',
'Hyperthyroidism':'Endocrinologist',
'Hypoglycemia':'Endocrinologist',
'Osteoarthristis':'Rheumatologist',
'Arthritis':'Rheumatologist',
'(vertigo) Paroymsal  Positional Vertigo':'Neurologist',
'Acne':'Dermatologist',
'Urinary tract infection':'Urologist',
'Psoriasis':'Dermatologist',
'Impetigo':'Dermatologist'
}

for j in d['disease']:
    if j in high_severity:
        d['severity'].append("high")
    else:
        d['severity'].append("low")
    TIME=random.randint(10,40)
    d["time"].append(str(TIME)+"min")
    d["specialisation"].append(spec[j])
  

df2=pd.DataFrame(d)
df2.to_csv("diseases_dataset\severity.csv",index=True)