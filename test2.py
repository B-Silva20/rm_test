import cv2
import numpy as np

image = cv2.imread("test2.png")

img_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
img_h, img_s, img_v = cv2.split(img_hsv)

mask_h = cv2.inRange(img_h, 80, 110)
mask_s = cv2.inRange(img_s, 40, 255)
mask_v = cv2.inRange(img_v, 150, 255)

mask_h_and_s = cv2.bitwise_and(mask_h, mask_s)
binary = cv2.bitwise_and(mask_h_and_s, mask_v)

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
binary2 = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel, iterations=2)

contours, _ = cv2.findContours(binary2, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

boxes = []

for contour in contours:
    area = cv2.contourArea(contour)

    if area < 800 or area > 6000:
        continue

    x, y, w, h = cv2.boundingRect(contour)

    if w < 45 or h < 45:
        continue

    ratio = w / h
    if ratio < 0.5 or ratio > 2.0:
        continue

    epsilon = 0.03 * cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, epsilon, True)

    if len(approx) < 4 or len(approx) > 8:
        continue

    boxes.append((x, y, x + w, y + h))


merged_boxes = []

for box in boxes:
    x1, y1, x2, y2 = box
    merged = False

    for i in range(len(merged_boxes)):
        mx1, my1, mx2, my2 = merged_boxes[i]

        if not (x2 < mx1 or x1 > mx2 or y2 < my1 or y1 > my2):
            merged_boxes[i] = (
                min(x1, mx1),
                min(y1, my1),
                max(x2, mx2),
                max(y2, my2)
            )
            merged = True
            break

    if not merged:
        merged_boxes.append(box)


padding = 2

for x1, y1, x2, y2 in merged_boxes:
    roi = binary[y1:y2, x1:x2]

    tight_contours, _ = cv2.findContours(roi, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    if len(tight_contours) == 0:
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 255), 2)
        continue

    points = []

    for tight_contour in tight_contours:
        area = cv2.contourArea(tight_contour)
        if area < 50:
            continue
        points.append(tight_contour)

    if len(points) == 0:
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 255), 2)
        continue

    all_points = np.vstack(points)
    tx, ty, tw, th = cv2.boundingRect(all_points)

    nx1 = x1 + tx - padding
    ny1 = y1 + ty - padding
    nx2 = x1 + tx + tw + padding
    ny2 = y1 + ty + th + padding

    cv2.rectangle(image, (nx1, ny1), (nx2, ny2), (0, 0, 255), 2)

cv2.imshow("img", image)
cv2.imwrite("test2_out.png", image)
cv2.waitKey(0)
cv2.destroyAllWindows()