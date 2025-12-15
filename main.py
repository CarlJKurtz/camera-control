import os
# List all available camera devices using OpenCV
def list_available_cameras(max_index=10):
    print("[…] Scanning for available video devices...")
    available = []
    for index in range(max_index):
        cap = cv2.VideoCapture(index)
        if cap.read()[0]:
            print(f"[!] Camera found at index {index}")
            available.append(index)
        cap.release()
    if not available:
        print("[!] No cameras found.")
    return available

import cv2
import numpy as np
from PIL import Image

show_grayscale = False

crop_center_square = True

magnification_ppi = 4950

list_available_cameras()

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 3840)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 2160)

if not cap.isOpened():
    print("    Cannot open camera")
    exit()

print("[!] Found working camera at index 0")
print("    Press SPACE to take a photo. Press ESC to quit. Press G to toggle Grayscale mode.")


def switch_camera(index):
    global cap
    cap.release()
    cap = cv2.VideoCapture(index)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 3840)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 2160)
    print(f"🔁 Switched to camera index {index}")


while True:
    ret, frame = cap.read()
    if not ret or frame is None:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    frame = np.ascontiguousarray(frame)
    if crop_center_square:
        h, w = frame.shape[:2]
        min_dim = min(h, w)
        top = (h - min_dim) // 2
        left = (w - min_dim) // 2
        frame = frame[top:top+min_dim, left:left+min_dim]

    raw_frame = frame.copy()
    if show_grayscale:
        raw_frame = cv2.cvtColor(raw_frame, cv2.COLOR_BGR2GRAY)
        raw_frame = cv2.cvtColor(raw_frame, cv2.COLOR_GRAY2BGR)

    # Draw grid lines
    height, width = frame.shape[:2]
    grid_spacing = int(magnification_ppi / 25.4)
    for x in range(0, width, grid_spacing):
        cv2.line(frame, (x, 0), (x, height), (255, 255, 255), 1)
    y_count = 0
    for y in range(0, height, grid_spacing):
        y_count += 1
        if y_count == 8:
            cv2.line(frame, (0, y), (width, y), (0, 0, 255), 2)
        else:
            cv2.line(frame, (0, y), (width, y), (255, 255, 255), 1)
    display_frame = frame.copy()
    if show_grayscale:
        display_frame = cv2.cvtColor(display_frame, cv2.COLOR_BGR2GRAY)
        display_frame = cv2.cvtColor(display_frame, cv2.COLOR_GRAY2BGR)
    cv2.imshow('Camera', display_frame)
    key = cv2.waitKey(1)
    if key == 27:
        break
    elif key == 32:
        import datetime
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        output_dir = os.path.join("output", f"{today}")
        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename_raw = os.path.join(output_dir, f"photo_{timestamp}_raw.png")
        filename_grid = os.path.join(output_dir, f"photo_{timestamp}_grid.png")
        cv2.imwrite(filename_raw, raw_frame)
        img = Image.open(filename_raw)
        img.save(filename_raw, dpi=(9900, 9900))
        grid_frame = frame.copy()
        if show_grayscale:
            grid_frame = cv2.cvtColor(grid_frame, cv2.COLOR_BGR2GRAY)
            grid_frame = cv2.cvtColor(grid_frame, cv2.COLOR_GRAY2BGR)
        cv2.imwrite(filename_grid, grid_frame)
        img = Image.open(filename_grid)
        img.save(filename_grid, dpi=(9900, 9900))
        print(f"Photos saved as {filename_raw} and {filename_grid}")
    elif key == ord('g'):
        show_grayscale = not show_grayscale
        print("Grayscale mode:", "ON" if show_grayscale else "OFF")
    elif key == ord('s'):
        crop_center_square = not crop_center_square
        print("Center crop:", "ON" if crop_center_square else "OFF")


cap.release()
cv2.destroyAllWindows()
