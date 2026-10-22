"""Flask routes for hand-sign digit recognition."""

from flask import Flask, render_template, request

from model import preprocess_img, predict_result

app = Flask(__name__)


@app.route("/")
def main():
    """Render the image upload page."""
    return render_template("index.html")


@app.route("/prediction", methods=["POST"])
def predict_image_file():
    """Validate an uploaded image and render its predicted digit."""
    uploaded_file = request.files.get("file")

    if uploaded_file is None or not uploaded_file.filename:
        return render_template(
            "result.html",
            err="Please upload an image file.",
        ), 400

    try:
        image = preprocess_img(uploaded_file.stream)
    except (OSError, ValueError):
        return render_template(
            "result.html",
            err="File cannot be processed.",
        ), 400

    prediction = predict_result(image)
    return render_template("result.html", predictions=str(prediction))


if __name__ == "__main__":
    app.run(port=9000, debug=True)
