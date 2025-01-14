import cv2
import numpy as np
from utils import draw_contours


class generateCoordinates:

    def __init__(self, image, output):
        self.output = output

        self.image = cv2.imread(image).copy()
        self.click_count = 0
        self.ids = 0
        self.coordinates = []
        cv2.namedWindow("Preprocess", cv2.WINDOW_GUI_EXPANDED)
        cv2.resizeWindow("Preprocess", 800, 600)
        cv2.setMouseCallback("Preprocess", self.mouse_callback)

    def generate(self):
        while True:
            cv2.imshow("Preprocess", self.image)
            key = cv2.waitKey(0)

            if key == 114:
                self.image = self.image.copy()
            elif key == 113:
                break
        cv2.destroyWindow("Preprocess")

    def mouse_callback(self, event, x, y, flags, params):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.coordinates.append((x, y))
            self.click_count += 1

            if self.click_count >= 4:
                self.draw_quadrilateral()

            elif self.click_count > 1:
                cv2.line(self.image, self.coordinates[-2], self.coordinates[-1], (255, 0, 0), 1)

        cv2.imshow("Preprocess", self.image)        

    def draw_quadrilateral(self):
        cv2.line(self.image, self.coordinates[2], self.coordinates[3], (255,255,255), 1)
        cv2.line(self.image, self.coordinates[3], self.coordinates[0], (255,255,255), 1)

        self.click_count = 0

        coordinates = np.array(self.coordinates)

        self.output.write("-\n          id: " + str(self.ids) + "\n          coordinates: [" +
                          "[" + str(self.coordinates[0][0]) + "," + str(self.coordinates[0][1]) + "]," +
                          "[" + str(self.coordinates[1][0]) + "," + str(self.coordinates[1][1]) + "]," +
                          "[" + str(self.coordinates[2][0]) + "," + str(self.coordinates[2][1]) + "]," +
                          "[" + str(self.coordinates[3][0]) + "," + str(self.coordinates[3][1]) + "]]\n")

        draw_contours(self.image, coordinates, str(self.ids + 1), (255,255,255))

        for i in range(0, 4):
            self.coordinates.pop()

        self.ids += 1
