import os
import random
import shutil

dir = "C:\\Users\\larsg\\CantinaSelfCheckoutDatasetMensa"
# train_dir = ("C:\\Users\\timen\\Documents\\Uni\\4. Mastersemester\\Data Science II\\cantinaSelfCheckout\\Trainingsbilder\\train")
# validation_dir = ("C:\\Users\\timen\\Documents\\Uni\\4. Mastersemester\\Data Science II\\cantinaSelfCheckout\\Trainingsbilder\\val")

# for every folder in train dir take 20% of the images and move them to the test dir
def split_train_test(dir):
    train_dir = os.path.join(dir, "train")
    validation_dir = os.path.join(dir, "val")
    for folder in os.listdir(train_dir):
        # exclude .txt files
        if folder.endswith(".txt") or folder.endswith(".yaml"):
            continue
        train_folder = os.path.join(train_dir, folder)
        validation_folder = os.path.join(validation_dir, folder)
        if not os.path.exists(validation_folder):
            os.makedirs(validation_folder)
        for file in os.listdir(train_folder):
            if random.random() < 0.2:
                shutil.move(os.path.join(train_folder, file), validation_folder)

def reverse_test_train(dir):
    train_dir = os.path.join(dir, "train")
    validation_dir = os.path.join(dir, "val")
    for folder in os.listdir(validation_dir):
        # exclude .txt files
        if folder.endswith(".txt") or folder.endswith(".yaml"):
            continue
        train_folder = os.path.join(train_dir, folder)
        validation_folder = os.path.join(validation_dir, folder)
        if not os.path.exists(train_folder):
            os.makedirs(train_folder)
        for file in os.listdir(validation_folder):
            shutil.move(os.path.join(validation_folder, file), train_folder)

if __name__ == '__main__':
    split_train_test(dir)
    # reverse_test_train(dir)