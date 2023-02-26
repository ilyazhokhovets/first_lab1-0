import os
from math import cos

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

# функция преобразования изображения
def convert_image(filename, period=0):
 # читаем файл с диска
 directory = os.getcwd()
 img = Image.open(directory+'/static/'+filename)

 #переводим изображение в массив numpy
 img_arr = np.array(img)

 #разделяем на три массива, каждого цвета
 r = img_arr[:,:,0]
 g = img_arr[:,:,1]
 b = img_arr[:,:,2]

 # по очередно преобразуем каждый цвет
 r = _convert_layer(r, period)
 g = _convert_layer(g, period)
 b = _convert_layer(b, period)

 #складываем все слои обратный в один тензор
 l = []
 for i,j,k in zip(r,g,b):
  z = []
  for v in range(len(i)):
   z.append([i[v],j[v],k[v]])
  l.append(z)
 l = np.array(l, dtype=float)
 max_ = np.max(l)
 min_ = np.min(l)
 # l = np.array(l)
 l = (l - min_) / (max_ - min_)
 # приводим тензор к виду, который PIL сможет прочитать
 l = l * 255
 l = l.astype(np.uint8)
 img_new = Image.fromarray(l)

 # изменяем название нового файла
 name, extension = filename.rsplit('.',1)
 name += '_new'

 # сохраняем
 img_new.save(directory+'/static/'+name+'.'+extension)

 #возвращаем название файла
 return name+'.'+extension


#в этой функции преобразуется каждый цвет
def _convert_layer(layer, period):
 l = []

 #составляем новую картинку путем умножения старой на cos
 for i,n in enumerate(layer):
  temp = []
  for j,m in enumerate(n):
   temp.append(m*cos(period*((i+j)/2)))
  l.append(temp)

 # #нормируем
 # max_ = np.max(l)
 # min_ = np.min(l)
 l = np.array(l)
 # l = (l - min_) / (max_ - min_)
 return l

# распеределение цветов
def color_distribution(img_arr):
 r = img_arr[:,:,0]
 g = img_arr[:,:,1]
 b = img_arr[:,:,2]
 avr_r = np.average(r)
 avr_b = np.average(b)
 avr_g = np.average(g)
 return (avr_r, avr_g, avr_b)

#в этой функции строим график, полученного распределения и сохраняем в файл
def color_distribution_image(filename, img_arr):
 directory = os.getcwd()
 plt.rcdefaults()
 colors = ('Red', 'Green', 'Blue')
 y_pos = np.arange(len(colors))
 performance = color_distribution(img_arr)
 fig, ax = plt.subplots()

 ax.barh(y_pos, performance, color=colors, align='center')
 ax.set_yticks(y_pos, labels=colors)
 ax.invert_yaxis()
 ax.set_xlabel('Среднее значение цвета')

 name, res = filename.rsplit('.', 1)
 name += '_colormap'
 saved_plot = f'{directory}/static/{name}.{res}'
 fig.savefig(saved_plot)
 return f'{name}.{res}'

