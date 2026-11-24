import numpy as np
import cv2
import sys
from data_processing import PreprocessYOLO, PostprocessYOLO
from model_backend import CUDABackend, CoralBackend, USE_CUDA, USE_CORAL

np.set_printoptions(threshold=sys.maxsize)

CLASS_NAMES = {
    0: "RedYellowPin",
    1: "Cup",
    2: "BlueYellowPin",
    3: "YellowPin",
    4: "RedBluePin",
}

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
    def __init__(self, input_is_rgb=False):
        if USE_CUDA:
            self.backend = CUDABackend()
            print("Using CUDA for model inferencing")
        elif USE_CORAL:
            self.backend = CoralBackend()
            print("Using Coral Edge TPU for model inferencing")
        else:
            raise RuntimeError(
                "No inference backend found. Install CUDA/TensorRT for Jetson "
                "or connect a Coral Edge TPU."
            )

        self.input_resolution_yolov3_HW = (320, 320)
        self.input_is_rgb = input_is_rgb
        self.preprocessor = PreprocessYOLO(self.input_resolution_yolov3_HW)
        self.postprocessor = PostprocessYOLO()

    def inference(self, inputImage):
        image_raw, image_tensor, scale, pad_x, pad_y = self.preprocessor.process(
            inputImage, self.backend.dtype, input_is_rgb=self.input_is_rgb
        )
        shape_orig_WH = (image_raw.shape[1], image_raw.shape[0])

        outputs = self.backend.inference(image_tensor)
        Detections = []

        if not outputs:
            return inputImage, Detections

        boxes, classes, scores = self.postprocessor.process(
            outputs, shape_orig_WH, scale, pad_x, pad_y
        )

        if boxes.size == 0:
            return inputImage, Detections

        for box, score, category in zip(boxes, scores, classes):
            cat_id = int(category)
            if cat_id not in CLASS_NAMES:
                continue

            x_coord, y_coord, width, height = box
            orig_w, orig_h = shape_orig_WH

            left = max(0, min(orig_w - 2, int(np.floor(x_coord + 0.5))))
            top = max(0, min(orig_h - 2, int(np.floor(y_coord + 0.5))))
            right = max(left + 1, min(orig_w, int(np.floor(x_coord + width + 0.5))))
            bottom = max(top + 1, min(orig_h, int(np.floor(y_coord + height + 0.5))))

            width_px = right - left
            height_px = bottom - top
            cx = x_coord + (width / 2.0)
            cy = y_coord + (height / 2.0)
            class_name = CLASS_NAMES[cat_id]

            cv2.rectangle(inputImage, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(
                inputImage,
                f"{class_name} ({score:.2f})",
                (left, max(12, top - 5)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                2
            )

            raw_det = rawDetection(
                x=left,
                y=top,
                center=[float(cx), float(cy)],
                width=int(width_px),
                height=int(height_px),
                prob=float(score),
                classID=cat_id
            )
            Detections.append(raw_det)
            print(f"DETECTED: {class_name} | Conf: {score:.2f} | Box: [{left}, {top}, {width_px}, {height_px}]")

        return inputImage, Detections