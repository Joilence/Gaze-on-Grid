import os
import pandas as pd

def generate_pairwise_rank(pairwise_rank_files):
    """
    Generate pairwise rank based on preference and decision time
    """

    def one_rank_result(file_path, file_name):
        tester = file_name.split("_")[0]
        image_num_per_grid = 6
        preference = []
        df = pd.read_csv(file_path)
        df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '')
        
        # get the prefere image and its decision duration
        for row in df.itertuples():
            if getattr(row, "result") == "left":
                prefer_image = getattr(row, "left_image").split("/")[-1]
            elif getattr(row, "result") == "right":
                prefer_image = getattr(row, "right_image").split("/")[-1]
            elif getattr(row, "result") == "not sure":
                prefer_image = str(getattr(row, "grid")) + "_NS.jpg"
            elif getattr(row, "result") == "no decision":
                prefer_image = str(getattr(row, "grid")) + "_ND.jpg"

            duration = getattr(row, "end_timestamp") - getattr(row, "start_timestamp") - 3 # compensation


            weight = ((8000-duration)/8000) # asign weight to each prefer image
            preference.append((getattr(row, "grid"), prefer_image, weight))
        
        # one image may have different decsion duration, combine all the decision duration for each image
        # NS and ND just names, do not have such two images
        g1_image_name_list = ["1_"+ str(i+1) +".jpg" for i in range(image_num_per_grid)] + ["1_NS.jpg", "1_ND.jpg"] 
        g2_image_name_list = ["2_"+ str(i+1) +".jpg" for i in range(image_num_per_grid)] + ["2_NS.jpg", "2_ND.jpg"]
        image_name_list = g1_image_name_list + g2_image_name_list

        preference_pd = pd.DataFrame(preference)
        preference = []
        unique_list = preference_pd[1].unique() # prefer image, remove duplicates
        

        for img in unique_list:
            img_df = preference_pd[preference_pd[1]== img]
            preference.append((img_df.iloc[0][0], img, img_df[2].sum())) # (prefer_image, sum_of_weight)
            if img in image_name_list:
                image_name_list.remove(img)

        for i in image_name_list:
            preference.append((int(i.split("_")[0]), i, 0.0)) # images don't belong to prefer image,
                                                                #(grid, image_name, weight)
        preference_pd = pd.DataFrame(preference)

        preference = []
        preference.append(tester)
        # rank the image according to the weight
        for g in [1,2]:
            df_grid = preference_pd[preference_pd[0]== g] # select grid = g
            df_grid[2] = (df_grid[2]-df_grid[2].min())/(df_grid[2].max()-df_grid[2].min()) # normalization
            df_grid = df_grid.sort_values(by=2 , ascending=False)
            preference.append(df_grid.iloc[:, 1].tolist())
            preference.append(df_grid.iloc[:, 2].tolist())
        
        return tuple(preference)

    # -----------------------------
    pairwise_rank_result = []

    for file_name in pairwise_rank_files:
        file_path = data_path + "/" + file_name
        pairwise_rank_result.append(one_rank_result(file_path, file_name))

    df = pd.DataFrame(pairwise_rank_result, columns=["tester", "pwc_grid_1_rank", "pwc_grid_1_2"
                                                    , "pwc_grid_2_rank", "pwc_grid_1_w"])
    df.to_csv ("./rank_result/pairwise_rank_result.csv", index = False, header=True)



def generate_click_rank(click_rank_files):
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

    click_rank_result = []
    for file_name in click_rank_files:
        tester = file_name.split("_")[0]
        with open(data_path + "/" + file_name) as fi:
            data = eval(fi.readlines()[1])
            g1_img_rank = [i.split("/")[-1] for i in data["1"]]
            g2_img_rank = [i.split("/")[-1] for i in data["2"]]
            click_rank_result.append(tuple([tester, g1_img_rank, g2_img_rank]))
    
    df = pd.DataFrame(click_rank_result, columns=["tester", "click_grid_1_rank", "click_grid_2_rank"])
    df.to_csv ("./rank_result/click_rank_result.csv", index = False, header=True)


if __name__ == "__main__":
    data_path = "./data"

    # click rank
    click_rank_files = [f for f in os.listdir(data_path) if "click_rank" in f]
    generate_click_rank(click_rank_files)

    # general rank
    pairwise_rank_files = [f for f in os.listdir(data_path) if "pairwise_rank" in f]
    generate_pairwise_rank(pairwise_rank_files)
        