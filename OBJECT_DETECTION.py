from collections import Counter
from ultralytics import YOLO



# LOAD MODEL
model = YOLO("yolov8n.pt")



# OBJECT DETECTION
def detect_objects(image_path):

    results = model(image_path)
    result = results[0]

    height, width = result.orig_shape

    detected_objects = []

    for box in result.boxes:

        class_id = int(box.cls[0])
        class_name = model.names[class_id]

        confidence = float(box.conf[0])

        x1, y1, x2, y2 = box.xyxy[0].tolist()

        detected_objects.append(
            {
                "object": class_name,
                "confidence": round(confidence, 2),
                "bbox": [
                    round(x1),
                    round(y1),
                    round(x2),
                    round(y2)
                ]
            }
        )


    return detected_objects, result, height, width




# BUILD PROMPT
def build_prompt(scene_analysis, user_question):

    prompt = f"""
You are VisionReasoner.

The following information was extracted from the image
using an object detection model and a scene analysis module.

{scene_analysis}

User question:
{user_question}

Instructions:

- Answer naturally in complete sentences.
- Base your answer only on the provided scene analysis.
- Never invent objects or events.
- If there is insufficient evidence, clearly explain why.
"""

    return prompt



