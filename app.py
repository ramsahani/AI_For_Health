from wsgiref import simple_server
import os
from flask import Flask, request,render_template
from flask_cors import cross_origin
import pickle


app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/',methods=['GET'])  # route to display the home page
@cross_origin()
def homePage():
    return render_template("index.html")
@app.route("/predict", methods=['POST'])
def index():
    if request.method=='POST':
        try:
            bmi=float(request.form['bmi'])
            insulin=float(request.form['insulin'])
            pregnancies=float(request.form['pregnancies'])
            bp=float(request.form['blood_pressure'])
            glucose=float(request.form['glucose'])
            skin_thicknes=float(request.form['skin_thickness'])
            dpf=float(request.form['diabetes_pedigree_Function'])
            age=float(request.form['age'])

            model=pickle.load(open('modelForPrediction.sav','rb'))
            scaler=pickle.load(open('standardScalar.sav','rb'))

            prediction=model.predict(scaler.transform([[pregnancies,glucose,bp,skin_thicknes,insulin,bmi,dpf,age]]))
            print('prediction is',prediction)
            if prediction[0]==1:
                res="POSITIVE"
            else:
                res='NEGATIVE'
            return render_template('results.html',prediction=res)
        except Exception as e:
            print("The Exception message is",e)
            return "something is wrong"
    else:
        return('index.html')

port = int(os.getenv("PORT"))
if __name__ == "__main__":
    # host = '0.0.0.0'
    # port = 5000
    # app.config.update(DEBUG=True)
    app.run(host='0.0.0.0', port=port)
    #httpd = simple_server.make_server(host, port, app)
    # print("Serving on %s %d" % (host, port))
    #httpd.serve_forever()