import numpy as np
import cv2


def preprocess(img_location, side):
    # probably put this to something more permanent
    img = cv2.imread(img_location)
    img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)

    size_x, size_y, _ = img.shape
    # crop - needs work
    img_crop_size = (480, 480)
    min_resize = max(img_crop_size[0] / size_x, img_crop_size[1] / size_y)
    img = cv2.resize(img, (int(size_x * min_resize), int(size_y * min_resize)))  # keeps the same aspect ratio
    size_x, size_y = (int(size_x * min_resize), int(size_y * min_resize))
    if side == 1:
        img = img[0:img_crop_size[0], (size_y - img_crop_size[1]):size_y]
    elif side == -1:
        img = img
    else:
        img = img

    img = cv2.transpose(img)
    img2 = img

    edges = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(edges, 200, 300)
    # edges = cv2.GaussianBlur(edges, (3, 3), 0)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 270, 150, minLineLength=20, maxLineGap=30)

    img = cv2.medianBlur(img, 5)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    edges = cv2.dilate(edges, kernel)

    # remove the blue red layer for smaller image size
    b, g, r = cv2.split(img)
    img = cv2.merge((b, g, edges))

    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            if not -0.3 < (y1 - y2) / (x1 - x2) < 0.3:
                cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 3)

    print(img.shape)
    cv2.imshow('test1', img2)
    cv2.imshow('test2', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


preprocess('test2.JPG', 1)
