from numpy import load
import numpy as np


data = load('C:/project/be/data/registered/registered_students.npz')
npz_faces, npz_labels = data['arr_0'], data['arr_1']



print(npz_faces)

