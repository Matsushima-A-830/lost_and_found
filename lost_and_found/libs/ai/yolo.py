# YOLOv8 推論ラッパー（ダミー実装）
import numpy as np
from typing import List

class DetectedItem:
    def __init__(self, label: str, confidence: float, bbox: list):
        self.label = label
        self.confidence = confidence
        self.bbox = bbox

def detect_objects(image: np.ndarray) -> List[DetectedItem]:
    # ダミー: 常に1件返す
    return [DetectedItem(label="bag", confidence=0.95, bbox=[10, 10, 100, 100])]
