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
            <title>Convert Imege 2 Pdf</title>
        <script>
            function readURL(input) {
                if (input.files && input.files[0]) {
                    var reader = new FileReader();
                    reader.onload = function(e) {
                    $('.image-upload-wrap').hide();
                    $('.file-upload-image').attr('src', e.target.result);
                    $('.file-upload-content').show();
                    $('.image-title').html(input.files[0].name);
                };
                reader.readAsDataURL(input.files[0]);
                } else {
                    removeUpload();}
                    }

                function removeUpload() {
                 $('.file-upload-input').replaceWith($('.file-upload-input').clone());
                 $('.file-upload-content').hide();
                 $('.image-upload-wrap').show();
                  }
                  $('.image-upload-wrap').bind('dragover', function () {
                        $('.image-upload-wrap').addClass('image-dropping');
                    });
                    $('.image-upload-wrap').bind('dragleave', function () {
                        $('.image-upload-wrap').removeClass('image-dropping');
                    });
        </script>
        <style>
        body {
                font-family: sans-serif;
                background-color: #eeeeee;
                }

                .file-upload {
                background-color: #ffffff;
                width: 600px;
                margin: 0 auto;
                padding: 20px;
                }

                .file-upload-btn {
                width: 100%;
                margin: 0;
                color: #fff;
                background: #1FB264;
                border: none;
                padding: 10px;
                border-radius: 4px;
                border-bottom: 4px solid #15824B;
                transition: all .2s ease;
                outline: none;
                text-transform: uppercase;
                font-weight: 700;
                }

                .file-upload-btn:hover {
                background: #1AA059;
                color: #ffffff;
                transition: all .2s ease;
                cursor: pointer;
                }

                .file-upload-btn:active {
                border: 0;
                transition: all .2s ease;
                }

                .file-upload-content {
                display: none;
                text-align: center;
                }

                .file-upload-input {
                position: absolute;
                margin: 0;
                padding: 0;
                width: 100%;
                height: 100%;
                outline: none;
                opacity: 0;
                cursor: pointer;
                }

                .image-upload-wrap {
                margin-top: 20px;
                border: 4px dashed #1FB264;
                position: relative;
                }

                .image-dropping,
                .image-upload-wrap:hover {
                background-color: #1FB264;
                border: 4px dashed #ffffff;
                }

                .image-title-wrap {
                padding: 0 15px 15px 15px;
                color: #222;
                }

                .drag-text {
                text-align: center;
                }

                .drag-text h3 {
                font-weight: 100;
                text-transform: uppercase;
                color: #15824B;
                padding: 60px 0;
                }

                .file-upload-image {
                max-height: 200px;
                max-width: 200px;
                margin: auto;
                padding: 20px;
                }

                .remove-image {
                width: 200px;
                margin: 0;
                color: #fff;
                background: #cd4535;
                border: none;
                padding: 10px;
                border-radius: 4px;
                border-bottom: 4px solid #b02818;
                transition: all .2s ease;
                outline: none;
                text-transform: uppercase;
                font-weight: 700;
                }

                .remove-image:hover {
                background: #c13b2a;
                color: #ffffff;
                transition: all .2s ease;
                cursor: pointer;
                }

                .remove-image:active {
                border: 0;
                transition: all .2s ease;
                }
        </style>
        </head>
        <body>


            
       
            <script class="jsbin" src="https://ajax.googleapis.com/ajax/libs/jquery/1/jquery.min.js"></script>
        <div class="file-upload">
         <form method=post enctype=multipart/form-data>
            <center><h1>Convert Image to PDF</h1></center>
            <button class="file-upload-btn" type="button" onclick="$('.file-upload-input').trigger( 'click' )">Add Image</button>

            <div class="image-upload-wrap">
                <input class="file-upload-input" type='file' name=file onchange="readURL(this);" accept="image/*" />
                <div class="drag-text">
                <h3>Drag and drop a file or select add Image</h3>
                </div>
            </div>
            <div class="file-upload-content">
                <img class="file-upload-image" src="#" alt="your image" />
                <div class="image-title-wrap">
                <button type="button" onclick="removeUpload()" class="remove-image">Remove <span class="image-title">Uploaded Image</span></button>
                </div>
            </div>
            <br>
            <center><input type=submit value=Convert></center>
        </form>
        <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-0402905678253589" crossorigin="anonymous"></script>
        </div>
             
 




        </body>
    </html>


    '''

@app.route('/download')
def download_file():
    path = './temp/file.pdf'  # Replace with the path to your file
    return send_file(path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
