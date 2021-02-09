from imageai.Detection.Custom import CustomObjectDetection
import os
class FindShips():
    PNG_PATH = "data/images_png/"
    TXT_PATH = "data/info_txt/"
    LEARN_PATH = "data/learn/"
    OUT_PATH = "data/out_processed_file/"

    def __init__(self):
        execution_path = os.getcwd()
        self.detector = CustomObjectDetection()
        self.detector.setModelTypeAsYOLOv3()
        self.detector.setModelPath("detection_model-ex-044--loss-0022.165.h5")
        self.detector.setJsonPath("detection_config.json")
        self.detector.loadModel()


    def searchImages(self,nameFile):
        ships = []
        outfile = nameFile.split('.')[0] + 'processed.png'
        detections = self.detector.detectObjectsFromImage(input_image=self.LEARN_PATH+nameFile, output_image_path=self.OUT_PATH +outfile, minimum_percentage_probability=50)
        print("save: " +outfile)
        outfileTxt = nameFile.split('.')[0] + 'corners.txt'
        f = open(self.TXT_PATH + outfileTxt, "r")
        moveX = float(f.readline())
        moveY = float(f.readline())
        f.close()

        counter = 0
        for detection in detections:
            x1, y1, x2, y2 = detection["box_points"]
            x = (x2+x1)/2
            y = (y2+y1)/2
            x += moveX
            y += moveY
            ships.append((x, y))
            counter += 1
        return ships
