metrics:

mAP@0.5: 0.9063866352708074
mAP@0.5:0.95: 0.7796790248382182
Precision: [    0.96238]
Recall: [    0.79964]

model chosen: yolov8

tried to make annotations with segment anything and GroundingDino with text promts but failed due to lack of precision,
therefore decided to make manual annotation of a part of dataset with makesence.ai. trained model on that part of dataset.

applied colour inversion to half of train dataset as an augmentation, tried to teach model not to rely on colour. implemented by direct inverting images in folder
with python script.

choose to transform images to 640 pixels, trained for 60 epoch, each about 700 images, chosen randomly from full dataset.


link to model weights and validation data to rum metrics im script_metrics.py:
https://drive.google.com/drive/folders/1YoLl0dRGcngKc4QVjPEXb50Ed4XXiE6M?usp=drive_link

change weights and data paths to yours and run script

to run with conda env:
go to Documents/tbank
$conda env create -f requirements.yml
$conda activate validate-env
run script_metric.py

to run with venv:
with venv activated
$pip install ultralytics
run script_metric.py



to build and run docker:

go to Documents

$sudo docker build -t tbank-logo-detector .

$sudo docker run -p 8000:8000 tbank-logo-detector
