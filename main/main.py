import numpy as np
import caffe as caffe
import matplotlib.pyplot as plt
import os
import skimage.color as color
from flask import Flask,url_for,render_template,request,send_from_directory,redirect
from werkzeug import secure_filename,SharedDataMiddleware
import scipy.ndimage.interpolation as sni

UPLOAD_FOLDER = './uploads/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
  return '.' in filename and \
    filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

#app.add_url_rule('/uploads/<filename>', 'uploaded_file',
 #                build_only=True)
#app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
#  '/uploads':  app.config['UPLOAD_FOLDER']
#})

plt.rcParams['figure.figsize'] = (12,6)

#(1)open the model first
gpu_id = 0
caffe.set_mode_gpu()
caffe.set_device(gpu_id)
net = caffe.Net('colorization_deploy_v0.prototxt','colorization_release_v0.caffemodel',caffe.TEST)
(H_in,W_in) = net.blobs['data_l'].data.shape[2:]
(H_out,W_out) = net.blobs['class8_ab'].data.shape[2:]
net.blobs['Trecip'].data[...] = 6/np.log(10)


@app.route('/',methods=['GET','POST'])
def upload_file():
  if request.method == 'POST':
    file = request.files['file']
    if file and allowed_file(file.filename):
      filename = secure_filename(file.filename)
      file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
      img_rgb = caffe.io.load_image(os.path.join(app.config['UPLOAD_FOLDER'],filename))
      img_lab = color.rgb2lab(img_rgb) # convert image to lab color space
      img_l = img_lab[:,:,0] # pull out L channel
      (H_orig,W_orig) = img_rgb.shape[:2] # original image size
      # create grayscale version of image (just for displaying)
      img_lab_bw = img_lab.copy()
      img_lab_bw[:,:,1:] = 0
      img_rgb_bw = color.lab2rgb(img_lab_bw)
      # resize image to network input size
      img_rs = caffe.io.resize_image(img_rgb,(H_in,W_in))
      img_lab_rs = color.rgb2lab(img_rs)
      img_l_rs = img_lab_rs[:,:,0]
      # show origin image,along with grayscale input
      img_pad = np.ones((H_orig,W_orig/10,3))
      # plt.imshow(np.hstack((img_rgb, img_pad, img_rgb_bw)))
      # plt.axis('off')
      # (3)Colorization time! Now it is time to run the network
      # plt.show()
      net.blobs['data_l'].data[0,0,:,:] = img_l_rs-50
      net.forward()

      ab_dec = net.blobs['class8_ab'].data[0,:,:,:].transpose((1,2,0))
      ab_dec_us = sni.zoom(ab_dec,(1.*H_orig/H_out,1.*W_orig/W_out,1))
      img_lab_out = np.concatenate((img_l[:,:,np.newaxis],ab_dec_us),axis=2)
      img_rgb_out = np.clip(color.lab2rgb(img_lab_out),0,1)

      plt.imsave("out.jpg",img_rgb_out)
      return 'wow,it\' amazing!'

  return render_template('index.html')

if __name__== '__main__':
  app.run(debug=True)

