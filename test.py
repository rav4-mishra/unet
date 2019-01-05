import sys
_CAFFE_ROOT = "../../caffe-crfrnn/"
sys.path.insert(0, _CAFFE_ROOT + "python")
import caffe

net = caffe.Net('train_val_test.prototxt', caffe.TEST)
print net.blobs['score'].data.shape
print net.blobs['crop5'].data.shape
