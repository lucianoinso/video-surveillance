import cv2
import numpy as np
from tensorflow.keras.applications.mobilenet import (
                                                preprocess_input,
                                                decode_predictions)
from tensorflow.keras.preprocessing import image

def classify(model, img):
    # Model input size for MobileNet, VGG16 and ResNet50

    size = (224, 224)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    height, width, channels = img.shape

    scale_value = width / height

    img_resized = cv2.resize(imgRGB, size, fx=scale_value, fy=1,
                                interpolation=cv2.INTER_NEAREST)

    x = image.img_to_array(img_resized)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)

    preds = model.predict(x)

    top_prediction = decode_predictions(preds, top=1)[0][0]

    class_name = top_prediction[1]
    confidence_score = top_prediction[2]
    confidence_level = confidence_score * 100


    return (class_name, confidence_level)
