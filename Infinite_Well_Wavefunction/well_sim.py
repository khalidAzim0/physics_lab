#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  4 13:36:45 2026

@author: khalodi
"""

#استيراد المكتبات 
import numpy as np
import matplotlib.pyplot as plt

#تحديد الثوابت
l=1
n=1

#انشاء المنجه الازاحة
x=np.linspace(0,l,200)

#حساب دالة الموجة
psi=np.sqrt(2/l)*np.sin((n*np.pi*x)/l)

#عملية الرسم البياني
plt.figure(figsize=(8,5))
plt.plot(x, psi, color='blue', linewidth=1, label='مسار المقذوف' )
plt.title('دالة الجهة لجسيم في بئر جهد لانهائي ')
plt.xlabel('الموضع X')
plt.ylabel('دالة الموجة psi')
plt.grid(True)
plt.show()
