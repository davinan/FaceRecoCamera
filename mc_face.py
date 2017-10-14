import httplib, urllib, base64, json

params = urllib.urlencode({
    'subscription-key': "bb833d4f4cee49fc9d93f8dbd89649f0",
    'returnFaceAttributes': 'age,gender,glasses',

}) 
headers = {

    'Content-type': 'application/octet-stream',

}

def analyse(img):
    body = "" 
    filename = img
    f = open(filename, "rb")
    body = f.read()
    f.close()
    conn = httplib.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
    conn.request("POST", "/face/v1.0/detect?%s" % params, body, headers)
    response = conn.getresponse("")
    data = response.read()
    parsed = json.loads(data)
    # print(type(parsed))
    # print(data[0]["faceAttributes"]["age"])
    # print ("Response:")
    # print (json.dumps(parsed, sort_keys=True, indent=2))
    conn.close()
    temp = parsed[0]["faceAttributes"]
    return [temp["age"], str(temp["gender"]), str(temp["glasses"])]

if __name__ == "__main__":
    print(analyse("alex.jpg"))