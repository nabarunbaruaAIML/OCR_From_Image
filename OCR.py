from os import listdir
from os.path import join
import os
import logging
from tqdm.auto import tqdm
import easyocr
import json
import numpy as np

# logging_str = "[%(asctime)s: %(levelname)s: %(module)s]: %(message)s"
log_dir = "logs"
# create_directory([log_dir])
os.makedirs(log_dir, exist_ok=True)


"""
The logging configurations are set here like logging level ,file name etc.
"""
logging.basicConfig(
    filename=os.path.join("logs", 'running_logs.log'), 
    level=logging.INFO, 
    format="[%(asctime)s: %(levelname)s: %(module)s]: %(message)s",
    filemode="a"
    )

"""
>> 1 >> This Stage gets OCR from Images.
"""
STAGE = 'OCR'

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=4,cls=NpEncoder)
    logging.info(f"json file saved at: {path}")

def main():
    list_of_files = listdir('Artifacts/memediff5k')
    N = len(list_of_files)
    ocr = easyocr.Reader(lang_list=['en'],model_storage_directory='Artifacts/EASYOCR_DIR')
    progress_bar = tqdm(range(N))
    lst_file = []
    lst_ocr_cordinates = []
    lst_ocr_txt = []
    lst_ocr_prob= []
    for key,file in enumerate(list_of_files):
        src = join('Artifacts\memediff5k', file) 
        ocr_result = ocr.readtext(src)
        for ocr_line in ocr_result:
            lst_file.append(file)
            lst_ocr_cordinates.append(ocr_line[0])
            lst_ocr_txt.append(ocr_line[1])
            lst_ocr_prob.append(ocr_line[2])
        progress_bar.update(1)
            
    Dict_File ={}
    Dict_File['File'] = lst_file
    Dict_File['OCR_Cordinate']= lst_ocr_cordinates
    Dict_File['OCR_Text']= lst_ocr_txt
    Dict_File['OCR_prob']= lst_ocr_prob
    save_json('Artifacts/Five_Thousand_Meme_json.json', Dict_File)
    

"""
    Main Function Execution
"""
if __name__ == '__main__':
    try:
        logging.info(f">>>>> {STAGE} started <<<<<")
        main()
        logging.info(f">>>>> {STAGE}  completed! <<<<<\n\n")
    except Exception as e:
        logging.exception(e)
        raise e