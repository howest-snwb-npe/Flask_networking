from flask import Flask, render_template, request
from netmiko import ConnectHandler
import json, requests
from ncclient import manager

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
    r = requests.get("https://192.168.0.119/restconf/data/Cisco-IOS-XE-native:native", 
                     auth=("k","Test123!"), headers=headers, verify=False)
    # print( r.text )
    # print( json.dumps(r.json(), indent=4) )
    output = json.dumps(r.json(), indent=4)
    return render_template("index.html", output=output)

@app.route("/netconf")
def netconf():
    netconf_filter = """
    <filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
        <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native" />
    </filter>
    """    
    with manager.connect(host="192.168.0.119", username="k", password="Test123!", device_params={'name':"iosxe"}) as m:
        # for capability in m.server_capabilities:
        #     print(capability)
        r = m.get_config('running', netconf_filter)

    output = r.xml
    return render_template("index.html", output=output)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)