

🎨 Air Doodle — A Computer Vision Project using OpenCV

Ever wanted to draw your imagination by just waving your finger in the air?
Air Doodle lets you do exactly that — a virtual drawing tool where you can draw anything in the air using just a colored marker detected by your webcam.

This project uses Computer Vision techniques in OpenCV, implemented in Python due to its simple syntax and powerful libraries. The same concept can also be extended to any language that supports OpenCV.


---

🧠 How it Works:

Color Detection & Tracking form the core of this project. A colored object (like a marker cap or finger tip with colored tape) is used to control the virtual pen.

We convert the video frame to HSV color space (better for detecting color) and generate a mask to isolate the marker. Using morphological operations like erosion (removing noise) and dilation (restoring the shape), we clean the mask for accurate detection.


---

⚙️ Algorithm Steps:

1. Capture video frames using webcam.


2. Convert each frame to HSV color space.


3. Set up a trackbar to help detect the desired marker color.


4. Generate a binary mask for the color using HSV thresholds.


5. Apply Erosion and Dilation to refine the mask.


6. Detect contours and find the largest one.


7. Track its center and store coordinates frame-by-frame.


8. Use the stored coordinates to draw lines on a canvas.


9. The result: a live virtual drawing that follows your marker in air!

