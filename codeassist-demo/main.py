# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from flask import Flask, render_template, request
import calendar

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home_page():
    return render_template("index.html")


@app.route("/convert", methods=["POST"])
def convert():
    number = request.form["number"]
    roman = calendar.number_to_roman(number)
    return render_template("convert.html", number=number, roman=roman)


@app.route("/temp_form", methods=["GET"])
def temp_form():
    direction = request.args.get("direction", "f2c")
    return render_template("temp_form.html", direction=direction)


@app.route("/convert_temp", methods=["POST"])
def convert_temp():
    try:
        temperature = float(request.form["temperature"])
        direction = request.form["direction"]
        
        if direction == "f2c":
            converted = (temperature - 32) * 5.0 / 9.0
            msg = f"{temperature}°F is {converted:.2f}°C"
        elif direction == "c2f":
            converted = (temperature * 9.0 / 5.0) + 32
            msg = f"{temperature}°C is {converted:.2f}°F"
        else:
            msg = "Invalid conversion direction selected."
    except ValueError:
        msg = "Invalid temperature entered."
        
    return render_template("convert_temp.html", msg=msg)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
