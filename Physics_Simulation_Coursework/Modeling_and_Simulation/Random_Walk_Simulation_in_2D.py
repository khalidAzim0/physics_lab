#استيراد المكتبات
import numpy as np
import matplotlib.pyplot as plt

# 1. تحديد معطيات المحاكاة
N_steps = 1000 

# 2. تجهيز مصفوفات لتخزين إحداثيات (x, y) لكل خطوة
x = np.zeros(N_steps + 1)
y = np.zeros(N_steps + 1)

# 3. حلقة التكرار لمحاكاة الحركة العشوائية خطوة بخطوة
for i in range(1, N_steps + 1):
    step_direction = np.random.randint(1, 5)
    
    if step_direction == 1:
        x[i] = x[i-1] + 1
        y[i] = y[i-1]
        
    elif step_direction == 2:
        x[i] = x[i-1] - 1
        y[i] = y[i-1]
        
    elif step_direction == 3:
        x[i] = x[i-1]
        y[i] = y[i-1] + 1
        
    else:
        x[i] = x[i-1]
        y[i] = y[i-1] - 1

# 4. حساب الإزاحة النهائية
x_final = x[-1] 
y_final = y[-1]
final_displacement = np.sqrt(x_final**2 + y_final**2)

# طباعة النتيجة في الكونسول
print(f"الإزاحة النهائية بعد {N_steps} خطوة هي: {final_displacement:.2f} وحدة")

# 5.الرسم مسار الجسيم
plt.figure(figsize=(8, 8)) 
plt.plot(x, y, color='blue', alpha=0.6, linewidth=1, label='Trajectory')
plt.scatter(0, 0, color='green', marker='o', s=100, label='Start (0,0)', zorder=5)
plt.scatter(x_final, y_final, color='red', marker='X', s=100, label='End', zorder=5)
plt.title('2D Random Walk Simulation', fontsize=14, fontweight='bold')
plt.xlabel('x (Position)', fontsize=12)
plt.ylabel('y (Position)', fontsize=12)
plt.axis('equal') 
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.show()