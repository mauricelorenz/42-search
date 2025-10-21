from flask import Flask, request, render_template
import requests

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("42-search.html")

@app.route("/result")
def result():
    with open("secret", "r") as f:
        cid = f.readline().strip()
        sec = f.readline().strip()
    get_token_url = "https://api.intra.42.fr/oauth/token"
    get_token_payload = f"grant_type=client_credentials&client_id={cid}&client_secret={sec}"
    get_token_response = requests.post(get_token_url, data=get_token_payload)
    token = get_token_response.json()["access_token"]
    campus = request.args["campus"].title()
    print(campus)
    get_campus_url = f"https://api.intra.42.fr/v2/campus?filter[name]={campus}"
    header = {"Authorization": f"Bearer {token}"}
    get_campus_response = requests.get(get_campus_url, headers=header)
    print(get_campus_response)
    if not get_campus_response.json():
        return render_template("42-result.html")
    campus_id = get_campus_response.json()[0]["id"]
    first_name = request.args["first_name"]
    get_users_url = f"https://api.intra.42.fr/v2/users?campus_id={campus_id}&filter[first_name]={first_name}"
    get_users_reponse = requests.get(get_users_url, headers=header)
    users = get_users_reponse.json()
    return render_template("42-result.html", users=users)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)