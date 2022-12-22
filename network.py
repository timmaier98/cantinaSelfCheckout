import keras.engine.functional
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
import os
import tensorflow as tf
import cv2


# class_names = ['Cola',
#  'Grohe',
#  'KitKat',
#  'Knoppers',
#  'Non',
#  'Skittles',
#  'Snickers',
#  'Spezi',
#  'Sprite',
#  'Studentenfutter']

class_names = ['Backfisch',
 'EintopfMWurst',
 'Kaiserschmarrn',
 'Kartoffelsalat',
 'Maultaschen',
 'Non',
 'NudelnBrokkoli',
 'NudelnTomate',
 'PizzaPesto',
 'PizzaVerdure',
 'ReisMitTomate',
 'Sauerkischpudding',
 'Schokopudding',
 'SoleroPudding',
 'Spinat']

model : keras.engine.functional.Functional = None

IMG_SIZE = (160, 160)


def initialize_model(path):
    global model, class_names
    model = tf.keras.models.load_model(path)
    return model


def get_pos_of_max_p(probabilities):
    probabilities = probabilities[0]
    if len(probabilities) == len(class_names):
        return class_names[np.argmax(probabilities)]
    else:
        return "Len of classnames doesn't match len of P"


def evaluate_image(img):
    if model is None:
        raise RuntimeError("Model not initialized")
    # check if image is not none and is a numpy array and has the correct shape
    if img is not None and isinstance(img, np.ndarray) and img.shape[0] >0 and img.shape[1] > 0:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, dsize=IMG_SIZE)
        img = np.expand_dims(img, axis=0)
        prediction = model.predict(img)
        out = get_pos_of_max_p(prediction)
        dictionary = dict(zip(class_names, prediction.flatten().tolist()))
        s = dict(sorted(dictionary.items(), key=lambda item: item[1], reverse=True))
        return out, s
    else:
        return "Error", None

if __name__ == '__main__':
    initialize_model('trained_models/model1_v2.h5')
    img = cv2.imread("C:\\Users\\larsg\\CantinaSelfCheckoutDataset\\val\\Cola\\IMG_0422.JPG")
    plt.imshow(img)
    plt.axis('off')
    predictions = evaluate_image(img)
    print(predictions)