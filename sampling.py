import datetime
import os

import cv2

from capture import Capture

if __name__ == "__main__":

    refPt = []
    cropping = False
    chopped_area = None

    sample_folder = "data"


    def click_and_crop(event, x, y, flags, param):
        # grab references to the global variables
        global refPt, cropping

        # if the left mouse button was clicked, record the starting
        # (x, y) coordinates and indicate that cropping is being
        # performed
        if event == cv2.EVENT_LBUTTONDOWN:
            refPt = [(x, y)]
            cropping = True

        # check to see if the left mouse button was released
        elif event == cv2.EVENT_LBUTTONUP:
            # record the ending (x, y) coordinates and indicate that
            # the cropping operation is finished
            refPt.append((x, y))
            cropping = False

            # draw a rectangle around the region of interest
            cv2.rectangle(current_frame, refPt[0], refPt[1], (0, 255, 0), 1)
            cv2.imshow("frame", current_frame)
            chopped_area.append((refPt[0], refPt[1]))
            print(str.format("Added new pair {0} to {1}", refPt[0], refPt[1]))


    current_frame = None

    cv2.namedWindow("frame")
    cv2.setMouseCallback("frame", click_and_crop)

    capture = Capture(200, 200, 710, 400)

    while True:
        frame = cv2.cvtColor(capture.np_image(), cv2.COLOR_BGR2RGB)

        current_frame = frame.copy()

        chopped_area = list()

        cv2.imshow('frame', current_frame)

        out = cv2.waitKey(0) & 0xFF

        if out == ord('q'):
            break
        elif out == ord('d'):
            for (pt1, pt2) in chopped_area:
                crop_pos = frame[min(pt1[1], pt2[1]): min(pt1[1], pt2[1]) + abs(pt1[1] - pt2[1]),
                           min(pt1[0], pt2[0]): min(pt1[0], pt2[0]) + abs(pt1[0] - pt2[0])]

                cv2.imwrite(
                    os.path.join(sample_folder, "crop-" + datetime.datetime.now().strftime('%Y%m%d-%H%M%S.%f') + ".jpg"),
                    crop_pos)
            continue
        elif out == ord('s'):
            continue
