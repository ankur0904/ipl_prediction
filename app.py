from flask import Flask, render_template, request, jsonify, redirect
import numpy as np
import pickle
import time
import pandas as pd

app = Flask(__name__)

model = pickle.load(open("pipe_new_3.pkl", "rb"))


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    data = {
        "batting_team": (request.form.get("batting_team")),
        "bowling_team": (request.form.get("bowling_team")),
        "city": (request.form.get("city")),
        "runs_left": (
            request.form.get("run_left")
        ),
        "balls_left": int(request.form.get("ball_left")),
        "wickets": int(request.form.get("wicket")),
        "total_run_x": int(request.form.get("runs")),
        "crr": float(request.form.get("crr")),
        "rrr": float(request.form.get("rrr")),
    }
    # data = {
    #     "batting_team": "Delhi Capitals",
    #     "bowling_team": "Sunrisers Hyderabad",
    #     "city": "Hyderabad",
    #     "runs_left": 32,
    #     "balls_left": 28,
    #     "wickets": 5,
    #     "total_run_x": 147,
    #     "crr": 7.5,
    #     "rrr": 6.25
    # }
   
    test = pd.DataFrame(data, index=[0])
    
    print(test)
   
    # print("----------------------", data_array)
    pred = model.predict(test)
    # time.sleep(5)
    print(pred)
    if pred == 1:
        return render_template("success.html")
    return render_template("failure.html")


@app.route("/success", methods=["GET"])
def success():
    return render_template("success.html")


@app.route("/failure", methods=["GET"])
def failure():
    return render_template("failure.html")


@app.route("/404", methods=["GET"])
def error():
    return render_template("404.html")


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def catch_all(path):
    return redirect("/404")


if __name__ == "__main__":
    app.run(debug=True)