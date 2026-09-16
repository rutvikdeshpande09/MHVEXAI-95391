import numpy as np
import cv2

class PreprocessYOLO:
    def __init__(self, input_resolution):
        self.input_resolution = input_resolution

    def process(self, img, dtype, input_is_rgb=False):
        image_raw = img
        input_width, input_height = self.input_resolution
        image_height, image_width = image_raw.shape[:2]
        scale = min(input_width / image_width, input_height / image_height)
        resized_width = int(round(image_width * scale))
        resized_height = int(round(image_height * scale))
        image_resized = cv2.resize(
            image_raw, (resized_width, resized_height), interpolation=cv2.INTER_LINEAR
        )
        pad_width = input_width - resized_width
        pad_height = input_height - resized_height
        left = pad_width // 2
        top = pad_height // 2
        image_letterboxed = cv2.copyMakeBorder(
            image_resized,
            top,
            pad_height - top,
            left,
            pad_width - left,
            cv2.BORDER_CONSTANT,
            value=(114, 114, 114),
        )
        image_rgb = (
            image_letterboxed
            if input_is_rgb
            else cv2.cvtColor(image_letterboxed, cv2.COLOR_BGR2RGB)
        )
        image_normalized = image_rgb.astype(np.float32) / 255.0
        image_transposed = np.transpose(image_normalized, (2, 0, 1))
        image_expanded = np.expand_dims(image_transposed, axis=0)
        image_contiguous = np.ascontiguousarray(image_expanded, dtype=dtype)
        return image_raw, image_contiguous, scale, left, top

class PostprocessYOLO:
    def __init__(self, **kwargs):
        self.conf_threshold = 0.40
        self.nms_threshold = 0.45
        self.class_names = {
            0: "RedYellowPin",
            1: "Cup",
            2: "BlueYellowPin",
            3: "YellowPin",
            4: "RedBluePin",
        }
        self.input_resolution = (320, 320)

    def process(self, outputs, orig_shape, scale=1.0, pad_x=0, pad_y=0):
        orig_w, orig_h = orig_shape
        boxes = []
        classes = []
        scores = []

        for output in outputs:
            tensor = np.asarray(output)
            channels_per_detection = 4 + len(self.class_names)
            channels_with_objectness = channels_per_detection + 1

            # TensorRT returns a flat buffer, while ONNX Runtime commonly
            # returns [1, channels, anchors]. Support both layouts.
            if tensor.ndim == 1:
                if tensor.size % channels_per_detection == 0:
                    channels = channels_per_detection
                elif tensor.size % channels_with_objectness == 0:
                    channels = channels_with_objectness
                else:
                    continue
                preds = tensor.reshape(channels, -1).transpose()
            else:
                tensor = np.squeeze(tensor)
                if tensor.ndim != 2:
                    continue
                if tensor.shape[0] in (channels_per_detection, channels_with_objectness):
                    preds = tensor.transpose()
                elif tensor.shape[1] in (channels_per_detection, channels_with_objectness):
                    preds = tensor
                else:
                    continue

            if preds.shape[1] not in (channels_per_detection, channels_with_objectness):
                continue

            has_objectness = preds.shape[1] == channels_with_objectness
            for pred in preds:
                class_scores = pred[5:] if has_objectness else pred[4:]
                best_cls_id = int(np.argmax(class_scores))
                final_conf = float(class_scores[best_cls_id])
                if has_objectness:
                    final_conf *= float(pred[4])

                if final_conf < self.conf_threshold:
                    continue

                if best_cls_id not in self.class_names:
                    continue

                # Coordinates are already decoded to the 320x320 scale by the engine
                cx, cy, w, h = pred[0], pred[1], pred[2], pred[3]

                # Undo letterbox padding and scale back to the camera frame.
                x1 = ((cx - w / 2.0) - pad_x) / scale
                y1 = ((cy - h / 2.0) - pad_y) / scale
                box_w = w / scale
                box_h = h / scale

                boxes.append([int(x1), int(y1), int(box_w), int(box_h)])
                classes.append(best_cls_id)
                scores.append(final_conf)

        final_boxes = []
        final_classes = []
        final_scores = []

        if len(boxes) > 0:
            indices = cv2.dnn.NMSBoxes(boxes, scores, self.conf_threshold, self.nms_threshold)
            if len(indices) > 0:
                for i in indices.flatten():
                    final_boxes.append(boxes[i])
                    final_classes.append(classes[i])
                    final_scores.append(scores[i])

        return np.array(final_boxes) if final_boxes else np.empty((0, 4)), \
               np.array(final_classes) if final_classes else np.empty((0,)), \
               np.array(final_scores) if final_scores else np.empty((0,))