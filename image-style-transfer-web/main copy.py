#app.py
from flask import Flask, flash, request, redirect, url_for, render_template
import urllib.request
import os
from werkzeug.utils import secure_filename
import collect_fea_style as cfs
import img_style_transform as ist

app = Flask(__name__)
 
UPLOAD_FOLDER_content = 'static/uploads/content'
UPLOAD_FOLDER_style = 'static/uploads/style'
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER_content'] = UPLOAD_FOLDER_content
app.config['UPLOAD_FOLDER_style'] = UPLOAD_FOLDER_style
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
 
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(file):
    file_content = file[0]
    file_style = file[1]
    file_cname = file_content.filename
    file_sname = file_style.filename
    a = '.' in file_cname and file_cname.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    b = '.' in file_sname and file_sname.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    return a & b
     
 
@app.route('/')
def home():
    return render_template('index.html')
 
@app.route('/', methods=['POST'])
def upload_image():
    print('get')
    if 'content-file' and 'style-file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    content_file = request.files['content-file']
    style_file = request.files['style-file']
    print('content name :',content_file.filename)
    print('style name :',style_file.filename)
    file = [content_file, style_file]
    if file[0].filename == '' or file[1].filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file):
        filename_content = secure_filename(file[0].filename)
        filename_style = secure_filename(file[1].filename)
        content_pure_name = filename_content.split('.')[0]
        style_pure_name = filename_style.split('.')[0]
        file[0].save(os.path.join(app.config['UPLOAD_FOLDER_content'], filename_content))
        file[1].save(os.path.join(app.config['UPLOAD_FOLDER_style'], filename_style))
        cfs.style_model_train(style_pure_name)
        ist.img_style_transform(content_pure_name,style_pure_name)
        #print('upload_image filename: ' + filename)
        flash('Image successfully uploaded and displayed below')
        content_path = app.config['UPLOAD_FOLDER_content']+ '/'+ filename_content
        style_path = app.config['UPLOAD_FOLDER_style'] +'/' + filename_style
        output_path = 'static/uploads/output/' + content_pure_name+'_'+style_pure_name +'.jpg'
        params = {
            'content': content_path,
            'style':style_path,
            'output' : output_path
        }
        return render_template('success.html', **params)
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)
 
if __name__ == "__main__":
    app.run()