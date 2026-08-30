import numpy as np
import cv2
import sys
from model_backend import CUDABackend, CoralBackend, USE_CUDA, USE_CORAL

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
            print("No backend found!")

    def inference(self, inputImage):
        orig_h, orig_w = inputImage.shape[:2]

        img = cv2.cvtColor(inputImage, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (320, 320))
        img = img.astype(np.float32) / 255.0

        outputs = self.backend.inference(img)
        
        # CRITICAL FIX: Reshape to (6 channels, 500 detections) then transpose to (500, 6)
        raw_output = outputs[0].reshape(6, -1).transpose()
        
        Detections = []
        conf_threshold = 0.45

        for det in raw_output:
            conf = float(det[4])
            
            if np.isnan(conf) or conf < conf_threshold:
                continue
                
            cx, cy, w, h = det[0:4]
            class_id = int(det[5])

            if cx <= 1.0 and cy <= 1.0 and w <= 1.0 and h <= 1.0:
                cx *= orig_w
                cy *= orig_h
                w *= orig_w
                h *= orig_h
            else:
                cx *= (orig_w / 320.0)
                cy *= (orig_h / 320.0)
                w *= (orig_w / 320.0)
                h *= (orig_h / 320.0)

            # Clamp coordinates to ensure valid, non-zero area bounding boxes
            left = max(0, min(orig_w - 2, int(cx - (w / 2))))
            top = max(0, min(orig_h - 2, int(cy - (h / 2))))
            right = max(left + 1, min(orig_w, int(cx + (w / 2))))
            bottom = max(top + 1, min(orig_h, int(cy + (h / 2))))

            width_px = right - left
            height_px = bottom - top

            cv2.rectangle(inputImage, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(inputImage, f"ID:{class_id} ({conf:.2f})", (left, max(12, top - 5)), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)

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