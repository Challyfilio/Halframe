import yaml
from funs import *

if __name__ == '__main__':
    file = open('config.yml', 'r', encoding='utf-8')
    cfg = file.read()
    dict = yaml.safe_load(cfg)

    mode = dict['MODE']
    image_input_dir = dict['IMAGE_INPUT_DIR']
    temp_image_input_dir = dict['TEMP_IMAGE_INPUT_DIR']
    cut_single_filename = dict['CUT_SINGLE_FILENAME']
    temp_filename_1 = dict['TEMP_FILENAME_1']
    temp_filename_2 = dict['TEMP_FILENAME_2']
    tag_1, tag_2 = dict['STATE']['cut_rejoint'], dict['STATE']['black_bar']

    if mode == 'Cut_Batch':
        Cut_Process_batch(image_input_dir, cut_rejoint=tag_1, black_bar=tag_2)
    elif mode == 'Cut_Single':
        Cut_Process_single(image_input_dir, cut_single_filename, cut_rejoint=tag_1, black_bar=tag_2)
    elif mode == 'Joint':
        Joint_Process(temp_image_input_dir, temp_filename_1, temp_filename_2, black_bar=tag_2)
    else:
        pass
