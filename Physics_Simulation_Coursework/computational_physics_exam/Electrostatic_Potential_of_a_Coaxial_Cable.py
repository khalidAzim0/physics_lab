#استيراد المكتبات
import numpy as np
import matplotlib.pyplot as plt

# --- 1. إعداد المعلمات الهندسية والفيزيائية ---
R1 = 2.0              # نصف قطر الموصل الداخلي (cm)
R2 = 5.0              # نصف قطر الموصل الخارجي (cm)
V0 = 100.0            # جهد الموصل الداخلي (V)
grid_size = 150      # دقة الشبكة (عدد النقاط)
physical_size = 12.0  # حجم المساحة الكلية للمحاكاة (من -6 إلى 6 سم)

# إنشاء المحاور والشبكة ثنائية الأبعاد
x = np.linspace(-physical_size/2, physical_size/2, grid_size)
y = np.linspace(-physical_size/2, physical_size/2, grid_size)
X, Y = np.meshgrid(x, y)
R = np.sqrt(X**2 + Y**2) # مصفوفة تحتوي على بُعد كل نقطة عن المركز

# --- 2. إعداد مصفوفة الجهد وشروط الحدود ---
V = np.zeros((grid_size, grid_size))

# تحديد مناطق الموصلات باستخدام (Masks)
inner_mask = R <= R1
outer_mask = R >= R2

# تطبيق شروط ديريشليت (Dirichlet Boundary Conditions)
V[inner_mask] = V0
V[outer_mask] = 0.0

# --- 3. الحل العددي باستخدام طريقة جاكوبي (Jacobi Method) ---
max_iter = 4000 # عدد التكرارات (كلما زاد، زادت الدقة واقترب النظام من الاتزان)
for _ in range(max_iter):
    V_next = np.copy(V)
    # تحديث النقاط الداخلية بحساب متوسط النقاط الأربع المجاورة
    V_next[1:-1, 1:-1] = 0.25 * (V[2:, 1:-1] + V[:-2, 1:-1] + V[1:-1, 2:] + V[1:-1, :-2])
    
    # إعادة تثبيت الجهد على الحدود لأن التحديث السابق قد يغيرها
    V_next[inner_mask] = V0
    V_next[outer_mask] = 0.0
    
    V = V_next # الانتقال للخطوة الزمنية/التكرارية التالية

# --- 4. الحساب التحليلي للمقارنة (Analytical Solution) ---
# نستخرج خطاً واحداً من المركز إلى الحافة (على طول المحور السيني مثلاً)
mid_index = grid_size // 2
r_axis = x[mid_index:]       # المسافة من المركز (r)
V_numerical_1D = V[mid_index, mid_index:] # الجهد العددي المقابل لهذه المسافات

# حساب الجهد التحليلي لنفس المسافات
V_analytical_1D = np.zeros_like(r_axis)
for i, r_val in enumerate(r_axis):
    if r_val <= R1:
        V_analytical_1D[i] = V0
    elif r_val >= R2:
        V_analytical_1D[i] = 0.0
    else:
        # تطبيق المعادلة المعطاة في المشروع
        V_analytical_1D[i] = V0 * (np.log(R2 / r_val) / np.log(R2 / R1))

# --- 5. رسم واستخراج النتائج (Deliverables) ---
plt.figure(figsize=(14, 6))

# الرسم الأول: خريطة الألوان لتوزيع الجهد (2D Potential Distribution)
plt.subplot(1, 2, 1)
plt.imshow(V, extent=[-physical_size/2, physical_size/2, -physical_size/2, physical_size/2], origin='lower', cmap='inferno')
plt.colorbar(label='Potential V(x,y) [Volts]')
# رسم دوائر توضح حدود الموصلات
circle1 = plt.Circle((0, 0), R1, color='white', fill=False, linestyle='--')
circle2 = plt.Circle((0, 0), R2, color='white', fill=False, linestyle='--')
plt.gca().add_patch(circle1)
plt.gca().add_patch(circle2)
plt.title('2D Potential Distribution of Coaxial Cable')
plt.xlabel('x (cm)')
plt.ylabel('y (cm)')

# الرسم الثاني: مقارنة الحل العددي بالتحليلي (Comparison Plot)
plt.subplot(1, 2, 2)
plt.plot(r_axis, V_numerical_1D, 'bo', label='Numerical (FDM)', markersize=4)
plt.plot(r_axis, V_analytical_1D, 'r-', label='Analytical Solution', linewidth=2)
plt.title('Comparison: Numerical vs Analytical')
plt.xlabel('Radial distance r (cm)')
plt.ylabel('Potential V(r) [Volts]')
plt.axvline(R1, color='gray', linestyle='--', label='Inner Conductor (R1)')
plt.axvline(R2, color='gray', linestyle='-.', label='Outer Conductor (R2)')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()