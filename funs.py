"""
Halframe相机照片填坑用
v2.0
2022/5/2
Challyfilio
"""
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import glob
from tqdm import tqdm


def Info(input_image):
    # print("shape=", input_image.shape)  # (h,w,c)
    height = input_image.shape[0]
    width = input_image.shape[1]
    if height >= width:
        layout = 'vertical'
    else:
        layout = 'horizontal'
    return layout, height, width


def get_file_basename(path: str) -> str:
    return os.path.splitext(os.path.basename(path))[0]


def CutAndSaveTemp(input_image, layout, height, width, basename):
    temp1 = temp2 = []
    if layout == 'vertical':
        height_half = int(height / 2)
        temp1 = input_image[:height_half, :]
        temp2 = input_image[height_half:, :]
    elif layout == 'horizontal':
        width_half = int(width / 2)
        temp1 = input_image[:, :width_half]
        temp2 = input_image[:, width_half:]
    else:
        pass
    Save_temp(basename, temp1, temp2)


def CutAndSaveTemp_WithBar(input_image, layout, basename, cut_rejoint=False, black_bar=False):
    if layout == 'vertical':
        temp1 = input_image[:1416, :]
        temp2 = input_image[1500:, :]
        if cut_rejoint:
            if black_bar:
                mask = np.zeros((64, temp1.shape[1], 3), np.uint8)
                result = np.vstack((np.vstack((temp1, mask)), temp2))
            else:
                result = np.vstack((temp1, temp2))
            Save_result(basename, result)
        else:
            Save_temp(basename, temp1, temp2)
    elif layout == 'horizontal':
        temp1 = input_image[:, :1416]
        temp2 = input_image[:, 1500:]
        if cut_rejoint:
            if black_bar:
                mask = np.zeros((temp1.shape[0], 64, 3), np.uint8)
                result = np.hstack((np.hstack((temp1, mask)), temp2))
            else:
                result = np.hstack((temp1, temp2))
            Save_result(basename, result)
        else:
            Save_temp(basename, temp1, temp2)
    else:
        pass


def Save_temp(basename: str, temp1, temp2):
    cv2.imwrite('temp/{}_t1.jpg'.format(basename), temp1)
    cv2.imwrite('temp/{}_t2.jpg'.format(basename), temp2)


def Cut_Process_batch(image_input_dir, cut_rejoint=False, black_bar=False):
    image_input_path = glob.glob(os.path.join(image_input_dir, '*.*'))
    assert (len(image_input_path) != 0)
    for path in tqdm(image_input_path):
        basename = get_file_basename(path)
        input = cv2.imread(path)
        layout, height, width = Info(input)
        if cut_rejoint:
            if black_bar:
                CutAndSaveTemp_WithBar(input, layout, basename, cut_rejoint, black_bar)
            else:
                CutAndSaveTemp_WithBar(input, layout, basename, cut_rejoint, black_bar)
        else:
            if black_bar:
                CutAndSaveTemp_WithBar(input, layout, basename, cut_rejoint, black_bar)
            else:
                CutAndSaveTemp(input, layout, height, width, basename)
    print('Done')


def Cut_Process_single(image_input_dir, filename, cut_rejoint=False, black_bar=False):
    path = image_input_dir + '/' + filename
    basename = get_file_basename(path)
    input = cv2.imread(path)
    layout, height, width = Info(input)
    if cut_rejoint:
        if black_bar:
            CutAndSaveTemp_WithBar(input, layout, basename, cut_rejoint, black_bar)
        else:
            CutAndSaveTemp_WithBar(input, layout, basename, cut_rejoint, black_bar)
    else:
        if black_bar:
            CutAndSaveTemp_WithBar(input, layout, basename, cut_rejoint, black_bar)
        else:
            CutAndSaveTemp(input, layout, height, width, basename)
    print('Done')


def Judge(input_image1, input_image2):
    global length
    joint_way = ''
    if input_image1.shape == input_image2.shape:  # (h,w,c)
        height = input_image1.shape[0]
        width = input_image1.shape[1]
        if height >= width:
            joint_way = 'horizontal'
            length = height
        else:
            joint_way = 'vertical'
            length = width
    else:
        print('Shape Not Match')
        exit()
    return joint_way, length


def ImageShow_Plt(image):
    b, g, r = cv2.split(image)
    image = cv2.merge([r, g, b])
    plt.imshow(image)
    plt.pause(0.001)  # 暂停一会儿显示图像


def JointAndSaveRes(input_temp1, input_temp2, joint_way, black_bar, length, basename):
    # print(basename)
    global result
    if joint_way == 'vertical':
        if black_bar:
            mask = np.zeros((64, length, 3), np.uint8)
            result = np.vstack((np.vstack((input_temp1, mask)), input_temp2))
        else:
            result = np.vstack((input_temp1, input_temp2))
    elif joint_way == 'horizontal':
        if black_bar:
            mask = np.zeros((length, 64, 3), np.uint8)
            result = np.hstack((np.hstack((input_temp1, mask)), input_temp2))
        else:
            result = np.hstack((input_temp1, input_temp2))
    else:
        pass
    ImageShow_Plt(result)
    Save_result(basename, result)


def Save_result(basename: str, result):
    dir_name = 'result'
    if not os.path.isdir(dir_name):
        os.makedirs(dir_name)
    cv2.imwrite('result/{}.jpg'.format(basename), result)
    print('Image Save Finish')


def Joint_Process(temp_image_input_dir, filename1, filename2, black_bar=False):
    path1 = temp_image_input_dir + '/' + filename1
    path2 = temp_image_input_dir + '/' + filename2
    basename = get_file_basename(path1) + ' $ ' + get_file_basename(path2)
    temp_image1 = cv2.imread(path1)
    temp_image2 = cv2.imread(path2)
    joint_way, length = Judge(temp_image1, temp_image2)
    JointAndSaveRes(temp_image1, temp_image2, joint_way, black_bar, length, basename)


if __name__ == '__main__':
    mode = 'Joint'  # Cut_Batch、Cut_Single、Joint
    image_input_dir = 'input'
    temp_image_input_dir = 'temp'
    cut_single_filename = '017.jpg'
    temp_filename_1 = '008_t2.jpg'
    temp_filename_2 = '015_t2.jpg'
    '''
    tag_1   # cut_rejoint
    tag_2   # black_bar
    (cut_rejoint,black_bar)
    '''
    state_1 = (True, True)  # 截去渐变黑边，添加黑边拼图，存result
    state_2 = (True, False)  # 截去渐变黑边，不添加黑边拼图，存result
    state_3 = (False, True)  # 截去渐变黑边，存temp
    state_4 = (False, False)  # 保留渐变黑边，存temp

    tag_1, tag_2 = state_3

    if mode == 'Cut_Batch':
        Cut_Process_batch(image_input_dir, cut_rejoint=tag_1, black_bar=tag_2)
    elif mode == 'Cut_Single':
        Cut_Process_single(image_input_dir, cut_single_filename, cut_rejoint=tag_1, black_bar=tag_2)
    elif mode == 'Joint':
        Joint_Process(temp_image_input_dir, temp_filename_1, temp_filename_2, black_bar=tag_2)
    else:
        pass
