from flask import Flask, render_template, send_file, request
from rembg import remove
import os
from uuid import uuid4

app = Flask(__name__)
app.config['PRE'] = 'static/temporal_files/pre'
app.config['POST'] = 'static/temporal_files/post'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return render_template('index.html')
    return render_template('index.html')

@app.route('/remove-bg', methods=['GET', 'POST'])
def remove_bg():
    if request.method == 'POST':
        image_file = request.files['image']
        image_filename = image_file.filename
        ex = os.path.splitext(image_filename)[1]
        id = str(uuid4())
        new_filename = f"{id}{ex}"
        path = os.path.join(app.config['PRE'], new_filename)
        image_file.save(path)

        new_path = os.path.join(app.config['POST'], new_filename)
        with open(path, 'rb') as i:
            with open(new_path, 'wb') as o:
                input = i.read()
                new_image = remove(input)
                o.write(new_image)

        return render_template('remove-bg.html', name = new_filename)
    
    return render_template('remove-bg.html')

@app.route('/download/<filename>')
def download(filename):
    path = os.path.join(app.config['POST'], filename)
    return send_file(path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)