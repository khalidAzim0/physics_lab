# -*- coding: utf-8 -*-
"""
Created on Mon Feb  9 13:10:52 2026

@author: KH A
"""

import numpy as np
import matplotlib.pyplot as plt

#المعطات الثوات
g=9.81
l=1.5
theta=15

theta_r=np.radians(theta)

t=np.linspace(0, 15, 200)
theta_t = theta_r*np.cos(np.sqrt(g/l)*t) 

#الرسم البياني
plt.figure(figsize=(8, 4))
plt.plot(t, theta_t, color='red')
plt.title('Simple Pendulum (Degrees to Radians)')
plt.xlabel('Time (s)')
plt.ylabel('Angle (Radians)')
plt.grid(True)

plt.show()