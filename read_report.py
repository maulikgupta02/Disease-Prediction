import io
import pdfplumber
import re
from flask import Flask, request, jsonify
import pandas as pd

def extract_text(pdf_file):
  with pdfplumber.open(pdf_file) as pdf:
    text = ""
    for page in pdf.pages:
      text += page.extract_text()
    return text

def extract_details(text):
  test_pattern = r"([A-Za-z &()]+)\s+([\d.]+)\s+([a-zA-Z/]+)\s+([\d.-]+)\s+([- \d. -]+)"
  matches = re.findall(test_pattern, text)

  # Create a dictionary to store the results
  test_results = []

  # Extracted information
  for match in matches:
      test_name = match[0].strip()
      if test_name=="Total":
        continue
      result = float(match[1].strip())
      unit = match[2].strip()
      lower_limit = float(match[3].strip())
      upper_limit = float(match[4].strip()[2:])
      # print(match)

      temp = {
          "test_name":test_name,
          "result": result,
          "unit": unit,
          "lower_limit": lower_limit,
          "upper_limit": upper_limit
      }

      if test_name=="Glucose Fasting":
        if result > (lower_limit+upper_limit)/2:
          temp["disease"]="diabetes"
          df=pd.read_csv("exercises.csv")
          df2=pd.read_csv("food_items.csv")
          exercises=[str(i) for i in list(df[temp["disease"]].values)]
          for j in range(len(exercises)):
            if exercises[j]=='nan':
              exercises=exercises[:j]
              break
          temp["body_parts"]=exercises
          food_items=[str(i) for i in list(df2[temp["disease"]].values)]
          for j in range(len(food_items)):
            if food_items[j]=='nan':
              food_items=food_items[:j]
              break
          temp["food_items"]=food_items

      test_results.append(temp)

  return test_results


# print(extract_details((extract_text("sample_report.pdf"))))


app = Flask(__name__)

@app.route('/')
def index():
  return "Hello, World!"

@app.route('/extract', methods=['POST'])
def extract():
  if request.method == 'POST':
    pdf_file = request.files['pdf_file']
    text = extract_text(pdf_file)
    details = extract_details(text)
    return jsonify(details)

if __name__ == '__main__':
  app.run(debug=True)