from flask import Flask, request, render_template
import requests
# import urllib.parse

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("42-search.html")

@app.route("/result")
def result():
    with open("secret", "r") as f:
        cid = f.readline().strip()
        sec = f.readline().strip()

    token_url = "https://api.intra.42.fr/oauth/token"
    token_payload = f"grant_type=client_credentials&client_id={cid}&client_secret={sec}"
    token_response = requests.post(token_url, data=token_payload)
    token = token_response.json()["access_token"]

    campus = request.args["campus"].title()
    # campus_encoded = urllib.parse.quote(campus)
    campus_url = f"https://api.intra.42.fr/v2/campus?filter[name]={campus}"
    header = {"Authorization": f"Bearer {token}"}
    campus_response = requests.get(campus_url, headers=header)

    if not campus_response.json():
        return render_template("42-result.html")
    campus_id = campus_response.json()[0]["id"]
    first_name = request.args["first_name"]
    # first_name_encoded = urllib.parse.quote(first_name)
    users_url = f"https://api.intra.42.fr/v2/users?campus_id={campus_id}&filter[first_name]={first_name}"
    users_response = requests.get(users_url, headers=header)

    users = users_response.json()
    return render_template("42-result.html", users=users)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)