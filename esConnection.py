from flask import Flask, render_template, request
from elasticsearch import Elasticsearch

INDEX_NAME = 'maritime_accidents'
TYPE_NAME = 'document'
USERNAME = 'elastic'
PASSWORD = 'kVadsXwpJLKtIB7m4hlajnED'
es = Elasticsearch('https://35a530cd680844118e0642de8fc07b63.us-central1.gcp.cloud.es.io',
                   http_auth=(USERNAME, PASSWORD), scheme='https', port=9243, timeout=1000)

query = "lampedusa migrant shipwreck"
topDocs = []
scoredDocs = []
name = "saiesh"
queryId = "1"

app = Flask(__name__)

#Default
@app.route("/", methods = ["POST", "GET"])
def home():
    with open("./qreldata/qrelsaiesh.txt", "r") as file:
        for eachLine in file:
            data = eachLine.split()
            scoredDocs.append(data[2])
    file.close()
    res = [i for i in topDocs if i['docId'].replace("%26","&") not in scoredDocs]
    return render_template("assesment.html", docs=res, query=query, scoredDocs=scoredDocs)

# @app.route("/evaluateDocs", methods = ["POST", "GET"])
# def evaluateDocs():
#     with open("./qreldata/qrelsaiesh.txt", "r") as file:
#         for eachLine in file:
#             data = eachLine.split()
#             scoredDocs.append(data[2])
#     file.close()
#     return render_template("assesment.html", docs = topDocs, query = query, scoredDocs = scoredDocs)

@app.route("/score", methods = ["GET"])
def scoreDocument():
    global scoredDocs
    docId = request.args.get("id")
    print(docId)
    score = request.args.get("score")
    print(score)
    with open("./qreldata/qrelsaiesh.txt","a") as file:
        l = "\n" + queryId + " " + name +" "+ docId.replace("%26","&") + " " + str(score)
        file.write(l)
    file.close()
    scoredDocs.clear()
    with open("./qreldata/qrelsaiesh.txt", "r") as file:
        for eachLine in file:
            data = eachLine.split()
            scoredDocs.append(data[2])
    file.close()
    res = [i for i in topDocs if i['docId'].replace("%26","&") not in scoredDocs]
    return render_template("assesment.html", docs=res, query=query, scoredDocs = scoredDocs)

def getResults():
    global topDocs
    body = {
        "query": {
            "query_string": {
                "default_field": "text",
                "query": query
            }
        },
        "size": 200
        , "_source": ["text", "id"]
    }

    esResult = es.search(index=INDEX_NAME, body= body)

    for result in esResult["hits"]["hits"]:
        temp = {}
        temp["id"] = result["_source"]["id"]
        temp["text"] = result["_source"]["text"]
        temp["docId"] = str(result["_id"]).replace("&","%26")
        topDocs.append(temp)

    print(len(topDocs))

getResults()

if __name__ == "__main__":
    app.run(debug= True)