import os
from flask import Flask, flash, request, redirect, url_for,send_from_directory, render_template
from werkzeug.utils import secure_filename
from os.path import join, dirname, realpath
from test_image import generate_image

# UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'uploads')
UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)

app.secret_key = "1mcc-ccm1"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/', methods=['GET', 'POST'])
def upload_file():

    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']

    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        ip_img_path ='static/uploads/'+filename

        MODEL_NAME = 'netG_epoch_4_300.pth'

        if request.form.get('DIV2K') == 'DIV2K':
            MODEL_NAME = 'netG_epoch_4_300.pth'
        elif  request.form.get('CELEB') == 'CELEB':
            MODEL_NAME = 'netG_epoch_4_28.pth'

        print('MODEL_NAME >>>>>>', MODEL_NAME)
        op_img_path = generate_image(ip_img_path,filename,MODEL_NAME)

        print('upload_image filename: ','static/uploads/'+filename)
        flash('Image successfully uploaded and displayed below')
        return render_template('index.html', filename=filename, genImg=op_img_path)
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)


@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)


@app.route('/displayip/<filename>')
def display_ip_image(filename):
    return redirect(url_for('static',filename='uploads/'+ filename), code=301)

@app.route('/displayop/<filename>')
def display_op_image(filename):
    return redirect(url_for('static',filename='downloads/'+ filename), code=301)
 
if __name__ == "__main__":
    app.run()