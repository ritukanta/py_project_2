#! /usr/local/bin python
import numpy as np  # for numerical stability
import matplotlib.pyplot as plt  # for plotting the actual model
from scipy.integrate import solve_ivp  # to solve the order 2 ODE

# Parameters
m = 80
g = 9.8
k = 50
L = 30
h = 100

# Initials
y0 = h
v0 = 0
t_span = (0, 30)  # Simulate for 30 seconds
t_eval = np.linspace(t_span[0], t_span[1], 1000)  # Time points for evaluation

# Define the system of ODEs


def bungee_jump(t, state):
    y, v = state  # Unpack state variables (position and velocity)

    # Check if the cord is slack or stretched
    if y > L:
        # Cord is stretched: spring force acts
        a = g - (k / m) * (y - L)
    else:
        # Cord is slack: only gravity acts
        a = g

    return [v, a]  # Return [dy/dt, dv/dt]


# Solve the ODE
sol = solve_ivp(bungee_jump, t_span, [y0, v0], t_eval=t_eval)

# Extract results
y = sol.y[0]
v = sol.y[1]
t = sol.t

# Calculate forces
F_gravity = m * g
F_spring = np.where(y > L, k * (y - L), 0)

# Plot results
plt.figure(figsize=(12, 8))

# Position vs Time
plt.subplot(3, 1, 1)
plt.plot(t, y, label="Position (m)")
plt.axhline(L, color="r", linestyle="--", label="Unstretched Cord Length")
plt.xlabel("Time (s)")
plt.ylabel("Position (m)")
plt.title("Bungee Jumping: Position vs Time")
plt.legend()
plt.grid()

# Velocity vs Time
plt.subplot(3, 1, 2)
plt.plot(t, v, label="Velocity (m/s)", color="orange")
plt.xlabel("Time (s)")
plt.ylabel("Velocity (m/s)")
plt.title("Bungee Jumping: Velocity vs Time")
plt.legend()
plt.grid()

# Forces vs Time
plt.subplot(3, 1, 3)
plt.plot(t, F_gravity * np.ones_like(t), label="Gravity (N)", color="green")
plt.plot(t, F_spring, label="Spring Force (N)", color="purple")
plt.xlabel("Time (s)")
plt.ylabel("Force (N)")
plt.title("Bungee Jumping: Forces vs Time")
plt.legend()
plt.grid()

plt.tight_layout()
plt.show()
