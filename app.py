from flask import Flask, request, redirect, url_for, send_file, send_from_directory
import os
import fitz


app = Flask(__name__, static_url_path='/static')
UPLOAD_FOLDER = './temp/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
processing_file = False


def convert_to_pdf(file_path):
    try:
        print(file_path)
        # check that uploaded file is an image
        allowed_extensions = {'png', 'jpg', 'jpeg', 'bmp'}
        file_extension = os.path.splitext(file_path)[1][1:].lower()
        if file_extension not in allowed_extensions:
            raise Exception('File must be an image')

        # convert the uploaded file to PDF
        img = fitz.Document(file_path)
        pdf = fitz.Document()

        page = pdf.new_page(width=img[0].rect.width, height=img[0].rect.height)
        page.insert_image(fitz.Rect(0, 0, page.mediabox[2], page.mediabox[3]), stream=img[0].get_pixmap().tobytes())
        pdf_filename = os.path.splitext(file_path)[0] + '.pdf'
        pdf.save("./temp/file.pdf")
        # remove the original uploaded file
        os.remove(file_path)

        print(pdf_filename)
        return redirect(request.url + "/download")
    except Exception as e:
        # remove the uploaded file if there was an error
        os.remove(file_path)
        return str(e)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also submit an empty part without filename
        if file.filename == '':
            return redirect(request.url)
        if file:
            filename = file.filename
            # save the uploaded file
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            return convert_to_pdf(file_path)
    return '''
    <!doctype html>
    <html>
        <head>
            <title>Upload new File</title>
        </head>
        <body>
            <h1>Upload new File</h1>
            <form method=post enctype=multipart/form-data>
              <input type=file name=file>
              <input type=submit value=Upload>
            </form>
        </body>
    </html>
    '''

@app.route('/download')
def download_file():
    path = './temp/file.pdf'  # Replace with the path to your file
    return send_file(path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
