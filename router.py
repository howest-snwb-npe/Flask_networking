from flask import Flask, render_template, request
from netmiko import ConnectHandler
import json, requests

app = Flask(__name__)

@app.route("/")
def root():
    return render_template("index.html")

@app.route("/sendcommand")
def netmiko():
    commando = request.args.get("input")
    with ConnectHandler(host="192.168.0.119", username="k", password="Test123!", device_type="cisco_ios") as ch:
        output = ch.send_command(commando)
        print(output)
    return render_template("index.html", output=output)

@app.route("/restconf")
def restconf():
    headers = {"Accept": "application/yang-data+json"}
    r = requests.get("https://192.168.0.119/restconf/data/ietf-yang-library:modules-state", 
                     auth=("k","Test123!"), headers=headers, verify=False)
    print( r.text )
    print( json.dumps(r.json(), indent=4) )
    output = json.dumps(r.json(), indent=4)
    return render_template("index.html", output=output)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)