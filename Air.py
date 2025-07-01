import numpy as np
import cv2
from collections import deque

# Points for each color
bpoints = [deque(maxlen=1024)]
gpoints = [deque(maxlen=1024)]
rpoints = [deque(maxlen=1024)]
ypoints = [deque(maxlen=1024)]

# Indexes for each color
blue_index = 0
green_index = 0
red_index = 0
yellow_index = 0

# Kernel for morphology
kernel = np.ones((5, 5), np.uint8)

# Drawing colors (BGR)
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)]
colorIndex = 1  # Default to GREEN

# Canvas
paintWindow = np.ones((471, 636, 3), dtype=np.uint8) * 255
cv2.namedWindow('Paint', cv2.WINDOW_AUTOSIZE)

# Webcam
cap = cv2.VideoCapture(0)

# HSV range for orange detection
lower_orange = np.array([10, 100, 100])
upper_orange = np.array([25, 255, 255])

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Draw UI buttons
    frame = cv2.rectangle(frame, (40, 1), (140, 65), (122, 122, 122), -1)  # CLEAR ALL
    frame = cv2.rectangle(frame, (160, 1), (255, 65), colors[0], -1)  # BLUE
    frame = cv2.rectangle(frame, (275, 1), (370, 65), colors[1], -1)  # GREEN
    frame = cv2.rectangle(frame, (390, 1), (485, 65), colors[2], -1)  # RED
    frame = cv2.rectangle(frame, (505, 1), (600, 65), colors[3], -1)  # YELLOW

    cv2.putText(frame, "CLEAR ALL", (49, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "BLUE", (185, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "GREEN", (298, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "RED", (420, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "YELLOW", (520, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                (150, 150, 150), 2, cv2.LINE_AA)

    # Create mask for orange
    Mask = cv2.inRange(hsv, lower_orange, upper_orange)

    # Morphology to clean mask
    Mask = cv2.erode(Mask, kernel, iterations=1)
    Mask = cv2.morphologyEx(Mask, cv2.MORPH_OPEN, kernel)
    Mask = cv2.dilate(Mask, kernel, iterations=1)

    cnts, _ = cv2.findContours(Mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    center = None

    if len(cnts) > 0:
        cnt = sorted(cnts, key=cv2.contourArea, reverse=True)[0]
        ((x, y), radius) = cv2.minEnclosingCircle(cnt)

        if radius > 5:  # Filter small noise
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            M = cv2.moments(cnt)
            if M['m00'] != 0:
                center = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))

            if center and center[1] <= 65:
                # Check if clicking buttons
                if 40 <= center[0] <= 140:
                    # CLEAR ALL
                    bpoints = [deque(maxlen=512)]
                    gpoints = [deque(maxlen=512)]
                    rpoints = [deque(maxlen=512)]
                    ypoints = [deque(maxlen=512)]
                    blue_index = green_index = red_index = yellow_index = 0
                    paintWindow[67:, :, :] = 255
                elif 160 <= center[0] <= 255:
                    colorIndex = 0  # BLUE
                elif 275 <= center[0] <= 370:
                    colorIndex = 1  # GREEN
                elif 390 <= center[0] <= 485:
                    colorIndex = 2  # RED
                elif 505 <= center[0] <= 600:
                    colorIndex = 3  # YELLOW
            else:
                # Append point to selected color deque
                if colorIndex == 0:
                    bpoints[blue_index].appendleft(center)
                elif colorIndex == 1:
                    gpoints[green_index].appendleft(center)
                elif colorIndex == 2:
                    rpoints[red_index].appendleft(center)
                elif colorIndex == 3:
                    ypoints[yellow_index].appendleft(center)
    else:
        # If no contours found, create new deque for each color to separate strokes
        bpoints.append(deque(maxlen=1024))
        blue_index += 1
        gpoints.append(deque(maxlen=1024))
        green_index += 1
        rpoints.append(deque(maxlen=1024))
        red_index += 1
        ypoints.append(deque(maxlen=1024))
        yellow_index += 1

    points = [bpoints, gpoints, rpoints, ypoints]

    # Draw all points for all colors on frame and paintWindow
    for i in range(len(points)):
        for j in range(len(points[i])):
            for k in range(1, len(points[i][j])):
                if points[i][j][k - 1] is None or points[i][j][k] is None:
                    continue
                cv2.line(frame, points[i][j][k - 1], points[i][j][k], colors[i], 2)
                cv2.line(paintWindow, points[i][j][k - 1], points[i][j][k], colors[i], 2)

    cv2.imshow("Tracking", frame)
    cv2.imshow("Paint", paintWindow)
    cv2.imshow("Mask", Mask)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
