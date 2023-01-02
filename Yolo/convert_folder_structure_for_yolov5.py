import os
import random
import shutil

dir = "C:\\Users\\larsg\\CantinaSelfCheckoutDatasetMensa\\train"

new_dir = "C:\\Users\\larsg\\CantinaSelfCheckoutDatasetMensaYolo2"

if not os.path.exists(new_dir):
    os.makedirs(new_dir)


# First run segmentation.py to get the images and the labels.txt
# Then run this script to get the folder structure for YoloV5
# When zipping the folder structure for YoloV5, make sure to have en folder in a folder

valid_percentage = 0.2
test_percentage = 0.1
train_percentage = 1 - valid_percentage - test_percentage

def crate_yolo_folder_structure(dir, new_dir):
    # copy data.yaml
    shutil.copy(os.path.join(dir, "data.yaml"), os.path.join(new_dir, "data.yaml"))
    # crate train and valid folder
    train_dir = os.path.join(new_dir, "train")
    valid_dir = os.path.join(new_dir, "valid")
    if not os.path.exists(train_dir):
        os.makedirs(train_dir)
    if not os.path.exists(valid_dir):
        os.makedirs(valid_dir)
    for folder in os.listdir(new_dir):
        # create a folder images and labels
        if folder.endswith(".txt") or folder.endswith(".yaml"):
            continue
        images_dir = os.path.join(new_dir, folder, "images")
        labels_dir = os.path.join(new_dir, folder, "labels")
        if not os.path.exists(images_dir):
            os.makedirs(images_dir)
        if not os.path.exists(labels_dir):
            os.makedirs(labels_dir)
        # copy images and labels to the new folder structure 20% to valid folder

    # print all folders in new_dir
    train_images_dir = ""
    valid_images_dir = ""
    train_labels_dir = ""
    valid_labels_dir = ""
    train_dir = os.path.join(new_dir, "train")
    valid_dir = os.path.join(new_dir, "valid")
    train_images_dir = os.path.join(train_dir, "images")
    valid_images_dir = os.path.join(valid_dir, "images")
    train_labels_dir = os.path.join(train_dir, "labels")
    valid_labels_dir = os.path.join(valid_dir, "labels")
    print(train_images_dir)
    print(valid_images_dir)
    print(train_labels_dir)
    print(valid_labels_dir)

    for folder in os.listdir(dir):
        # exclude .txt files
        if folder.endswith(".txt") or folder.endswith(".yaml"):
            continue
        train_folder = os.path.join(dir, folder)
        for file in os.listdir(train_folder):
            label_file = file.replace(".png", ".txt")
            if not os.path.exists(os.path.join(dir, label_file)):   # check if label file exists
                continue
            random_split = random.random()
            if random.random() < 0.2:
                # print("Would move file: " + os.path.join(train_folder, file) + " to " + os.path.join(valid_images_dir, file))
                shutil.copy(os.path.join(train_folder, file), valid_images_dir)
                # copy labels
                # take name of file and replace .png with .txt
                # print("Would move file: " + os.path.join(dir, label_file) + " to " + os.path.join(valid_labels_dir, label_file))
                shutil.copy(os.path.join(dir, label_file), valid_labels_dir)
            else:
                # print("Would move file: " + os.path.join(train_folder, file) + " to " + os.path.join(train_images_dir, file))
                shutil.copy(os.path.join(train_folder, file), train_images_dir)
                # copy labels
                # take name of file and replace .png with .txt
                # print("Would move file: " + os.path.join(dir, label_file) + " to " + os.path.join(train_labels_dir,
                #                                                                                   label_file))
                shutil.copy(os.path.join(dir, label_file), train_labels_dir)






if __name__ == '__main__':
    crate_yolo_folder_structure(dir, new_dir)