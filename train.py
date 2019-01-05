import sys
_CAFFE_ROOT = "../../caffe-crfrnn/"
sys.path.insert(0, _CAFFE_ROOT + "python")
import caffe

solver = ""
net = caffe.Net()
