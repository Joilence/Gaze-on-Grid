import pandas as pd
import os
from PIL import Image, ImageOps
import os
import random

def get_grid_image_order(data_path, file_name):
    """
    # Data Example
    # "1" & "2": click ranking result
    # "pos": from left to right, top to left, the indexs of the block are 1,2,3,4,5,6
    # "1_order" & "2_order" : image in block 1~6
    # "cali": calibration verification result, block 1~6, "1" -> passed, "0": failed

    {'1': ['./images/grid_1/1_4.jpg'
        , './images/grid_1/1_5.jpg'
        , './images/grid_1/1_1.jpg'
        , './images/grid_1/1_3.jpg'
        , './images/grid_1/1_6.jpg'
        , './images/grid_1/1_2.jpg']
    , '2': ['./images/grid_2/2_4.jpg'
        , './images/grid_2/2_6.jpg'
        , './images/grid_2/2_5.jpg'
        , './images/grid_2/2_2.jpg'
        , './images/grid_2/2_1.jpg'
        , './images/grid_2/2_3.jpg']
    , 'pos': [
                {'order': '5', 'img_left_top': {'top': 653.59375, 'left': 849.859375}, 'img_size': [200, 290], 'img_aoi': [714.859375, 1184.859375, 553.59375, 1043.59375]}
                , {'order': '2', 'img_left_top': {'top': 119, 'left': 849.859375}, 'img_size': [200, 290], 'img_aoi': [714.859375, 1184.859375, 19, 509]}
                , {'order': '4', 'img_left_top': {'top': 653.59375, 'left': 184.59375}, 'img_size': [200, 290], 'img_aoi': [49.59375, 519.59375, 553.59375, 1043.59375]}
                , {'order': '1', 'img_left_top': {'top': 119, 'left': 184.59375}, 'img_size': [200, 290], 'img_aoi': [49.59375, 519.59375, 19, 509]}
                , {'order': '3', 'img_left_top': {'top': 119, 'left': 1515.125}, 'img_size': [200, 290], 'img_aoi': [1380.125, 1850.125, 19, 509]}
                , {'order': '6', 'img_left_top': {'top': 653.59375, 'left': 1515.125}, 'img_size': [200, 290], 'img_aoi': [1380.125, 1850.125, 553.59375, 1043.59375]}]
    , '1_order': ['./images/grid_1/1_6.jpg', './images/grid_1/1_5.jpg', './images/grid_1/1_1.jpg', './images/grid_1/1_2.jpg', './images/grid_1/1_4.jpg', './images/grid_1/1_3.jpg']
    , '2_order': ['./images/grid_2/2_6.jpg', './images/grid_2/2_4.jpg', './images/grid_2/2_5.jpg', './images/grid_2/2_1.jpg', './images/grid_2/2_2.jpg', './images/grid_2/2_3.jpg']
    , 'cali': [1, 1, 1, 0, 1, 1]}
    """

    
    tester = file_name.split("_")[0]
    with open(data_path + "/" + file_name) as fi:
        data = eval(fi.readlines()[1])
        g1_img_order = data["1_order"]
        g2_img_order = data["2_order"]
    
    return (tester, g1_img_order, g2_img_order)

    
def generate_grid_iamge(tester_and_orders):
    """
    # grid 3*2
    # image size = (200, 290)
    # for each block, (1902/3, 1080/2) = (640, 540)
    # for each image, padding, left and right, (640-200)/2 = 220, top+bottom = 540-290=250
         for top, and bottom: row 1: top=100, bottom=150, row 2: top=150, bottom=50
    """

    def combineImages(grid_size, image_size, image_list, grid_idx, block_size
                    , padding_h_l_r, padding_v_to_middle, padding_v_to_edge):
        grid_image = Image.new('RGB',grid_size)
        padding = {0: (padding_h_l_r, padding_v_to_edge, padding_h_l_r, padding_v_to_middle) # row 1
                , 1: (padding_h_l_r, padding_v_to_middle, padding_h_l_r, padding_v_to_edge)} # row 2

        for pos_order, image in enumerate(image_list):
            fromImge = Image.open(image)
            fromImge = fromImge.resize(image_size)
            fromImge = ImageOps.expand(fromImge, padding[int(pos_order / 3)], fill="white")
            loc = (((pos_order % 3) * block_size[0], int(pos_order / 3) * block_size[1]))
            grid_image.paste(fromImge, loc)

        grid_image.save("./exp-img/" + tester + "_grid_" + str(grid_idx+1) +".jpg")


    tester, g1_img_order, g2_img_order = tester_and_orders
    grid_size = (1920, 1080)
    block_size = (640, 540)
    image_size = (200, 290)

    padding_h_l_r = 220
    padding_v_to_middle = 150
    padding_v_to_edge = 100

    for grid_idx, image_list in enumerate([g1_img_order, g2_img_order]):
        combineImages(grid_size, image_size, image_list, grid_idx, block_size
                    , padding_h_l_r, padding_v_to_middle, padding_v_to_edge)


if __name__ == "__main__":
    data_path = "./data"
    # find click_rank.csv
    click_rank_files = [f for f in os.listdir(data_path) if "click_rank" in f]

    for file_name in click_rank_files:
        generate_grid_iamge(get_grid_image_order(data_path, file_name))