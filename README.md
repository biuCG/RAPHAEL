# RAPHAEL

Recognition of race bib number in image crops (previously cut by YOLO detect.py) 

To run 
python3 main.py --inpath path/of/crops/ --output_file output_results.csv --thres 0.5

Returns a csv file with:
image name
indicator : 0,1,2 --> 0 no dorsal detected, 1 at least one dorsal detected but bib number not identified, 2 dorsal detected and bib number recognized
bib numbers detected in the image: type list
condifence of recognitions: type list
confidence of detected dorsals: type list

