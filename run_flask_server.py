import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {"zip", "pdf"}

host = "127.0.0.1"
port = 5000


app = Flask(__name__)

app.config['SECRET_KEY'] = 'kjadfnkvjadfn'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/menu")
def menu():
    return render_template("menu.html")

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        uploaded_files = request.files.getlist("file")
        print(len(uploaded_files), uploaded_files)
     
        for file in uploaded_files:
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                if filename.endswith("pdf"):
                    file.save(os.path.join('./Pliki/', filename))
                else:
                    file.save(os.path.join('./Input/', filename))

        # return redirect(url_for('upload_file', name=filename))
    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True, host=host, port=port)