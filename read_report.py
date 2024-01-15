import io
import pdfplumber
import re
from flask import Flask, request, jsonify

def extract_text(pdf_file):
  with pdfplumber.open(pdf_file) as pdf:
    text = ""
    for page in pdf.pages:
      text += page.extract_text()
    return text

def extract_details(text):
  # Extract patient name
  name = re.search(r"Patient Name: (.*?)\n", text).group(1)

  # Extract patient age
  age = re.search(r"Age: (.*?)\n", text).group(1)

  # Extract patient gender
  gender = re.search(r"Gender: (.*?)\n", text).group(1)

  # Extract date of birth
  dob = re.search(r"Date of Birth: (.*?)\n", text).group(1)

  # Extract lab tests
  tests = re.findall(r"Test Name: (.*?)\n", text)

  # Extract test results
  results = re.findall(r"Result: (.*?)\n", text)

  # Extract test units
  units = re.findall(r"Units: (.*?)\n", text)

  # Extract suitable range
  interval = re.findall(r"Bio. Ref. Interval: (.*?)\n", text)

  return {
      "name": name,
      "age": age,
      "gender": gender,
      "dob": dob,
      "tests": tests,
      "results": results,
      "units": units
  }

text=(extract_text("WM17S.pdf"))

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
        "result": result,
        "unit": unit,
        "lower_limit": lower_limit,
        "upper_limit": upper_limit
    }

    if test_name=="Glucose Fasting":
      if result > (lower_limit+upper_limit)/2:
        temp["disease"]="glucose"

    test_results.append(temp)

print(test_results)