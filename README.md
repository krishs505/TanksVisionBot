# Tanks Vision Bot

**Tanks Vision Bot** analyzes the GamePigeon Tanks game, detects target positions and wind conditions, and calculates the optimal firing angle and power to hit the enemy tank using kinematics-based projectile motion.

---

## How It Works

- Resizes and processes clipboard image using **Pillow** and **NumPy**
- Determines:
  - **Wind direction and strength** based on blue pixel intensity
  - **Red and blue tank positions** based on pixel intensities
- Runs a **few hundred physics-based simulations** based on experimentally determined gravity and wind constants
- Predicts the **optimal launch angle and power** using trigonometry and kinematic equations to minimize trajectory error
- Checks for possible tower collisions before finalizing a result

<img width="230" height="500" alt="resized_image" src="https://github.com/user-attachments/assets/ba7e7b3d-8f0a-42dd-8313-46e1349f0506" />

---

## How to Use
1. **Install main.py and the required Python libraries using pip.**

2. **Copy an image of your GamePigeon Tanks game to your clipboard.**

3. **Run the script:**

```bash
python main.py
```

4. **The script will print the best angle and power combination.**

---
