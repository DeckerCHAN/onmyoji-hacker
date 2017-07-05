import cv2

from capture import Capture

if __name__ == "__main__":
    capture = Capture(100, 200, 400, 400)

    while True:
        cv2.imshow('frame', cv2.cvtColor(capture.np_image(), cv2.COLOR_BGR2RGB))

        out = cv2.waitKey(0)

        if out & 0xFF == ord('q'):
            break
        elif out & 0xFF == ord('s'):
            continue
