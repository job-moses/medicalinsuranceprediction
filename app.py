
from flask import Flask, redirect, render_template, url_for, request, session
import pickle
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
import numpy as np
import pandas as pd

app = Flask(__name__)
app.secret_key ='supersecretkey'
# Load the pre-trained model (with preprocessing pipeline)
with open('model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

@app.route('/')
def index():
    prediction = session.pop('prediction', None)
    return render_template('index.html' , prediction = prediction)

@app.route('/predict', methods=['GET','POST'])
def predict():
            try:
                    data = {
                        "age": [int(request.form['age'])],
                        "bmi": [float(request.form['bmi'])],
                        "children": [int(request.form['children'])],
                        "sex": [request.form['sex'].lower()],
                        "smoker": [request.form['smoker'].lower()],
                        "region": [request.form['region'].lower()]
                    }
                    df = pd.DataFrame(data)
                    pred = model.predict(df)
                    prediction = np.exp(pred)
                    session['prediction'] = round(prediction[0],4)
                    print(session['prediction'])
                    return redirect(url_for('index'))
            except Exception as e:
                error='please fill form appropriately'
                return render_template('index.html', error = error)
            
if __name__ == '__main__':
    app.run(debug=True)