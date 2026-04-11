# الخطوة الأولى: استدعاء المكتبات
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# الخطوة الثانية: تعريف النظام الفيزيائي
def damped_oscillator(t, y, m, c, k):
    x, v = y
    dxdt = v
    dvdt = -(c / m) * v - (k / m) * x
    return [dxdt, dvdt]

# الخطوة الثالثة: إدخال بيانات المشكلة (المعاملات والشروط الابتدائية)
m = 1.0  
c = 0.5  
k = 10.0
x0 = 1.0
v0 = 0.0
initial_conditions = [x0, v0] 

# الخطوة الرابعة: تحديد الزمن والحل العددي
t_span = (0.0, 20.0)
t_eval = np.linspace(0.0, 20.0, 500)

solution = solve_ivp(
    fun=damped_oscillator,
    t_span=t_span,
    y0=initial_conditions,
    t_eval=t_eval,
    args=(m, c, k)
)

# الخطوة الخامسة: رسم النتائج البيانية
plt.figure(figsize=(10, 6)) 
plt.plot(solution.t, solution.y[0], label='Displacement x(t)', color='blue', linewidth=2)
plt.axhline(0, color='black', linestyle='--', linewidth=0.8)
plt.title('Damped Harmonic Oscillator Simulation', fontsize=14)
plt.xlabel('Time t (seconds)', fontsize=12)
plt.ylabel('Displacement x (meters)', fontsize=12)
plt.grid(True, linestyle=':')
plt.legend()
plt.show()