import sys
_CAFFE_ROOT = "../../caffe-crfrnn/"
sys.path.insert(0, _CAFFE_ROOT + "python")
import caffe
import numpy as np
import cv2
import numpy.random as random

class DataLayer(caffe.Layer):

    def setup(self, bottom, top):

        self.imgdir = "/home/nd-archi/Documents/playground/play_caffe/real_crfasrnn/crfasrnn/cunet-model/train/images/"
        self.maskdir = "/home/nd-archi/Documents/playground/play_caffe/real_crfasrnn/crfasrnn/cunet-model/train/masks/"
        self.imgtxt = "/home/nd-archi/Documents/playground/play_caffe/real_crfasrnn/crfasrnn/cunet-model/img.txt"
        self.random = True
        self.seed = None

        if len(top) != 2:
            raise Exception("Need to define two tops: data and mask.")

        if len(bottom) != 0:
            raise Exception("Do not define a bottom.")

        self.lines = open(self.imgtxt, 'r').readlines()
        self.idx = 0

        if self.random:
            random.seed(self.seed)
            self.idx = random.randint(0, len(self.lines) - 1)

    def reshape(self, bottom, top):
        # load image + label image pair
        self.data = self.load_image(self.idx)
        self.mask = self.load_mask(self.idx)
        # reshape tops to fit (leading 1 is for batch dimension)
        top[0].reshape(*self.data.shape)
        top[1].reshape(1, *self.mask.shape)

    def forward(self, bottom, top):
        # assign output
        top[0].data[...] = self.data
        top[1].data[...] = self.mask

        # pick next input
        if self.random:
            self.idx = random.randint(0, len(self.lines) - 1)
        else:
            self.idx += 1
            if self.idx == len(self.lines):
                self.idx = 0

    def backward(self, top, propagate_down, bottom):
        pass

    def load_image(self, idx):

        imname = self.imgdir + self.lines[idx]
        imname = imname[:-1]
        #print 'load img %s' %imname
        im = cv2.imread(imname)
	im = im[:, :, ::-1]
        #im = cv2.imread(imname)
        print im.shape
        #im = cv2.resize(im,(3,512,512))
        #im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        im = np.array(im, np.float32)
        im = np.resize(im,(3,512,512))
	im /= 255.0
        im -= 0.5
        return im[np.newaxis, :]

    def load_mask(self, idx):
	outimg = np.empty((2,512,512))
        imname = self.maskdir + self.lines[idx]
        imname = imname[:-5]+'_mask.png'
        #print 'load mask %s' %imname
        im = cv2.imread(imname)
        im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
	im = cv2.resize(im,(512,512))
        ret, img = cv2.threshold(im, 0.5, 1.0, cv2.THRESH_BINARY)
	#ret, back = cv2.threshold(im, 0.5, 1.0, cv2.THRESH_BINARY_INV)
	#outimg[0, ...] = img;
	#outimg[1, ...] = back;
	#outimg.astype(np.uint8)
        return img[np.newaxis, :]
