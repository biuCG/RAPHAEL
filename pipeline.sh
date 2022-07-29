git clone https://github.com/ultralytics/yolov5  # clone
pip install -qr yolov5/requirements.txt

model=test_albumentation_60epochs
weights=weights_${model}.pt
image_path=data
out_path=test1
out_name=test1_${model}

python3 yolov5/detect.py --weights $weights --img 640 --conf 0.25 --source $image_path --save-conf --save-crop --save-txt --project $out_path --name $out_name

path=${out_path}/${out_name}/
res_file=results_${out_name}.csv
python3 main.py --inpath $path --output_file $res_file --thres 0.1
