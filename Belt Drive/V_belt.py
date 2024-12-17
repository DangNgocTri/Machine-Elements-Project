print("V-belt design")
print("Input require: Capacity, Number of revolutions in small pulley (rpm) and Transmission ratio ")
import math, sys
# Input parameters
Pow = float(input("Capacity P = "))
n1 = float(input("Num. of revs. n1 = "))
u = float(input("Speed ratio u = "))
# Standard sizes
standard_sizes = [
        40, 45, 50, 56, 63, 71, 80, 90, 100, 110,
        125, 140, 160, 180, 200, 225, 250, 280, 320, 360,
        400, 450, 500, 560, 630, 710, 800, 900, 1000, 1250,
        1400, 1600, 1800, 2000
    ]
standard_length = [
    400, 450, 500, 560, 630, 710, 800, 900, 1000, 1120, 1250, 1400, 1600, 1800, 2000,
    2240, 2500, 2800, 3150, 3550, 4000, 5000, 5600, 6300, 7100, 8000, 9000, 10000,
    11200, 12500, 14000, 16000, 18000
]
# 1. Based on Figure 4.22-[1], select the most suitable 
# belt type follow table 4.3, then input these parameters
# input("Type of belt : ")
input("Symbol : ")
print("Input parameters of th selected belt")
bp = float(input("bp = "))
bo = float(input("bo = "))
h = float(input("h = "))
yo = float(input("yo = "))
Area = float(input("A = "))
dmin = float(input("dmin = "))
dmax = float(input("dmax = "))

# 2. Cal d1
d1_cal = 1.2*dmin
def round_up_to_higher_value(d1_cal, standard_sizes):
    # Find the higher value in the standard group next to the given value
    for standard_value in standard_sizes:
        if standard_value > d1_cal:
            return standard_value
    return None  # Return None if no suitable value is found
d1 = round_up_to_higher_value(d1_cal, standard_sizes)
print("Recommend smallest value according to standard in page 159-[1], d1 = ",d1)
d1 = float(input("Choose d1 = "))

# 3. Cal d2, new ratio and error
while (True):
    epsilon = float(input("Choose epsilon = "))
    if ( epsilon < 0.01  or epsilon > 0.02) :
        print("input epsilon again")
    else:
        break
d2_value = d1*(1-epsilon)*u
def select_nearest_d2(d2_value):
     # Find the standard size closest to d2_value
    d2 = min(standard_sizes, key=lambda x: abs(x - d2_value))
    return d2
d2 = select_nearest_d2(d2_value)
print("Calulating d2:",d2_value)
print("Selected nearest standard size for d2:",d2)
u_n = d2/(d1*(1-epsilon))
error = (u-u_n)/u*100
print("Calulating new ratio u_new = ",u_n)
print("The error between the pre-selected and the re-calculated transmission ratio is",error,"%")

# 4. Cal axial distance and select belt length
a_max = 2*(d1 + d2)
a_min = 0.55*(d1 + d2) + h
print(f"Selected axial distance {a_min} <= a <= {a_max} in standard sizes")
a = float(input("Choose primary axial distance a = "))
# Check if the value is in the list of standard sizes
def check_value_in_standard_sizes(a, standard_sizes):
    return a in standard_sizes
if check_value_in_standard_sizes(a, standard_sizes):
    print(f"Axial distance a = {a} is satified standard sizes.")
else:
    print(f"Axial distance a = {a} is not satified standard sizes.")
# Cal Length of belt
Length_min = round(2*a + math.pi*(d1+d2)/2 + (d2-d1)**2/(4*a),1)
print(f"Calculating Length_min = {Length_min} mm")
Length = float(input("Choose belt length L = "))
if check_value_in_standard_sizes(Length, standard_length):
    print(f"L = {Length} is satified standard sizes.")
else:
    print(f"L = {Length} is not satified standard sizes.")

# 5. Cal Velocity v1
# Velocity
v1 = math.pi*n1*d1/60000
print(f"Velocity v1 = {v1 } m/s.")
# Num. of revs per s
i = 1000*v1/Length
if (i <= 10):
    print(f"i = {i} <= 10 is satified.")
else:
    print(f"i = {i} > 10  is not satified.")
# Re cal axial distance
k = Length - math.pi*(d1 + d2)/2
delta = (d2 - d1)/2
a = round((k + math.sqrt(k**2 - 8*delta**2))/4,1)
print("Calulating k = ",k)
print("Calulating delta = ",delta)
print("Recalulating a = ",a)
if ( a_min <= a <= a_max):
    print(f"Axial distance a = {a} is satified.")
else:
    print(f"Axial distance a = {a} is not satified.")

# 6. Cal Wrap angle
alpha1 = math.pi - (d2-d1)/a
print(f"Wrap angle alpha1 = {alpha1}rad.")

# 7. Cal Ci
C_a = 1.24*(1 - math.e**(-1*alpha1*180/(110*math.pi)))
print("Hugging angle factor C_a = ",C_a)
C_v = 1 - 0.05*(0.01*v1**2 - 1)
print("Velocity factor C_v = ",C_v)
Lo = float(input("Based on table 4.8, choose Lo = "))
C_Len = (Length/Lo)**(1/6)
print("Length factor C_Len = ",C_Len)
C_z = float(input("Primary Num. of belts factor C_z = "))
C_u = float(input("Ratio factor C_u = "))
C_r = float(input("Shock factor C_r = "))
C_all = C_a*C_u*C_Len*C_z*C_r*C_v # Load factor
Po = float(input("Based on table 4.8, choose Po = "))
z_cal = Pow/(Po*C_all)
z = round(z_cal)
print("Number of belts z >= ",z_cal , ". Choose z = ",z)

# 8. Initial force
# with V-belt: sigma0 = 1.5 MPa
sigma_0 = 1.5
Fo = z*Area*sigma_0
print("Initial force Fo = ",Fo)
Ft = round(1000*Pow/v1,1)
print("Tension force Ft = ",Ft)

# 9. Force on shaft
Fr = 2*Fo*math.sin(alpha1/2)
print("Force on shaft Fr = ",Fr)
density = float(input("Selecting density in page 133-[1], p = "))
sigma0 = Fo/(Area*z)
sigmaT = Ft/(Area*z)
sigmaV = density*v1**2*10**(-6)
sigma1 = sigma0 + sigmaT/2
sigmaF = (2*yo)/d1*100 # Elastic modulus E = 100 MPa

# 10. Maximum Stress
print(" Sigma0 = ", sigma0)
print(" SigmaT = ", sigmaT)
print("Centrifugal stress SigmaV = ", sigmaV)
print("Bending stress SigmaF = ", sigmaF)
sigma_max = sigma1 + sigmaV + sigmaF
print("Maximum Stress sigma_max = ", sigma_max)

# 11. Lifespan
# V-belt 𝑚=8 , i < [i], [i] = 10
sigmaR = float(input("In page 156, choose sigmaR = "))
Lh = ((sigmaR / sigma_max)**8*10**7)/(2*3600*i)
print("Lifespan Lh = ", Lh)

x = input("Enter to End the program")
