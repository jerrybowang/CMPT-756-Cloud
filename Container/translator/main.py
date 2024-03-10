import os
import prediction
from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

# Route for the index page
@app.route("/")
def index():
    return render_template("index.html")

# Route for the text input page
@app.route("/input_text", methods=["GET", "POST"])
def input_text():
    if request.method == "POST":
        text = request.form['text']
        translated_text = prediction.translation_eng(text)  # Ensure you have defined this function
        return render_template("input_text.html", original_text=text, translated_text=translated_text)
    else:
        return render_template("input_text.html", original_text=None, translated_text=None)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
