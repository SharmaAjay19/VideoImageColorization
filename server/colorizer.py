import numpy as np
import os
import skimage.color as color
import matplotlib.pyplot as plt
import scipy.ndimage.interpolation as sni
import caffe

caffe.set_mode_cpu()

class CaffeModel:
	def __init__(self):
		self.prototxt_file_path = "../models/colorization_deploy_v2.prototxt"
		self.caffe_model_file_path = "../models/colorization_release_v2.caffemodel"
		self.net = caffe.Net(self.prototxt_file_path, self.caffe_model_file_path, caffe.TEST)
		(self.H_in,self.W_in) = self.net.blobs['data_l'].data.shape[2:] # get input shape
		(self.H_out,self.W_out) = self.net.blobs['class8_ab'].data.shape[2:] # get output shape
		self.pts_in_hull = np.load('../resources/pts_in_hull.npy') # load cluster centers
		self.net.params['class8_ab'][0].data[:,:,0,0] = self.pts_in_hull.transpose((1,0)) # populate cluster centers as 1x1 convolution kernel

	def color_image(self, image_file_path, output_file_path):
		img_rgb = caffe.io.load_image(image_file_path)
		img_lab = color.rgb2lab(img_rgb) # convert image to lab color space
		img_l = img_lab[:,:,0] # pull out L channel
		(H_orig,W_orig) = img_rgb.shape[:2] # original image size
		# resize image to network input size
		img_rs = caffe.io.resize_image(img_rgb,(self.H_in,self.W_in)) # resize image to network input size
		img_lab_rs = color.rgb2lab(img_rs)
		img_l_rs = img_lab_rs[:,:,0]
		self.net.blobs['data_l'].data[0,0,:,:] = img_l_rs-50 # subtract 50 for mean-centering
		self.net.forward() # run network
		ab_dec = self.net.blobs['class8_ab'].data[0,:,:,:].transpose((1,2,0)) # this is our result
		ab_dec_us = sni.zoom(ab_dec,(1.*H_orig/self.H_out,1.*W_orig/self.W_out,1)) # upsample to match size of original image L
		img_lab_out = np.concatenate((img_l[:,:,np.newaxis],ab_dec_us),axis=2) # concatenate with original image L
		img_rgb_out = (255*np.clip(color.lab2rgb(img_lab_out),0,1)).astype('uint8') # convert back to rgb
		plt.imsave(output_file_path, img_rgb_out)