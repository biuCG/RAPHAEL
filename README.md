# RAPHAEL

Recognition of race bib number in images (previously dorsal detection by YOLO detect.py) 

YOLO optional parameters: 
python3 detect.py --weights weights.pt --img 640 --conf 0.25 --source path/input/images --save-conf --save-crop --save-txt --project path/outs/ --name name_folder

To run:

python3 main.py --inpath path/of/crops/ --output_file output_results.csv --thres 0.5

Returns a csv file with:

image name
indicator : 0,1,2 --> 0: no dorsal detected, 1: dorsal detected without number identified, 2: at least on number recongized.
bib numbers detected in the image: type list
condifence of recognitions: type list
confidence of detected dorsals: type list

