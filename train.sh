#!/bin/sh
cd /home/nd-archi/Documents/playground/play_caffe/real_crfasrnn/crfasrnn/cunet-model/unet/
pwd
export PYTHONPATH=/home/nd-archi/Documents/playground/play_caffe/real_crfasrnn/crfasrnn/cunet-model/unet:$PYTHONPATH
/home/nd-archi/Documents/playground/play_caffe/real_crfasrnn/crfasrnn/caffe-crfrnn/build/tools/caffe train --solver=solver.prototxt
