#!/bin/bash
stage=0

num_colors=3
num_classes=9
train_image_size=256

epochs=300
batch_size=16
lr=0.01
momentum=0.9
dir=exp/all/fcn8s_resnet101_bce

. ./path.sh




if [ $stage -le 1 ]; then
  mkdir -p $dir/configs
  echo "$0: Creating core configuration and unet configuration"

  cat <<EOF > $dir/configs/core.config
  num_classes $num_classes
  num_colors $num_colors
EOF

fi


if [ $stage -le 2 ]; then
  echo "$0: Training the network....."
  python3 local/train_iou.py \
       --batch-size $batch_size \
       --momentum $momentum \
       --train-image-size $train_image_size \
       --epochs $epochs \
       --lr $lr \
       --loss bce \
       --alpha 1 \
       --arch fcn8_resnet101 \
       --log-freq 100 \
       --core-config $dir/configs/core.config \
       --visualize \
       --pretrain \
       --tensorboard \
       $dir
fi
