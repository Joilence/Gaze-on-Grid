import os
import pandas as pd

def generate_pairwise_rank():
    """
    Generate pairwise rank based on preference and decision time
    """
    pass

def generate_general_rank(click_rank_files):
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

    general_rank_result = []
    for file_name in click_rank_files:
        tester = file_name.split("_")[0]
        with open(data_path + "/" + file_name) as fi:
            data = eval(fi.readlines()[1])
            g1_img_rank = [i.split("/")[-1] for i in data["1"]]
            g2_img_rank = [i.split("/")[-1] for i in data["2"]]
            general_rank_result.append(tuple([tester] + g1_img_rank + g2_img_rank))
    
    df = pd.DataFrame(general_rank_result, columns=["tester", "g_g1_1", "g_g1_2", "g_g1_3", "g_g1_4", "g_g1_5", "g_g1_6"
                                        , "g_g2_1", "g_g2_2", "g_g2_3", "g_g2_4", "g_g2_5", "g_g2_6"])
    df.to_csv ("./rank_result/general_rank_result.csv", index = False, header=True)


if __name__ == "__main__":
    data_path = "./data"
    # find click_rank.csv
    click_rank_files = [f for f in os.listdir(data_path) if "click_rank" in f]
    generate_general_rank(click_rank_files)
    
        