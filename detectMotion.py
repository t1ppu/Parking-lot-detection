import cv2
import numpy as np
from utils import draw_contours

class detectMotion:
    def __init__(self, video, coordinates):
        self.video = video
        self.coordinates_data = coordinates
        self.contours = []
        self.bounds = []
        self.mask = []
        self.delay = 0.5
        self.lp = 1.4
        self.available = 0

    def detect(self):
        capture = cv2.VideoCapture(self.video)
        coordinates_data = self.coordinates_data

        for p in coordinates_data:
            coordinates = np.array(p["coordinates"])

            quad = cv2.boundingRect(coordinates)

            new_coordinates = coordinates.copy()
            new_coordinates[:, 0] = coordinates[:, 0] - quad[0]
            new_coordinates[:, 1] = coordinates[:, 1] - quad[1]

            self.contours.append(coordinates)
            self.bounds.append(quad)

            mask = cv2.drawContours(
                np.zeros((quad[3], quad[2]), dtype=np.uint8),
                [new_coordinates],
                contourIdx=-1,
                color=255,
                thickness=-1,
                lineType=cv2.LINE_8)

            mask = mask == 255
            self.mask.append(mask)

        statuses = [False] * len(coordinates_data)
        times = [None] * len(coordinates_data)

        while capture.isOpened():
            result, frame = capture.read()
            if frame is None:
                break

            if not result:
                print(f"Error: Could not read frame from {self.video}")
                break

            blurred = cv2.GaussianBlur(frame.copy(), (5, 5), 3)
            grayed = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
            new_frame = frame.copy()

            position_in_seconds = capture.get(cv2.CAP_PROP_POS_MSEC) / 1000.0

            for index, c in enumerate(coordinates_data):
                status = self.apply(grayed, index, c)

                if times[index] is not None and self.equalStatus(statuses, index, status):
                    times[index] = None
                    continue

                if times[index] is not None and self.toggleStatus(statuses, index, status):
                    if position_in_seconds - times[index] >= self.delay:
                        statuses[index] = status
                        times[index] = None
                        if status:
                            self.available += 1
                    continue

                if times[index] is None and self.toggleStatus(statuses, index, status):
                    times[index] = position_in_seconds
                    if not status:
                        self.available -= 1

            for index, p in enumerate(coordinates_data):
                coordinates = np.array(p["coordinates"])

                color = (0, 255, 0) if statuses[index] else (0, 0, 255)
                draw_contours(new_frame, coordinates, str(p["id"] + 1), (255, 255, 255), color)
            cv2.namedWindow(str(self.video), cv2.WINDOW_NORMAL)
            cv2.imshow(str(self.video), new_frame)
            k = cv2.waitKey(1)
            if k == ord("q"):
                break
        capture.release()
        cv2.destroyAllWindows()

    def apply(self, grayed, index, p):
        coordinates = np.array(p["coordinates"])
        rect = self.bounds[index]
        roi_gray = grayed[rect[1]:(rect[1] + rect[3]), rect[0]:(rect[0] + rect[2])]
        laplacian = cv2.Laplacian(roi_gray, cv2.CV_64F)

        coordinates[:, 0] = coordinates[:, 0] - rect[0]
        coordinates[:, 1] = coordinates[:, 1] - rect[1]

        status = np.mean(np.abs(laplacian * self.mask[index])) < self.lp
        return status

    def equalStatus(self, coordinates_status, index, status):
        return status == coordinates_status[index]

    def toggleStatus(self, coordinates_status, index, status):
        return status != coordinates_status[index]

