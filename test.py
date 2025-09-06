# Read chuck the file !!
# with open("saida.bin", "wb") as f:
#     while chunk := await file.read(1024 * 1024):  # lê 1MB por vez
#         f.write(chunk)

from deepface import DeepFace
import matplotlib.pyplot as plt
import cv2
import os

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import tensorflow as tf

face = DeepFace.detectFace('database/lucas.jpg', target_size=(224, 224), detector_backend='opencv')
plt.imshow(face)