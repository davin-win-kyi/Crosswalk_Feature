'''''''''
Oveall system design:

- use Yolo / Minchu's model in order to detect objects 
- for each object we will get the average depth of the object 
    - this will allow us to know how close an object is 
- for each object that passes the threshold figure out which direction it is in 
- pass this information to the HoloLens to inform the user
'''

'''''''''
testing plan:
- get a few example images
- check to see if we are notified at the right time 
'''

from ultralytics import YOLO
from transformers import pipeline
from PIL import Image
import requests
import time

# we will be doing this to get the average
# value in the given image
import numpy as np

def run_yolo(model, pipe):
    img_path = 'C:\\Users\\davin\\PycharmProjects\\Depth_Testing\\crosswalk_testimage#1.jpg'
    image = Image.open(img_path)
    results = model(image)  # predict on an image
    # print("Results: ", results)
    depth = pipe(image)["depth"]
    depth.save("depth_image.jpg", "JPEG")
    # print("Depth: ", depth)

    boxes = results[0].boxes.xyxy.tolist()
    classes = results[0].boxes.cls.tolist()
    names = results[0].names

    # print("CLASSES: ", classes)
    # print("NAMES: ", names)

    np_image = np.array(depth)

    # now we can loop over each of the objects in the image and we can
    # check to see how close the objects are, we can set a threshold as
    # needed
    # Example parsing (details will depend on the actual output format of your model)
    for detection in range(len(boxes)):
        bbox = boxes[detection]

        object_name = names[classes[detection]]

        print("Class name: ", object_name)

        print("Bounding box: ", bbox)

        # here we can check over to see the average depth for the given
        # object in the image, and will add the object into a list which
        # we will check over

        # round the values by an int()
        x1 = int(bbox[0])
        y1 = int(bbox[1])
        x2 = int(bbox[2])
        y2 = int(bbox[3])

        depth_matrix = np_image[x1:x2, y1:y2]

        mean_val = np.mean(depth_matrix)

        print("MEAN DEPTH: ", mean_val)

        # let's determine the threshold first, then
        # we can discuss how to determine direction (will that also have a threshold?)
        # what are some edge cases to consider
        # etc. concerns



if __name__ == '__main__':
    model = YOLO("yolov8n.pt")
    pipe = pipeline(task="depth-estimation", model="LiheYoung/depth-anything-small-hf")
    run_yolo(model, pipe)