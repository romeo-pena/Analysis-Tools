# Analysis-Tools
This Repository was used to do analysis on the results of the model (weighted stats and RGB color profiling) from the Model-Training-Testing project.

## Reading logs for weighted metrics
1. Once training is finished from the Model-Training-Testing project. we copy the `None.log.json` of the working directory of the model and analyze the files. However, we need to process the json file into two files manually.
    1. If you ran the `train.py` and `eval.py` scripts from the Model-Training-Testing project project, your `None.log.json` can be read into two parts: (1) the logs of the `train.py` and (2) the logs of the `eval.py`
    2. Manually copy `eval.py` logs from the `None.log.json` file into a new txt file found in this project. This is usually found near the end of the file denoted by a seperator `{}`
    3. Remove the `eval.py` logs from the `None.log.json` and copy the json file into this project
    4. Once complete you can run the `analyzelog.py` script and read the specific weighted metrics during trainig and evaluation. 
        - This script requires the use of a label directory - folder containing ground truth images, to find the specific weights of each class
    5. Example runscripts of the `analyzeog.py` command: 
        - `python analyzelog.py --log_file json/experiments/val/Synthia_val.txt --label_dir datasets/Cityscapes_256/labels`
        - `python analyzelog.py --log_file json/experiments/val/ST_val.txt --label_dir datasets/Cityscapes_256/labels`
        - The reason why we're using the Cityscapes labels in this example as our label directory is because the that is the target dataset we're evaluating in. 

## Analyzing the RGB Values of a dataset.
1. The `RGBAnalyzer.py` script was used to do analysis on a specific dataset for its color profile.
2. The script however is not as refined as the other scripts and will require manual code editing to read the specific datasets wanted. It reads files found in a `dataset` folder and outputs its analysis on the `figures` folder