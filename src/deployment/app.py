from flask import Flask, render_template, request, url_for, redirect
from flask_bootstrap import Bootstrap
from fastai import *
from fastai.vision import *


app = Flask(__name__)
Bootstrap(app)
app.config['UPLOAD_FOLDER'] = './tmp'


def predict(p, img_name):
    path = Path(p)
    img = open_image(path)

    # Load model
    learner = load_learner(Path('../model'))

    # Make prediction
    predicted_class, predicted_label, predicted_probs = learner.predict(img)

    return predicted_class


@app.route("/", methods=['GET', 'POST'])
def index():

    return render_template("index.html")


@app.route("/classify", methods=['POST'])
def classify():
    if 'file' in request.files:
        print('hooray')
        img_file = request.files.get('file')
        img_name = img_file.filename

        # Save image in a tmp folder.
        p = os.path.join(app.config['UPLOAD_FOLDER'], img_name)
        img_file.save(p)

        # Make a prediction.
        prediction = predict(p, img_name)
        print("prediction: ", prediction)

        # Delete image from tmp folder.
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], img_name))

    else:
        print("error")

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)