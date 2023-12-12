from flask import Flask, render_template, request
from netmiko import ConnectHandler

app = Flask(__name__)

@app.route("/")
def root():
    return render_template("index.html")

@app.route("/sendcommand")
def huppeldepup():
    commando = request.args.get("input")
    with ConnectHandler(host="192.168.0.119", username="k", password="Test123!", device_type="cisco_ios") as ch:
        output = ch.send_command(commando)
        print(output)
    return render_template("index.html", output=output)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)