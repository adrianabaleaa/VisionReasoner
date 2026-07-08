from collections import Counter
import math 


# ==========================================================
# SCENE KNOWLEDGE BASE
# ==========================================================

SCENE_RULES = {

    "Busy Road": [
        "car",
        "truck",
        "bus",
        "motorcycle",
        "traffic light",
        "stop sign"
    ],

    "Living Room": [
        "tv",
        "couch",
        "chair",
        "potted plant",
        "book"
    ],

    "Bedroom": [
        "bed",
        "book",
        "chair"
    ],

    "Office": [
        "laptop",
        "keyboard",
        "mouse",
        "chair",
        "tv"
    ],

    "Dining Room": [
        "dining table",
        "chair",
        "cup",
        "bottle"
    ]
}


INDOOR_OBJECTS = [
    "chair",
    "couch",
    "tv",
    "bed",
    "book",
    "laptop",
    "keyboard",
    "mouse",
    "dining table",
    "refrigerator",
    "oven"
]

OUTDOOR_OBJECTS = [
    "car",
    "truck",
    "bus",
    "motorcycle",
    "traffic light",
    "stop sign",
    "bench",
    "bicycle"
]

# ==========================================================
# COUNT OBJECTS
# ==========================================================

def count_objects(detected_objects):

    counts = Counter()

    for obj in detected_objects:
        counts[obj["object"]] += 1

    return dict(counts)


# ==========================================================
# ESTIMATE SCENE
# ==========================================================

def estimate_scene(object_counts):

    best_scene = "Unknown"
    best_score = 0

    for scene, objects in SCENE_RULES.items():

        score = 0

        for obj in objects:

            if obj in object_counts:
                score += object_counts[obj]

        if score > best_score:
            best_score = score
            best_scene = scene

    return best_scene


# ==========================================================
# VEHICLE DENSITY
# ==========================================================

def analyze_density(object_counts):

    vehicles = (
        object_counts.get("car", 0)
        + object_counts.get("truck", 0)
        + object_counts.get("bus", 0)
        + object_counts.get("motorcycle", 0)
    )

    if vehicles >= 20:
        return "Very high"

    elif vehicles >= 10:
        return "High"

    elif vehicles >= 5:
        return "Moderate"

    elif vehicles > 0:
        return "Low"

    return "None"


# ==========================================================
# OBJECT SUMMARY
# ==========================================================

def build_object_summary(object_counts):

    summary = ""

    for obj, count in sorted(object_counts.items()):

        summary += f"- {obj}: {count}\n"

    return summary


# ==========================================================
# ENVIRONMENT ESTIMATION
# ==========================================================

def estimate_environment(object_counts):

    indoor_score = 0
    outdoor_score = 0

    for obj, count in object_counts.items():

        if obj in INDOOR_OBJECTS:
            indoor_score += count

        if obj in OUTDOOR_OBJECTS:
            outdoor_score += count

    if indoor_score > outdoor_score:
        return "Indoor"

    elif outdoor_score > indoor_score:
        return "Outdoor"

    return "Unknown"


# ==========================================================
# POSITIONS ANALYZER
# ==========================================================

def analyze_positions(detected_objects, width, height):

    positions = []

    for obj in detected_objects:

        x1, y1, x2, y2 = obj["bbox"]

        cx = (x1 + x2) / 2
        cy = (y1 + y2) / 2

        # Horizontal position

        if cx < width / 3:
            horizontal = "left"
        elif cx < 2 * width / 3:
            horizontal = "center"
        else:
            horizontal = "right"

        # Vertical position
        if cy < height / 3:
            vertical = "top"
        elif cy < 2 * height / 3:
            vertical = "middle"
        else:
            vertical = "bottom"

        positions.append(
            {
                "object": obj["object"],
                "position": f"{vertical} {horizontal}"
            }
        )

    summary = ""

    grouped = {}

    for p in positions:

        grouped.setdefault(
            p["object"],
            []
        ).append(
            p["position"]
        )

    for obj, pos_list in grouped.items():

        most_common = Counter(pos_list).most_common(1)[0][0]

        summary += f"Most {obj}s are located in the {most_common} of the image.\n"

    return summary


# ==========================================================
# NEARBY OBJECTS
# ==========================================================

def find_nearby_objects(detected_objects, width, height):

    relations = []
    threshold = min(width, height) * 0.12

    for i in range(len(detected_objects)):

        obj1 = detected_objects[i]

        x1, y1, x2, y2 = obj1["bbox"]

        cx1 = (x1 + x2) / 2
        cy1 = (y1 + y2) / 2

        for j in range(i + 1, len(detected_objects)):

            obj2 = detected_objects[j]

            x1, y1, x2, y2 = obj2["bbox"]

            cx2 = (x1 + x2) / 2
            cy2 = (y1 + y2) / 2

            distance = math.sqrt(
                (cx1 - cx2) ** 2 +
                (cy1 - cy2) ** 2
            )

            if distance < threshold:

                relations.append(
                    f"{obj1['object']} is near {obj2['object']}"
                )

    if not relations:

        return "No nearby object relationships detected."

    return "\n".join(relations)


# ==========================================================
# MAIN FUNCTION
# ==========================================================

def analyze_scene(detected_objects, width, height):

    object_counts = count_objects(detected_objects)

    estimated_scene = estimate_scene(object_counts)

    density = analyze_density(object_counts)

    estimated_environment= estimate_environment(object_counts)

    position_summary = analyze_positions(detected_objects, width, height)

    nearby_summary = find_nearby_objects(detected_objects, width, height)

    summary = f"""
Scene Analysis

Estimated scene:
{estimated_scene}

Object statistics:

{build_object_summary(object_counts)}

Vehicle density:
{density}

Environment:
{estimated_environment}

Object positions:

{position_summary}

"""
    return summary