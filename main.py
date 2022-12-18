import cv2

import focus
import rating


def open_cam():
    cam = cv2.VideoCapture(0)
    if cam.isOpened():
        return cam
    else:
        return 0


state = {
    "rating_current": 0,
    "rating_previous": 0,
    "rating_max": 0,

    "step": 0,

    "initial": True,
    "initial_max": 0,
    "initial_max_step": 0,

    "similar_count": 0,

    # "step_max": 0,  # FIXME change wenn über x% Unterschied?
    # "step_toMax": 0,  # steps since last max
    "step_direction": 1,  # 1-> pos, -1-> neg
    "step_direction_changes": 0  # wenn 5 (hintereinander), dann neues lokales Max?
}


def start_custom_af(cam: cv2.VideoCapture, focus_state: state):
    while True:

        ret, frame = cam.read()
        cv2.imshow('frame', frame)

        focus_state["step"] = cam.get(cv2.CAP_PROP_FOCUS)
        # print(state["step"], " vs ", cam.get(cv2.CAP_PROP_FOCUS))
        focus_state["rating_previous"] = focus_state["rating_current"]
        focus_state["rating_current"] = rating.rate_image(frame)
        if focus_state["initial"]:
            cam.set(cv2.CAP_PROP_FOCUS, 0)
            focus.initial_scan(cam, focus_state)
        else:
            focus.adjust_focus(cam, focus_state)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()


def start_bisect_af(cam: cv2.VideoCapture):
    init = True
    score = 0
    step = 0
    lower = 0
    higher = 0
    last_hundred = []  # Speicher für letzte 100 scores
    while True:

        _, frame = cam.read()
        cv2.imshow('frame', frame)

        if init:
            print("init")

            score, step = focus.find_max_bisection(cam)
            cam.set(cv2.CAP_PROP_FOCUS, step)
            print("max ", score, "@", step)
            init = False
            last_hundred.append(score)
        else:
            # scene change detection
            new_score = rating.rate_image(frame)
            last_hundred.append(score)
            if len(last_hundred) > 100:
                last_hundred.pop()
                if new_score < 0.8 * (sum(last_hundred) / len(last_hundred)):  # Durchschnitt letzte Hundert Scores
                    lower += 1
                    higher = 0
                elif new_score > 1.2 * (sum(last_hundred) / len(last_hundred)):
                    higher += 1
                    lower = 0
                if (lower > 30) or (higher > 30):
                    init = True
                    last_hundred = []
                    lower = 0
                    higher = 0

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    cap = open_cam()
    if cap == 0:
        print("Camera couldn't be opened- Aborting ...")
        exit()
    else:
        cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
        cap.set(cv2.CAP_PROP_FOCUS, 0)
        print("AF by Tom Braune")
        method = input("1 - Bisection \nor \n2 - Hill Climbing? ")
        if method == "1":
            start_bisect_af(cap)
        elif method == "2":
            start_custom_af(cap, state)
        else:
            print("Invalid input - Aborting ...")
