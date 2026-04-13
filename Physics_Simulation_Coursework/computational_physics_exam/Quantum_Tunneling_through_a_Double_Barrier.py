#استيراد المكتبات
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.sparse import diags
from scipy.sparse.linalg import spsolve
#==============================================================================
# 1. إعدادات الشبكة المكانية والزمنية 
L = 20.0          # طول المجال المكاني
Nx = 800          # عدد النقاط لضمان دقة مكانية جيدة
x = np.linspace(0, L, Nx)
dx = x[1] - x[0]

dt = 0.005        # خطوة الزمن
Nt = 800          # عدد خطوات المحاكاة الكلية
#==============================================================================
# 2. تعريف دالة الجهد المزدوج (Double Potential Barrier)
# V(x) = VB for x in [8,9] and x in [11,12]
V = np.zeros(Nx)
V_B = 60.0        # تعيين ارتفاع الحاجز
V[(x >= 8.0) & (x <= 9.0)] = V_B
V[(x >= 11.0) & (x <= 12.0)] = V_B
#==============================================================================
# 3. الحزمة الموجية الابتدائية (Initial Wave Packet)
x0 = 5.0          # الموضع الابتدائي المطلوب في المشروع
sigma = 0.5       # عرض الحزمة (الانحراف المعياري)
k0 = 12.0         # الزخم الابتدائي لضمان حركة الحزمة نحو الحاجز

# الدالة الموجية الابتدائية (Gaussian Wave Packet)
psi0 = np.exp(-0.5 * ((x - x0) / sigma)**2) * np.exp(1j * k0 * x)
# معايرة الدالة الموجية (Normalization) لضمان أن الاحتمالية الكلية تساوي 1
psi0 = psi0 / np.sqrt(np.trapz(np.abs(psi0)**2, dx=dx))
#==============================================================================
# 4. إعداد مصفوفات طريقة كرانك-نيكولسون (Crank-Nicolson Method)
# المعادلة تأخذ الشكل: A * psi_new = B * psi_old
r = 1j * dt / (4.0 * dx**2)

# بناء المصفوفة A (التي تضرب في الخطوة الزمنية الجديدة)
main_diag_A = 1.0 + 2.0*r + 1j * (dt/2.0) * V
off_diag_A = -r * np.ones(Nx - 1)
A = diags([off_diag_A, main_diag_A, off_diag_A], [-1, 0, 1], format='csr')

# بناء المصفوفة B (التي تضرب في الخطوة الزمنية الحالية)
main_diag_B = 1.0 - 2.0*r - 1j * (dt/2.0) * V
off_diag_B = r * np.ones(Nx - 1)
B = diags([off_diag_B, main_diag_B, off_diag_B], [-1, 0, 1], format='csr')
#==============================================================================
# 5. محاكاة التطور الزمني (Time Evolution)
psi_history = []
psi_current = psi0.copy()

for i in range(Nt):
    if i % 2 == 0:  # حفظ إطار واحد كل خطوتين لتسريع الأنيميشن
        psi_history.append(psi_current.copy())
    
    # حساب الطرف الأيمن للمعادلة
    b = B.dot(psi_current)
    # حل النظام الخطي المتمثل في المصفوفات المتفرقة (Sparse Matrices)
    psi_next = spsolve(A, b)
    psi_current = psi_next
#==============================================================================
# 6. الرسوم المتحركة (Animation)
fig, ax = plt.subplots(figsize=(10, 6))

# رسم الجهد في الخلفية (مع ضبط المقياس ليناسب رسم الاحتمالية)
max_prob = np.max(np.abs(psi0)**2)
ax.plot(x, V / V_B * max_prob, 'k-', linewidth=2, alpha=0.5, label='Double Barrier V(x)')

# تهيئة خط كثافة الاحتمالية
line, = ax.plot([], [], 'b-', linewidth=2, label=r'Probability Density $|\Psi(x,t)|^2$')

ax.set_xlim(0, 20)
ax.set_ylim(0, max_prob * 1.1)
ax.set_xlabel('Position x')
ax.set_ylabel(r'$|\Psi|^2$')
ax.set_title('Time Evolution of a Wave Packet (Crank-Nicolson)')
ax.legend(loc='upper right')
ax.grid(True, linestyle='--', alpha=0.6)

def init():
    line.set_data([], [])
    return line,

def animate(i):
    y = np.abs(psi_history[i])**2
    line.set_data(x, y)
    return line,

# تشغيل الأنيميشن
ani = FuncAnimation(fig, animate, frames=len(psi_history), init_func=init, blit=True, interval=20)
plt.show()