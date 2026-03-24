import cv2
import numpy as np

img = cv2.imread('dmg_background.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Threshold to find shapes (like white/transparent boxes or circles)
_, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)

# Find contours
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

centers = []
for cnt in contours:
    area = cv2.contourArea(cnt)
    if area > 1000: # large enough to be an icon placeholder
        x, y, w, h = cv2.boundingRect(cnt)
        cx = x + w//2
        cy = y + h//2
        centers.append((cx, cy, w, h))

centers.sort(key=lambda x: x[0])
print(f"Image Size: {img.shape[1]}x{img.shape[0]}")
print("Found potential icon placeholders at:")
for c in centers:
    print(c)
