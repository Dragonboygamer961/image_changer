# Program to Upload Color Image and convert into Black & White image
import os
from flask import  Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import cv2
import numpy as np

app = Flask(__name__)

# Open and redirect to default upload webpage
@app.route('/')
def load_form():
    return render_template('upload.html')


# Function to upload image and redirect to new webpage
@app.route('/gray', methods=['POST'])
def upload_image():
    operation_selection = request.form["image_type_selection"]
    
    file = request.files['file']
    
    filename = secure_filename(file.filename)

    reading_file_data = file.read()

    image_array = np.fromstring(reading_file_data, dtype='uint8')
    
    decode_array_to_img = cv2.imdecode(image_array,cv2.IMREAD_UNCHANGED)
    
    if operation_selection =='gray':
        file_data = make_grayscale(decode_array_to_img)
    elif operation_selection == 'sketch':
        file_data = image_sketch(decode_array_to_img)
    elif operation_selection == 'oil_painting':
        file_data = image_oil_painting(decode_array_to_img)
    elif operation_selection == 'rgb':
        file_data = image_rgb(decode_array_to_img)
    elif operation_selection == 'water_painting':
        file_data = image_water_painting(decode_array_to_img)
    elif operation_selection == 'inverted':
        file_data = image_inverted(decode_array_to_img)
    elif operation_selection == 'hdr':
        file_data = image_hdr(decode_array_to_img)
    else:
        print('No image selected')

    

    
    with open(os.path.join('static/', filename),
              'wb') as f:
        f.write(file_data)

    display_message = 'Image successfully uploaded and displayed below'
    return render_template('upload.html', filename=filename, message = display_message)



def make_grayscale(decode_array_to_img):

    # Make grayscale
    converted_gray_img = cv2.cvtColor(decode_array_to_img, cv2.COLOR_RGB2GRAY)
    status, output_image = cv2.imencode('.PNG', converted_gray_img)
    print('Status:',status)

    return output_image

def image_sketch(decode_array_to_img):
    converted_gray_img = cv2.cvtColor(decode_array_to_img, cv2.COLOR_RGB2GRAY)

    sharping_gray_img = cv2.bitwise_not(converted_gray_img)

    blur_img = cv2.GaussianBlur(sharping_gray_img, (111,111), 0)

    sharping_blur_img = cv2.bitwise_not(blur_img)

    sketch_img = cv2.divide(converted_gray_img,sharping_blur_img,scale=256.0)

    status, output_img = cv2.imencode('.PNG',sketch_img)

    return output_img
#oil painting starts here
def image_oil_painting(decode_array_to_img):
    oil_effect_img = cv2.xphoto.oilPainting(decode_array_to_img, 7,1)
    status, output_img = cv2.imencode('.PNG',oil_effect_img)

    return output_img
#oil painting ends here and rgb start here
def image_rgb(decode_array_to_img):
    rgb_effect_img = cv2.cvtColor(decode_array_to_img, cv2.COLOR_BGR2RGB)
    status, output_img = cv2.imencode('.PNG',rgb_effect_img)

    return output_img
#rgb ends here

def image_water_painting(decode_array_to_img):
    water_painting_img = cv2.stylization(decode_array_to_img, sigma_s=8, sigma_r=0.7)
    status, output_img = cv2.imencode('.PNG',water_painting_img)

    return output_img

def image_inverted(decode_array_to_img):
    inverted_img = cv2.bitwise_not(decode_array_to_img)
    status, output_img = cv2.imencode('.PNG',inverted_img)

    return output_img

def image_hdr(decode_array_to_img):
    hdr_effect = cv2.detailEnhance(decode_array_to_img, sigma_s=11000, sigma_r=1)
    status, output_img = cv2.imencode('.PNG',hdr_effect)

    return output_img

@app.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename=filename))



if __name__ == "__main__":
    app.run()


