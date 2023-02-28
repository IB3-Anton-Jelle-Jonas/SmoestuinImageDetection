import requests
from PIL import Image
import cv2

COLOR_DICT = {
    "chicken": (255, 0, 0),
    "egg": (0, 255, 0),
    "mouse": (255, 255, 255),
    "laptop": (0, 0 ,0),
    "chair": (0,0, 255),

}

capture = cv2.VideoCapture('http://10.129.48.15:8081/')

while(True):
    ret, frame = capture.read()
    cv2.imwrite("frame.jpg", frame)
    image_data = open("frame.jpg","rb").read()
    image = Image.open("frame.jpg").convert("RGB")
    #
    res = requests.post("http://10.108.80.214:80/v1/vision/custom/best", files={"image": image_data}).json()
    print(res)
    detect_dict = {}
    try:
        for object in res["predictions"]:

            label = object["label"]
            y_max = int(object["y_max"])
            y_min = int(object["y_min"])
            x_max = int(object["x_max"])
            x_min = int(object["x_min"])
            if not(detect_dict.get(label)):
                detect_dict[label] = 1
            else:
                detect_dict[label] += 1

            try:
                frame = cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), COLOR_DICT[label], 1)
            except:
                print(f"No color for: {label}")
    except:
        print("Nothing was found")
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    cv2.imshow("Smoestuin", frame)
    print(detect_dict)
    # try:
    #     requests.post("http://localhost:8080/objects/add", data=detect_dict)
    # except:
    #     print("failed to upload object count")

capture.release()
cv2.destroyAllWindows()

