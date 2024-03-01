import os
import prediction
from flask import Flask, request, send_file, render_template, jsonify, redirect, url_for

app = Flask(__name__)

# Route for uploading and displaying image file
@app.route("/upload", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        # Check if the POST request has the file part
        if "file" not in request.files:
            return "No file part"
        file = request.files["file"]
        # If user does not select file, browser also
        # submit an empty part without filename
        if file.filename == "":
            return "No selected file"
        if file:
            # Save the file to a folder (you might want to secure this location)
            file_path = os.path.join("uploads", file.filename)
            file.save(file_path)
            # Construct URL for displaying image
            image_url = f"/display/{file.filename}"
            # Return HTML response with image URL
            return render_template("show_result.html", image_url=image_url, class_name=prediction.predict(file_path), filename=file.filename)
    elif request.method == "GET":
        return render_template("upload.html")  # Assuming you have an HTML template for the upload form


# Route for displaying image
@app.route("/display/<filename>")
def display_image(filename):
    return send_file(os.path.join("uploads", filename), mimetype='image/png')


# Route for deleting uploaded file
@app.route("/delete/<filename>", methods=["GET"])
def delete_file(filename):
    file_path = os.path.join("uploads", filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        # redirect
        return render_template('delete_confirmation.html', filename=filename, redirect_url=url_for('upload_file'))
    else:
        # if file not found
        return jsonify({"message": f"File {filename} does not exist"})

@app.route("/")
def hello_world():
    return render_template("index.html", upload_url=url_for("upload_file"))

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
