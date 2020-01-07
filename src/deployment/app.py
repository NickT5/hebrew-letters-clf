from flask import Flask, render_template, request, url_for, redirect, session
from flask_bootstrap import Bootstrap
from fastai.vision import *
import base64
import cv2


app = Flask(__name__)
Bootstrap(app)
app.config['UPLOAD_FOLDER'] = 'static/img/tmp'
app.secret_key = "SUpeR SeCREt KeY" #todo put this in a env file and load that file in app.py

# STATE variables
STATE_START = 0
STATE_READY_2_PREDICT = 1
STATE_PREDICTION_DONE = 2


def predict(p):
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
    # Get STATE.
    if 'state' in session:
        state = session['state']
    else:
        state = STATE_START
        session['state'] = state

    # Handle according to the STATE.
    if state == STATE_START:
        pass
    elif state == STATE_READY_2_PREDICT:
        pass
    elif state == STATE_PREDICTION_DONE:
        prediction = session.get('prediction')
        hebrew_char = session.get('hebrew_char')
        if prediction is None or hebrew_char is None:
            return render_template('index.html', prediction="Something went wrong.", hebrew_char="")
        else:
            return render_template('index.html', prediction=prediction, hebrew_char=hebrew_char)
    else:
        print("Impossible state")

    return render_template("index.html")


@app.route("/classify", methods=['POST'])
def classify():
    if request.files['file'].filename == '':
        return redirect(url_for('index'))
        # todo render error page?
    else:
        # Get input image.
        img_file = request.files.get('file')
        img_name = img_file.filename

        # Save image in a tmp folder.
        img_p = os.path.join(app.config['UPLOAD_FOLDER'], img_name)
        img_file.save(img_p)

        # Save image path to session.
        session["img"] = img_p

        # Make a prediction.
        prediction = predict(img_p)

        # Get unicode of prediction.
        prediction, _ = str(prediction).split('-')  # e.g. alef-1 --> alef
        hebrew_char = get_hebrew_unicode(prediction)

        # Set prediction, unicode and state in session.
        session['prediction'] = prediction
        session['hebrew_char'] = hebrew_char
        session['state'] = STATE_PREDICTION_DONE

    return redirect(url_for('index'))


@app.route("/reset")
def reset():
    if 'img' in session:
        img_p = session['img']

        # Delete image from tmp folder.
        # todo maybe delete all image files in the dir instead one.
        os.remove(img_p) if os.path.isfile(img_p) else print("File is already deleted.")

        # Clear cache.
        session.clear()

    return redirect(url_for('index'))


@app.route('/draw')
def draw():
    return render_template('draw.html')


@app.route('/getdrawing', methods=['POST'])
def getdrawing():
    # Get the data from the post request (data a is base64 encoded string).
    print(request.form.get('drawing').replace("data:image/png;base64,", ""))
    img64 = request.form.get('drawing').replace("data:image/png;base64,", "")

    # Decode base64 string and save it as an image on our filesystem.
    img_p = os.path.join(app.config['UPLOAD_FOLDER'], "drawing.jpg")
    with open(img_p, "wb") as fh:
        fh.write(base64.decodebytes(img64.encode()))

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
