from flask import Flask, request, jsonify
import util

app = Flask(__name__)

@app.route('/')
def test():
    return "Hello"


@app.route("/get_location_names")
def get_location_names():
    response = jsonify({
        "location": util.get_location_names()
        })
    response.headers.add("Access-Control-Allow-Origin", "*")

    return response

@app.route('/predict_prop_price', methods=['GET', 'POST'])
def predict_home_price():
	bhk = int(request.form['BHK'])
	size = float(request.form['Size_In_Sqft'])
	n_bath = int(request.form['N_bath'])
	locn = request.form['Location']

	response = jsonify({
		'Net_Price' : util.get_estimated_price(locn, size, bhk, n_bath)
		})
	response.headers.add('Access-Control-Allow-Origin', '*')

	return response

if __name__ == '__main__':
    util.load_resources()
    print("Starting python server. Please wait!!!")
    app.run(debug= True)