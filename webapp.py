from flask import Flask, render_template, request, jsonify
import json
import os
from ibm_watson import VisualRecognitionV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

app = Flask(__name__)

key = 'V_bxV6yd3a1OI8ncXSaOhH7LtwdYwyJAStbzmJ90sLEV'
url = 'https://api.us-south.visual-recognition.watson.cloud.ibm.com/instances/cc3f29ef-b536-466d-8905-430bb6d3007a'

# key = 'T39bM1y9K31P70qukU99a0tSF13pVgCn-wqCNGjvQmWP'
# url = 'https://api.us-south.visual-recognition.watson.cloud.ibm.com/instances/4ece07d7-cbbc-4d7b-b639-395b35d938ab'

authenticator = IAMAuthenticator(key)
visual_recognition = VisualRecognitionV3(version='2018-03-19', authenticator=authenticator)
visual_recognition.set_service_url(url)


@app.route("/")
def index():
    return render_template("index.html")


@app.route('/upload', methods=["GET", 'POST'])
def uploadLabel():
    isthisFile = request.files.get('file')
    print(isthisFile)
    print(isthisFile.filename)
    isthisFile.save("./uploads/" + isthisFile.filename)
    classified = jsonify(classify(isthisFile.filename))
    os.remove("./uploads/" + isthisFile.filename)
    return classified


def classify(filename):
    with open('./uploads/' + filename, 'rb') as images_file:
        classes = visual_recognition.classify(images_file=images_file, threshold='0.6', owners=["me"]).get_result()
        print(json.dumps(classes, indent=2))
        try:
            return classes['images'][0]['classifiers'][0]['classes']
        except:
            return None


if __name__ == "__main__":
    app.run(debug=True)
    # with open('./uploads/2.png', 'rb') as images_file:
    #     classes = visual_recognition.classify(images_file=images_file, threshold='0.6', owners=["me"]).get_result()
    #     print(json.dumps(classes, indent=2))
