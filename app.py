from flask import Flask, render_template, jsonify, request, make_response
from flask_cors import CORS
import models
import os, subprocess


app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    # os.chdir(os.path.dirname(__file__))
    # print(os.getcwd())
    return "Hello, World from Atif! -> " + os.getcwd() + "->" + str(os.path.exists('/home/site/wwwroot/flops')) + "->" + str(os.path.exists('/home/site/repository/'))


@app.route('/aircadia')
def aaa():
    return "Hello, AirCADia!"



@app.route('/ExecuteModel', methods=["POST"])
def ExecuteModels():
	if request.is_json:
		req_json = request.get_json()

		modelName = req_json.get("ModelName")
		print(req_json["ModelName"])
		args = ()
		for input in req_json["Inputs"]:
			print(str(input["Name"]) + " = " + str(input["Value"]))
			args += (float(input["Value"]),)
		
		outputs = ()
		for output in req_json["Outputs"]:
			print(str(output["Name"]) + " = " + str(output["Value"]))
			outputs += (output["Value"],)
		
		y1 = getattr(models, modelName)(*args)
		print(y1)

		response_body = {
            "ModelName": modelName,
			"Inputs": [],
			"Outputs": []
        }
		for input in req_json["Inputs"]:
			response_body["Inputs"].append({"Name": input["Name"], "Value": input["Value"]})
		for output in req_json["Outputs"]:
			response_body["Outputs"].append({"Name": output["Name"], "Value": y1})

		res = make_response(jsonify(response_body), 200)
		return res
	else:
		print("Error")
		return make_response(jsonify({"Message": "Request body must be JSON"}), 400)    

if __name__ == '__main__':
    app.run(debug=True)