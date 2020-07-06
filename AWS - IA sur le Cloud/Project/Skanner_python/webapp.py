import os
from flask import Flask, flash, request, redirect, url_for, jsonify
from flask_ngrok import run_with_ngrok
from template_html import html
from werkzeug.utils import secure_filename
import time
import numpy as np
import tensorflow.compat.v2 as tf
from skimage.io import imread
from skimage.transform import resize

UPLOAD_FOLDER = './uploads/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
run_with_ngrok(app)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image = os.path.dirname(os.path.realpath(__file__)) + "/uploads/" + filename
            result = get_prediction(image)
            redirect(url_for('upload_file', filename=filename))
            return html(result)
    return html("")


def get_prediction(image):
    start = time.time()

    ## USE TO SAVE MODEL AND READ WITH TENSORFLOW <1.14
    # model = tf.keras.models.load_model('model_aws.h5')
    # model.save_weights("weights_only.h5")
    # # Save model config
    # json_config = model.to_json()
    # with open('model_config.json', 'w') as json_file:
    #     json_file.write(json_config)

    with open('model_config.json') as json_file:
        json_config = json_file.read()
    model = tf.keras.models.model_from_json(json_config)

    # # Load weights
    model.load_weights('weights_only.h5')

    def resize100(img):
        return resize(img, (224, 224), preserve_range=True, mode='reflect', anti_aliasing=True)

    image = resize100(imread(image))/255

    t = model.predict(np.expand_dims(image, 0))[0]

    ###WITH TENSORFLOW >1.15
    # arr = tf.keras.preprocessing.image.load_img(image)
    # arr = tf.keras.preprocessing.image.img_to_array(arr) / 255
    # image = tf.image.resize(arr, size=[224, 224])
    # t = model.predict(np.expand_dims(image, axis=0))[0]

    print('The prediction is ' + str(np.argmax(t)) + ' with a precision of ' + str(round(t[np.argmax(t)] * 100, 2)) + "%")
    print('The job ended after ' + str(round(time.time() - start, 0)) + ' seconds')
    return np.argmax(t)


if __name__ == "__main__":
    app.run()


