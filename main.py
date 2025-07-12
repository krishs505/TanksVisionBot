import math
from PIL import Image
from PIL import ImageGrab
import numpy as np

grabFromClipboard = True

# grab image from clipboard
if grabFromClipboard:
    img = ImageGrab.grabclipboard()

    if img is not None:
        img.save("clipboard_image.png")
        print("Image saved!")
    else:
        print("No image found in clipboard.")
        exit()

    # resize image to preferred size
    img = img.resize((495, 1077), Image.LANCZOS)
    img.save('resized_image.png')
else:
    img = Image.open('resized_image.png')

# conver to numpy array to analyze pixel data
img_np = np.array(img)

# calculate wind magnitude based on pixels
wind = 2
for c in img_np[121, 174:320]:
    if c[2] > 160:
        wind += 1

# determine if wind is reversed
if img_np[121, 245][2] > 160:
    wind = wind * -1

print('wind:', wind)

# scan specific region until red and green values are within player tank color range
foundRed = False
for r in range(700, 810):
    for c in range(0, 202):
        if img_np[r, c][1] > 40 and int(img_np[r, c][0]) - int(img_np[r, c][1]) > 10:
            xi = c + 10
            yi = r - 25
            print('red:', c, ',', r)
            print('red:', xi, ',', yi)
            foundRed = True
            break
    if foundRed:
        break

# scan specific region until blue values are within enemy tank color range
foundBlue = False
for r in range(883, 878, -1):
    for c in range(316, 494):
        if img_np[r, c][2] >= 200:
            xf = c + 13
            yf = r - 8
            print('blue:', xf, ',', yf)
            foundBlue = True
            break
    if foundBlue:
        break

# constants (determined by data analysis)
g = 0.2987
W = 0.007817097926 * wind

real_dy = yi - yf
print(real_dy)

difference = 1000
best_angle = 0
best_power = 0

# loop through power levels 60-81
for i in range(21):
    power = i + 60

    # estimated initial velocity in pixels/s based on data analysis
    vi = power * 0.139863 + 3.05155 

    # (for each power) loop through 31 different angles for best possible settings
    for k in range(31):
        print('---')

        theta = k + 55
        print(theta)

        # perform trigonometric calculations for theta and velocity components
        theta = math.radians(theta)
        vx = vi * math.cos(theta) + W
        vy = vi * math.sin(theta)
  
        dx = xf - xi

        # use kinematic equation to predict delta y AT same delta x of enemy tank
        dy = vy * dx / vx - 0.5 * g * math.pow(dx / vx, 2)

        # use kinematic equation to check if tower was hit from the left
        towerFirstCheck = yi - (vy * (197 - xi) / vx - 0.5 * g * math.pow((197 - xi) / vx, 2))
      
        if towerFirstCheck > yi - 132:
            print('--- will hit tower ---')
        else:
            # use kinematic equation to check if tower was hit from the right
            towerSecondCheck = yi - (vy * (295 - xi) / vx - 0.5 * g * math.pow((295 - xi) / vx, 2))
            print(towerSecondCheck)
            if towerSecondCheck > yi - 132:
                print('--- will hit tower pt 2 ---')
            else:
                print(dy)

                # is this the closest delta y to the actual target? if so, set it to the new best settings
                if abs(dy - real_dy) < difference:
                    difference = abs(dy - real_dy)
                    best_angle = theta
                    best_power = power

print('-----')
# print optimal angle and power with pixel difference
print('optimal angle = ' + str(math.degrees(best_angle)) + ' at power ' + str(best_power) + ', with difference of ' + str(difference))
