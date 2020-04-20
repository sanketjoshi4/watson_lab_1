from flask import Flask, render_template, request, jsonify
import json
import os
from ibm_watson import VisualRecognitionV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

uploads_dir = './uploads/'

credentials = {
    "apikey": "wGNsHglMIxNh4TRRhGhi3Z_Qq00vjUP5XsMRvXs4qolN",
    "iam_apikey_description": "Auto-generated for key e07331c4-1f0d-4f8f-8e12-3eac7ff6aaa6",
    "iam_apikey_name": "wdp-writer",
    "iam_role_crn": "crn:v1:bluemix:public:iam::::serviceRole:Writer",
    "iam_serviceid_crn": "crn:v1:bluemix:public:iam-identity::a/eed7635af9de4ec1a02ed80b7edae9dc::serviceid:ServiceId-e631cf1f-f238-4393-a68f-9788973a6924",
    "url": "https://api.us-south.visual-recognition.watson.cloud.ibm.com/instances/d85048a6-f9ab-4e85-a68b-994afcf9a2d0",
}

authenticator = IAMAuthenticator(credentials['apikey'])
visual_recognition = VisualRecognitionV3(version='2018-03-19', authenticator=authenticator)
visual_recognition.set_service_url(credentials['url'])

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route('/classify', methods=["GET", 'POST'])
def classify():
    file_obj = request.files.get('file')
    file_obj.save(uploads_dir + file_obj.filename)
    classified = jsonify(recognition(file_obj.filename))
    os.remove(uploads_dir + file_obj.filename)
    return classified


def recognition(filename):
    with open(uploads_dir + filename, 'rb') as images_file:
        classes = visual_recognition.classify(images_file=images_file, threshold=1e-3, owners=["me"]).get_result()
        print(json.dumps(classes, indent=2))
        try:
            return classes['images'][0]['classifiers'][0]['classes']
        except:
            return None


if __name__ == "__main__":
    app.run(debug=True)
