import numpy as np
import sys
import cv2
from model_backend import CUDABackend, CoralBackend, USE_CUDA, USE_CORAL

# Set print options for NumPy
np.set_printoptions(threshold=sys.maxsize)


class rawDetection:
    def __init__(self, x: int, y: int, center: list, width: int, height: int, prob: float, classID: int):
        self.x = x
        self.y = y
        self.Center = center
        self.Width = width
        self.Height = height
        self.Prob = prob
        self.ClassID = classID


class Model:
    def __init__(self):
        if USE_CUDA:
            self.backend = CUDABackend()
            print("Using CUDA for model inferencing")
        elif USE_CORAL:
            self.backend = CoralBackend()
            print("Using Coral Edge TPU for model inferencing")
        else:
            print("No backend found! Make sure you have CUDA or Coral installed based on your device")

    def inference(self, inputImage):
        # 1. Preprocess Image (Convert BGR to RGB, resize to 320x320, normalize to 0.0 - 1.0)
        img = cv2.cvtColor(inputImage, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (320, 320))
        img = img.astype(np.float32) / 255.0
        
        # Convert HWC to CHW if backend expects channel-first format:
        # img = np.transpose(img, (2, 0, 1))

        # 2. Run raw TensorRT / CUDA inference
        outputs = self.backend.inference(img)
        
        # Reshape flat output tensor (size 3000 -> N x 6 elements)
        raw_output = outputs[0].reshape(-1, 6) 
        
        Detections = []
        conf_threshold = 0.25

        orig_h, orig_w = inputImage.shape[:2]

        for det in raw_output:
            conf = det[4]
            
            # Skip NaNs or uninitialized array values
            if np.isnan(conf):
                continue
                
            # Filter predictions below confidence threshold
            if conf >= conf_threshold:
                cx, cy, w, h = det[0:4]
                class_id = int(det[5])

                # Print raw bounding box details for debugging
                print(f"Detection found -> Class: {class_id}, Conf: {conf:.2f}, Raw Box: [{cx:.2f}, {cy:.2f}, {w:.2f}, {h:.2f}]")

                # Handle normalized vs absolute coordinates
                if cx <= 1.0 and cy <= 1.0 and w <= 1.0 and h <= 1.0:
                    cx *= orig_w
                    cy *= orig_h
                    w *= orig_w
                    h *= orig_h
                else:
                    # Scale 320x320 box back to original input image dimensions
                    cx = cx * (orig_w / 320.0)
                    cy = cy * (orig_h / 320.0)
                    w = w * (orig_w / 320.0)
                    h = h * (orig_h / 320.0)
                
                # Calculate top-left corner coordinates and clamp to image frame
                left = max(0, int(cx - (w / 2)))
                top = max(0, int(cy - (h / 2)))
                width_px = min(orig_w - left, int(w))
                height_px = min(orig_h - top, int(h))
                
                raw_det = rawDetection(
                    x=left, 
                    y=top, 
                    center=[float(cx), float(cy)], 
                    width=int(width_px), 
                    height=int(height_px), 
                    prob=float(conf), 
                    classID=class_id
                )
                Detections.append(raw_det)

        return inputImage, Detections
