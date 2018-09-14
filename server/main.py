import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from colorizer import CaffeModel

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
model = CaffeModel()

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route('/')
def hello_world():
	return 'Hello, World!'

@app.route('/color', methods=['GET', 'POST'])
def upload_file():
	if request.method=='POST':
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['file']
		if file.filename == '':
			flash('No selected file')
			return redirect(request.url)
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			in_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
			out_file_name = filename.split(".")[0] + "_1." + filename.split(".")[1]
			out_file_path = os.path.join(app.config['UPLOAD_FOLDER'], out_file_name)
			file.save(in_file_path)
			model.color_image(in_file_path, out_file_path)
			return redirect(url_for('colored_file', filename=out_file_name))
	return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

@app.route('/colored/<filename>')
def colored_file(filename):
	return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
if __name__ == '__main__':
	app.run(host="0.0.0.0", port=3001)
