import cv2
import numpy as np
import torch

model = torch.load("best.pt")

img = cv2.imread("img.jpg")
height, width, _ = img.shape
img = cv2.resize(img, (640, 640))
img = np.transpose(img, (2, 0, 1))
img = img.astype(np.float32)
img = torch.from_numpy(img)
