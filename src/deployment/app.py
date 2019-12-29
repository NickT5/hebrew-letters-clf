from flask import Flask, render_template, request, url_for, redirect
from flask_bootstrap import Bootstrap
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


def get_hebrew_unicode(letter):
    hebrew_unicodes = {
        'alef': '&#1488;', 'bet': '&#64305;', 'vet': '&#1489;', 'gimel': '&#1490; ', 'dalet': '&#1491;',
        'he': '&#1492;', 'vav': '&#1493;', 'zayin': '&#1494;', 'chet': '&#1495;', 'tet': '&#1496;',
        'yod': '&#1497;', 'kaf': '&#64315;', 'kaf-final': '&#64314;', 'chaf': '&#1499; ', 'chaf-final': '&#1498;',
        'lamed': '&#1500;', 'mem': '&#1502; ', 'mem-final': '&#1501;', 'nun': '&#1504;', 'nun-final': '&#1503;',
        'samech': '&#1505;', 'ayin': '&#1506;', 'pei': '&#64324; ', 'pei-final': ' 	&#64323;', 'fei': '&#1508;',
        'fei-final': '&#1507;', 'tsade': '&#1510;', 'tsade-final': '&#1509;', 'quf': '&#1511;', 'reish': '&#1512; ',
        'shin': '&#64298;', 'sin': '&#64299;', 'tav': '&#1514;'
    }
    return hebrew_unicodes.get(letter).strip()  # todo insert default value if it can't find anything


@app.route("/", methods=['GET', 'POST'])
def index():

    return render_template("index.html")


@app.route("/classify", methods=['POST'])
def classify():
    if 'file' in request.files:
        img_file = request.files.get('file')
        img_name = img_file.filename

        # Save image in a tmp folder.
        p = os.path.join(app.config['UPLOAD_FOLDER'], img_name)
        img_file.save(p)

        # Make a prediction.
        prediction = predict(p, img_name)
        prediction, _ = str(prediction).split('-')  # e.g. alef-1 --> alef

        hebrew_char = get_hebrew_unicode(prediction)

        # Delete image from tmp folder.
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], img_name))

    else:
        print("error")
        # todo render error page?

#    return redirect(url_for('index'))
    return render_template("index.html", prediction=prediction, hebrew_char=hebrew_char)


if __name__ == '__main__':
    app.run(debug=True)