import cv2

cap = cv2.VideoCapture("additional_test.mp4")

frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

show_height = 960
show_width = int(frame_width * show_height / frame_height)

while True:
    ret, frame = cap.read()

    if not ret:
        break

    img_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    img_h, img_s, img_v = cv2.split(img_hsv)

    mask_h = cv2.inRange(img_h, 5, 25)
    mask_s = cv2.inRange(img_s, 80, 255)
    mask_v = cv2.inRange(img_v, 80, 255)

    mask_h_and_s = cv2.bitwise_and(mask_h, mask_s)
    binary = cv2.bitwise_and(mask_h_and_s, mask_v)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
    binary2 = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel, iterations=2)
    binary2 = cv2.morphologyEx(binary2, cv2.MORPH_OPEN, kernel, iterations=1)

    contours, _ = cv2.findContours(binary2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    if len(contours) > 0:
        max_contour = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(max_contour)

        if area > 1000:
            epsilon = 0.003 * cv2.arcLength(max_contour, True)
            approx = cv2.approxPolyDP(max_contour, epsilon, True)

            x, y, w, h = cv2.boundingRect(approx)

            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.drawContours(frame, [approx], -1, (0, 255, 0), 2)

    show_frame = cv2.resize(frame, (show_width, show_height))
    cv2.imshow("orange tracking", show_frame)

    if cv2.waitKey(30) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()