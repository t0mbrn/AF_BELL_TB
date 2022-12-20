import cv2
import xlsxwriter
import numpy
import matplotlib.pyplot as plt
import random
import array


# Erstellen von Fokusdiagrammen/Fokuskurven von einem Motiv
def open_cam():
    cam = cv2.VideoCapture(0)
    if cam.isOpened():
        return cam
    else:
        return 0


def rate_image(cam: cv2.VideoCapture):
    """ Rating Images based on edges found with Canny Edge-Detector"""
    _, frame = cam.read()
    edges = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # edges = cv2.GaussianBlur(edges, (7, 7), 1.5, 1.5)
    cv2.Canny(edges, 50, 150, edges, 3)  # 0,30
    return len(numpy.argwhere(edges != 0))


values = []


# Erstellen von Excel Tabellen
def excel(data):
    workbook = xlsxwriter.Workbook("FokusDiagramm.xlsx")
    worksheet = workbook.add_worksheet()

    worksheet.write(0, 0, "Focus Value")
    worksheet.write(0, 1, "Anzahl Canny Pixel")
    for rownum, date in enumerate(data):
        worksheet.write(rownum + 1, 0, rownum)
        worksheet.write(rownum + 1, 1, date)

    workbook.close()


def linear(cap):
    cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
    i = 0
    while i <= 255:
        cap.set(cv2.CAP_PROP_FOCUS, i)
        score = rate_image(cap)
        values.append(score)
        i += 1
    # excel(values)
    plt.plot(values)
    plt.title("Lineares Abfragen")
    plt.xlabel("Fokus Position")
    plt.ylabel("Kantenpixel")
    plt.show()


def rand_delay(cap, delay):
    cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
    i = 0
    order = array.array('i', (i for i in range(0, 255)))
    random.shuffle(order)
    scores = array.array('i', (0 for i in range(0, 255)))

    for i in order:
        cap.set(cv2.CAP_PROP_FOCUS, i)
        # delay
        for j in range(delay):
            _, dummy = cap.read()
        score = rate_image(cap)
        scores[i] = score
    # excel(values)
    plt.plot(scores)
    plt.title("Zufälliges Abfragen mit Verzögerung")
    plt.xlabel("Fokus Position")
    plt.ylabel("Kantenpixel")
    plt.show()


def rand(cap):
    cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
    i = 0
    order = array.array('i', (i for i in range(0, 255)))
    random.shuffle(order)
    scores = array.array('i', (0 for i in range(0, 255)))

    for i in order:
        cap.set(cv2.CAP_PROP_FOCUS, i)
        score = rate_image(cap)
        scores[i] = score
    # excel(values)
    plt.plot(scores)
    plt.title("Zufälliges Abfragen ohne Verzögerung")
    plt.xlabel("Fokus Position")
    plt.ylabel("Kantenpixel")
    plt.show()


if __name__ == "__main__":
    cam = open_cam()
    if cam == 0:
        print("Camera couldn't be opened- Aborting ...")
        exit()
    else:
        # normaler Fokusverlauf
        linear(cam)
        rand(cam)
        # Tests von unterschiedlichen Verzögerungen
        rand_delay(cam, 1)
        rand_delay(cam, 2)
        rand_delay(cam, 3)
        cam.release()
