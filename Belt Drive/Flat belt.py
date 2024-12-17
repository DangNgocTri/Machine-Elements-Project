print("Flat belt design")
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
standard_width = [
        10, 16, 20, 25, 32, 40, 50, 63, 65, 71, 80, 90, 100, 112,
        115, 120, 125, 140, 160, 180, 200, 224, 250, 280,
        315, 355, 400, 450, 500, 560, 600, 700, 800, 900, 1000,
        1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000
]

# 1. Selecting type and material
# In this project, selecting material is integrated in section 9
# 2. Cal d1
d1min = 1100*((Pow/n1)**(1/3))
d1max = 1300*((Pow/n1)**(1/3))
print("d1 from ",d1min,"to",d1max)
def select_d1(d1min, d1max):
    # Filter standard sizes within the range (d1min, d1max)
    valid_sizes = [size for size in standard_sizes if d1min < size < d1max]
    # Return the first valid size or None if no size is valid
    return valid_sizes[0] if valid_sizes else None
d1 = select_d1(d1min, d1max)
if d1:
    print(f"Selected d1: {d1}")
else:
    print("No suitable d1 found within the given range.")

# 3. Cal V
v1 = math.pi*d1*n1/60000
print("Velocity v1 =", v1, "m/s")

# 4. Cal d2, new ratio and error
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
u_n = d2/d1
error = (u-u_n)/u*100
print("Calulating new ratio u_new = ",u_n)
print("The error between the pre-selected and the re-calculated transmission ratio is",error,"%")

# 5. Cal the axial distance a
a_min = 2*(d1+d2)
print("input axial distance between ", a_min, "mm and 15m")
while (True):
    a = float(input("Choose axial distance = "))
    if ( a < a_min  or a > 15000) :
        print("input axial distance again")
    else:
        break
print("Center distance a =", a, "mm")

# 6. Cal Length
Length_min = round(2*a + math.pi*(d1+d2)/2 + (d2-d1)**2/(4*a))
print("Length >= = ", Length_min)
def adjust_to_multiple_of_100(Length_min, min_add=100, max_add=400):
    # Iterate through possible additions in the range [min_add, max_add]
    for add in range(min_add, max_add + 1):
        Length = Length_min + add
        if Length % 100 == 0:  # Check if the result is divisible by 100
            return Length , add
    return None, None  # Return None if no valid addition is found
Length, add = adjust_to_multiple_of_100(Length_min)
print("Lenght of the belt is ", Length)

# 7. Test the belt life according to the number of belt revolutions in 1 second:
i = v1*1000/Length_min
if i <= 5:
    print("i = ", i,"< 5 is satified")
else:
    print("Calculate again with bigger axial distance")
    sys.exit(0)

# 8. Cal Wrap angle (degree)
alpha1 = 180 - 57*((d2-d1)/a)
print("Wrap angle alpha1 = ",alpha1)

# 9. Choose belt thickness delta and check condition
delta = float(input("Choose belt's thickness in table 4.1-[1] delta = "))
#Choose belt's material
while True:
    try:
        # Prompt the user to choose an option
        print("Choose the matetial of belt: ")
        print("1 - Leather")
        print("2 - Rubber")
        Material = int(input("Choose  option: "))
        if (Material ==1):
            print("Choose Leather belt")
            if ( d1/delta >= 20):
                print("Belt's thickness is satified")
                break
            else:
                print("Belt's thickness is not satified, please choose different delta")
                break
        elif (Material ==2):
            if ( d1/delta >= 25):
                print("Belt's thickness is satified")
                break
            else:
                print("Belt's thickness is not satified, please choose different delta")
        else:
            print("Invalid input. Please enter 1 or 2.")
    except ValueError:
        print("Invalid input. Please enter a number.")

# 10. Cal Ci Parameters
C_a = 1 - 0.003*(180 - alpha1)
print("Hugging angle factor C_a = ",C_a)
C_v = 1 - 0.04*(0.01*v1**2 - 1)
print("Velocity factor C_v = ",C_v)
C_o = float(input("Arrangement of drive factor C_o = "))
C_r = float(input("Shock factor C_r = "))
C_all = C_a*C_v*C_o*C_r # Load factor
sigma_t0 = float(input("Choose useful stress in table 4.7, sigma_t0 = "))
sigma_t = sigma_t0*C_all
print("Allowed useful stress sigma_t = ",sigma_t)
# Determmine belt width
b_cal = 1000*Pow/(delta*v1*sigma_t)
def round_up_to_nearest_standard(b_cal, standard_width):
    # Find the smallest value in the standard group that is greater than or equal to the given value
    for standard_value in standard_width:
        if standard_value >= b_cal:
            return standard_value
    return None  # Return None if no suitable value is found
b = round_up_to_nearest_standard(b_cal, standard_width)
print("Choose width of belt follow table 4.1, b = ",b)

# 11. Select the Width of Sheave
def round_up_to_higher_value(b, standard_width):
    # Find the higher value in the standard group next to the given value
    for standard_value in standard_width:
        if standard_value > b:
            return standard_value
    return None  # Return None if no suitable value is found
B_value = round_up_to_higher_value(b, standard_width)
print("Choose width of Sheave follow table 4.5, B = ",B_value)

# 12. Tensile force
Ft = 1000*Pow/v1
print("Tension force Ft = ",Ft)

# 13. Determine force on shaft
sigma_0 = 1.8
F0_max = sigma_0*b*delta
print("Initial Force F0 = ", F0_max)
# Force on shaft
alpha1rad = alpha1/180*math.pi
Fr = math.sin(alpha1rad / 2)*F0_max*3
print("Force on shaft Fr = ", Fr)
density = float(input("Selecting density in page 133-[1], p = "))
sigma0 = F0_max/(b*delta)
sigmaT = Ft/(b*delta)
sigmaV = density*v1**2*10**(-6)
sigma1 = sigma0 + sigmaT/2
sigmaF = delta/d1*100 # Elastic modulus E = 100 MPa

# 14. Maximum Stress
# sig_max = sig0 + 0.5sigT + sigV + sig1
print(" Sigma0 = ", sigma0)
print(" SigmaT = ", sigmaT)
print("Centrifugal stress SigmaV = ", sigmaV)
print("Bending stress SigmaF = ", sigmaF)
sigma_max = sigma1 + sigmaV + sigmaF
print("Maximum Stress sigma_max = ", sigma_max)

# 15. Lifespan
# flatbelt 𝑚=5 , i < [i], [i] = 5
sigmaR = float(input("In page 156, choose sigmaR = "))
Lh = ((sigmaR / sigma_max)**5*10**7)/(2*3600*i)
print("Lifespan Lh = ", Lh)

x = input("Enter to End the program")


