from flask import Flask, jsonify, render_template

#Import our model class from gen.py.
from gen import Model

#Initialize our flask app.
app = Flask(__name__)

#Import our trained model!
model = Model("namegen-300.hdf5")

#Display the webpage at the root of our domain.
@app.route('/', methods=['GET'])
def home():
    return render_template('misnomers.html')

#This is the api that supplies the names form the model.
@app.route('/api', methods=['GET'])
def api_all():

    #Generate 5 names and then send as an array of JSON.
    values = []
    for x in range(5):
        values.append({"name":model.get_name()})

    response = jsonify(values)

    #I was having weird problems during development not being able to request the API, and this fixed them.
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response

#Run the app!
if __name__ == "__main__":
    app.run()
