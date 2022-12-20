import cv2

import main
import rating


def find_max(cam: cv2.VideoCapture, focus: main.state):
    """
    Maximum search based on Hill-Climbing
    (Tom Braune)
    """

    # Check for Overflow
    if focus["step"] in {0, 255}:
        focus["initial"] = True
        focus["step"] = 0
        cam.set(cv2.CAP_PROP_FOCUS, focus["step"])
        focus["step_direction_changes"] = 0

    elif focus["rating_current"] < focus["rating_previous"]:
        # Inverting direction
        focus["step_direction"] = - focus["step_direction"]
        focus["step_direction_changes"] = focus["step_direction_changes"] + 1
        # Calculating new step w/out if based on sign of step direction (either -/+)
        focus["step"] = focus["step"] + focus["step_direction"] * 5
        cam.set(cv2.CAP_PROP_FOCUS, focus["step"])

    else:
        focus["step_direction_changes"] = 0  # evt überarbeiten
        focus["step"] = focus["step"] + focus["step_direction"] * 5
        cam.set(cv2.CAP_PROP_FOCUS, focus["step"])


def adjust_focus(cam: cv2.VideoCapture, focus: main.state):
    if focus["rating_current"] > focus["rating_max"] or focus["step_direction_changes"] > 4:
        focus["rating_max"] = focus["rating_current"]
        focus["step_max"] = focus["step"]
        find_max(cam, focus)

    else:
        focus["stack"].append(focus["rating_current"])
        if len(focus["stack"]) > 100:
            focus["stack"].pop()
            mean = (sum(focus["stack"]) / len(focus["stack"]))
            if focus["rating_current"] < 0.8 * mean:  # Durchschnitt letzte Hundert Scores
                focus["lower"] += 1
                focus["higher"] = 0
            elif focus["rating_current"] > 1.2 * mean:
                focus["higher"] += 1
                focus["lower"] = 0
            if (focus["lower"] > 30) or (focus["higher"] > 30):
                focus["initial"] = True
                focus["step"] = 0
                cam.set(cv2.CAP_PROP_FOCUS, focus["step"])
                focus["stack"] = []
                focus["lower"] = 0
                focus["higher"] = 0


def initial_scan(cam: cv2.VideoCapture, focus: main.state):
    """
    Scanning focus settings from 0 to 255 for maxima
    """

    if focus["rating_current"] > focus["initial_max"]:
        focus["initial_max"] = focus["rating_current"]
        focus["initial_max_step"] = focus["step"]

    if focus["step"] < 255:
        focus["step"] = focus["step"] + 10
        cam.set(cv2.CAP_PROP_FOCUS, focus["step"])
    else:
        focus["step"] = focus["initial_max_step"]
        cam.set(cv2.CAP_PROP_FOCUS, focus["step"])
        focus["rating_max"] = focus["initial_max"]
        focus["initial_max_step"] = 0
        focus["initial_max"] = 0
        focus["initial"] = False
        print("Initialization complete")


def find_max_bisection(cam: cv2.VideoCapture):
    """
     Maximum search based on Bisection
     (Ralf Hubert, Tom Braune)
     """
    left = 0
    right = 255

    count = 0
    max_focus = [0, 0]
    unchanged_max = 0
    while count < 10:
        count += 1
        middle = int(left + (right - left) / 2)

        sample_point_l = int(left + (middle - left) / 2)
        sample_point_r = int(middle + (right - middle) / 2)

        cam.set(cv2.CAP_PROP_FOCUS, sample_point_l)
        # delay
        for _ in range(2):
            _, dummy = cam.read()

        _, frame = cam.read()
        print(cam.get(cv2.CAP_PROP_FOCUS))
        focus_l = rating.rate_image(frame)

        cam.set(cv2.CAP_PROP_FOCUS, sample_point_r)

        _, frame = cam.read()
        focus_r = rating.rate_image(frame)

        if focus_l > max_focus[0]:
            max_focus = [focus_l, sample_point_l]
            unchanged_max = 0
        elif focus_r > max_focus[0]:
            max_focus = [focus_r, sample_point_r]
            unchanged_max = 0
        else:
            if sample_point_l < max_focus[1]:
                left += 1
            else:
                right -= 1
            unchanged_max += 1
            if unchanged_max > 2: break
            if abs(left - right) < 4: break
            continue

        if focus_l > focus_r:
            right = middle
        else:
            left = middle

    return max_focus
