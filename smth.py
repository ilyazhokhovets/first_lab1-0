import numpy as np
from PIL import Image
import os
f = os.getcwd()
x = Image.open(f+'/flaskapp/static/hqdefault.jpeg')
t = np.array((x))
print(t)
w = Image.fromarray(t)
w.save(f+'/flaskapp/static/hqdefault1.jpeg')