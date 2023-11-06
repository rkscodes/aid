import pickle
from flask import Flask
from flask import request
from flask import jsonify
from pathlib import Path

input_file = Path('assets/model.bin')

if input_file.is_file(): 
    with open(input_file, 'rb') as f:
        dv, model = pickle.load(f)
else: 
    print(f"model.bin not found at {input_file}")
    print(f"you might want to run predict.py first")

app = Flask("app")


@app.route('/predict', methods=['POST'])
def predict():
    patient = request.get_json()
    X = dv.transform(patient)

    y_pred = model.predict_proba(X)[0,1]

    diabetic = y_pred >= 0.5

    result = {
        'diabetic_proba' : float(y_pred),
        'diabetic' : bool(diabetic)
    }

    return jsonify(result)

@app.route('/', methods=['GET'])
def welcome(): 
    return "Hii welcome, please go to /predict route to get outcome"


if __name__ == "__main__": 
    app.run(debug=True, port=6969, host='0.0.0.0')
