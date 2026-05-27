import cv2
import numpy as np


def order_points(points):
    points = points.reshape(4, 2).astype(np.float32)

    s = points.sum(axis=1)
    diff = np.diff(points, axis=1)

    left_up = points[np.argmin(s)]
    right_down = points[np.argmax(s)]
    right_up = points[np.argmin(diff)]
    left_down = points[np.argmax(diff)]

    return np.array([left_up, right_up, right_down, left_down], dtype=np.float32)


cap = cv2.VideoCapture("test3.mp4")

if not cap.isOpened():
    print("无法打开视频 test3.mp4")
    exit()

fps = cap.get(cv2.CAP_PROP_FPS)
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

fourcc = cv2.VideoWriter_fourcc(*"mp4v")
out = cv2.VideoWriter("test3_out.mp4", fourcc, fps, (frame_width, frame_height))

focal_length = max(frame_width, frame_height)

cameraMatrix = np.array([
    [focal_length, 0, frame_width / 2],
    [0, focal_length, frame_height / 2],
    [0, 0, 1]
], dtype=np.float32)

distCoeffs = np.zeros((5, 1), dtype=np.float32)

objectPoints = np.array([
    [-2.0, -1.5, 0.0],
    [2.0, -1.5, 0.0],
    [2.0, 1.5, 0.0],
    [-2.0, 1.5, 0.0]
], dtype=np.float32)

axis_points = np.array([
    [0.0, 0.0, 0.0],
    [2.0, 0.0, 0.0],
    [0.0, 2.0, 0.0],
    [0.0, 0.0, -2.0]
], dtype=np.float32)

while True:
    ret, frame = cap.read()

    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    binary = cv2.inRange(blur, 0, 100)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    binary2 = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel, iterations=2)

    contours, _ = cv2.findContours(binary2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    best_approx = None
    best_area = 0

    for contour in contours:
        area = cv2.contourArea(contour)

        if area < 3000:
            continue

        x, y, w, h = cv2.boundingRect(contour)

        if w < 80 or h < 80:
            continue

        ratio = w / h
        if ratio < 0.8 or ratio > 2.0:
            continue

        epsilon = 0.03 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)

        if len(approx) != 4:
            continue

        if area > best_area:
            best_area = area
            best_approx = approx

    if best_approx is not None:
        imagePoints = order_points(best_approx)

        success, rvec, tvec = cv2.solvePnP(
            objectPoints,
            imagePoints,
            cameraMatrix,
            distCoeffs
        )

        if success:
            points = imagePoints.astype(int)

            cv2.polylines(frame, [points], True, (0, 255, 0), 3)

            x, y, w, h = cv2.boundingRect(points)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

            projected_axis_points, _ = cv2.projectPoints(
                axis_points,
                rvec,
                tvec,
                cameraMatrix,
                distCoeffs
            )

            projected_axis_points = np.int32(projected_axis_points).reshape(-1, 2)

            origin = tuple(projected_axis_points[0])
            x_axis = tuple(projected_axis_points[1])
            y_axis = tuple(projected_axis_points[2])
            z_axis = tuple(projected_axis_points[3])

            cv2.line(frame, origin, x_axis, (0, 0, 255), 4)
            cv2.line(frame, origin, y_axis, (0, 255, 0), 4)
            cv2.line(frame, origin, z_axis, (255, 0, 0), 4)

            cv2.putText(frame, "X", x_axis, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.putText(frame, "Y", y_axis, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, "Z", z_axis, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

            text = "tvec: x={:.2f}, y={:.2f}, z={:.2f} cm".format(
                tvec[0][0],
                tvec[1][0],
                tvec[2][0]
            )
            cv2.putText(frame, text, (50, 80), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)

    out.write(frame)

    show_height = 960
    show_width = int(frame_width * show_height / frame_height)

    show_frame = cv2.resize(frame, (show_width, show_height))
    cv2.imshow("solvePnP result", show_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
out.release()
cv2.destroyAllWindows()