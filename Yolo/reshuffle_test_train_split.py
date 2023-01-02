import os
import random
import shutil

JPG = ".jpg"

dir = "C:\\Users\\Lars\\Downloads\\ds2.v18i.yolov5pytorch\\train"

new_dir = "C:\\Users\\Lars\\Reshuffled"

if not os.path.exists(new_dir):
    os.makedirs(new_dir)


# Download the dataset with 100% train from roboflow
# run this script and copy the data.yaml file to the new folder
# upload resampled again to roboflow (drag and drop final folder, no need to zip)

valid_percentage = 0.2
test_percentage = 0.1
train_percentage = 1 - valid_percentage - test_percentage

def resample_yolo(dir, new_dir):
    # copy data.yaml
    # shutil.copy(os.path.join(dir, "data.yaml"), os.path.join(new_dir, "data.yaml"))
    # crate train and valid folder
    train_dir = os.path.join(new_dir, "train")
    valid_dir = os.path.join(new_dir, "valid")
    test_dir = os.path.join(new_dir, "test")
    if not os.path.exists(train_dir):
        os.makedirs(train_dir)
    if not os.path.exists(valid_dir):
        os.makedirs(valid_dir)
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)
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
    test_dir = os.path.join(new_dir, "test")
    train_images_dir = os.path.join(train_dir, "images")
    valid_images_dir = os.path.join(valid_dir, "images")
    train_labels_dir = os.path.join(train_dir, "labels")
    valid_labels_dir = os.path.join(valid_dir, "labels")
    test_images_dir = os.path.join(test_dir, "images")
    test_labels_dir = os.path.join(test_dir, "labels")
    print(train_images_dir)
    print(valid_images_dir)
    print(train_labels_dir)
    print(valid_labels_dir)

    old_dir_images = os.path.join(dir, "images")
    old_dir_labels = os.path.join(dir, "labels")
    print(old_dir_images)
    for file in os.listdir(old_dir_images):
        if file.endswith(JPG):
            random_number = random.random()
            if random_number < test_percentage:
                shutil.copy(os.path.join(old_dir_images, file), os.path.join(test_images_dir, file))
                # print("Would now copy " + file + " to " + test_images_dir)
                shutil.copy(os.path.join(old_dir_labels, file.replace(JPG, ".txt")), os.path.join(test_labels_dir, file.replace(JPG, ".txt")))
                # print("Would now copy " + file.replace(JPG, ".txt") + " to " + test_labels_dir)
            elif random_number < test_percentage + valid_percentage:
                shutil.copy(os.path.join(old_dir_images, file), os.path.join(valid_images_dir, file))
                # print("Would now copy " + file + " to " + valid_images_dir)
                shutil.copy(os.path.join(old_dir_labels, file.replace(JPG, ".txt")), os.path.join(valid_labels_dir, file.replace(JPG, ".txt")))
                # print("Would now copy " + file.replace(JPG, ".txt") + " to " + valid_labels_dir)
            else:
                shutil.copy(os.path.join(old_dir_images, file), os.path.join(train_images_dir, file))
                # print("Would now copy " + file + " to " + train_images_dir)
                shutil.copy(os.path.join(old_dir_labels, file.replace(JPG, ".txt")), os.path.join(train_labels_dir, file.replace(JPG, ".txt")))
                # print("Would now copy " + file.replace(JPG, ".txt") + " to " + train_labels_dir)



if __name__ == "__main__":
    resample_yolo(dir, new_dir)