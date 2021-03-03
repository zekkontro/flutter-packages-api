#!flask/bin/python
from bs4 import BeautifulSoup
import requests
from flask import Flask, jsonify
from flask import make_response
from flask import request

app = Flask(__name__, static_url_path='')

@app.route("/")
def home():
    return """ <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flutter Packages API</title>
</head>
<body>
    <h1>Flutter Packages API</h1>
    <br>
    <br>
    <p>With the Flutter packages api, you can get information about all dart and flutter packages.</p>
    <br>
    <br>
    <h3>Usage</h3>
    <p>"/flutter-packages/api/PACKAGE_NAME" - get package information</p>
</body>
</html>"""

@app.route('/flutter-packages/api/<string:getInput>', methods=['GET'])
def get_package_info(getInput):
    respose = requests.get("https://pub.dev/packages/" + getInput)
    scoreResponse = requests.get("https://pub.dev/packages/" + getInput +"/score")
    versionResponse = requests.get("https://pub.dev/packages/" + getInput + "/versions/")
    scoreSource = BeautifulSoup(scoreResponse.content, "html.parser")
    versionSource = BeautifulSoup(versionResponse.content, "html.parser")
    source = BeautifulSoup(respose.content, "html.parser")
    versionList = versionSource.find_all("td", attrs={"class" : "version"})
    scoreList = scoreSource.find_all("span", attrs= {"class" : "score-key-figure-value"}, limit=3)
    versionStrList = []
    package_license = source.find("h3", attrs={"class" : "title"}, string="License").find_next("p").contents[0]
    likeCount = ""
    pubPoint = ""
    popularity = ""
    for v in versionList:
        newVersion = v.find("a")
        versionStrList.append(newVersion.text)
    for e in scoreList:
        if(scoreList.index(e) == 0):
            likeCount = e.text
        if(scoreList.index(e) == 1):
            pubPoint = e.text

        if (scoreList.index(e) == 2):
            popularity = e.text + "%"
    totalData = {"package_name" : getInput, "package_description" : source.find("p", attrs={"class" : "detail-lead-text"}).text, "github_link": source.find("a", attrs={"class" : "link", "rel" : "ugc"}).get("href"), "package_author" : source.find("a", attrs={"rel" : "nofollow"}).text, "package-license" : str(package_license).replace(" (", ""), "package_versions" : versionStrList, "pub_point" : pubPoint, "like_count" : likeCount, "popularity" : popularity}
    return jsonify(totalData)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'HTTP 404 Error': 'The content you looks for does not exist. Please check your request.'}), 404)

if __name__ == '__main__':
    app.run(debug=True)#!flask/bin/python

#print("Package Name" + getInput)
#print("Package Description: " + source.find("p", attrs={"class" : "detail-lead-text"}).text)
#print("Package Github Link: " + source.find("a", attrs={"class" : "link", "rel" : "ugc"}).get("href"))
#print("Package Author: " + source.find("a", attrs={"rel" : "nofollow"}).text)
#for e in scoreList:
#   if(scoreList.index(e) == 0):
#      print("Package Likes: " + e.text)
#    if(scoreList.index(e) == 1):
#        print("Package Pub Points: " + e.text)

 #   if (scoreList.index(e) == 2):
 #       print("Package Popularity: " + e.text + "%")
#package_license = source.find("h3", attrs={"class" : "title"}, string="License").find_next("p").contents[0]
#print("Package License: " + str(package_license).replace(" (", ""))

#print("Package Versions: ")

#for v in versionList:
 #   newVersion = v.find("a")
  #  print(newVersion.text)



    
