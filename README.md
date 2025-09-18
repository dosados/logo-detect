metrics:

mAP@0.5: 0.9063866352708074
mAP@0.5:0.95: 0.7796790248382182
Precision: [    0.96238]
Recall: [    0.79964]

model choden: yolov8

tried to make annotations with segment anything and GroundingDino with text promts but failed due to lack of precision,
therefore decided to make manual annotation of a part of dataset with makesence.ai

metrics are made by script_metrics.py

applied colour inversion to half of train dataset as an augmentation, tried to teach model not to rely on colour. implemented by direct inverting images in folder
with python script.

will add links to download dataset for metrics tests tomorrow.


to build and run docker:

$sudo docker build -t tbank-logo-detector .

$sudo docker run -p 8000:8000 tbank-logo-detector
