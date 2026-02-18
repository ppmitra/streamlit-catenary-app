import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

# --- App Title and Description ---
st.title("Catenary Curve Generator")
st.markdown("Adjust the parameters below to calculate and visualize the catenary curve.")

# --- Sidebar Inputs ---
with st.sidebar:
    st.header("Parameters")
    L = st.number_input("Length of Catenary (L)", value=158.98, format="%f")
    d = st.number_input("Horizontal Distance (d)", value=130.76, format="%f")
    yL = st.number_input("Height at Left (yL)", value=62.37, format="%f")
    yR = st.number_input("Height at Right (yR)", value=0.0, format="%f")


def solve_catenary(L, d, yL, yR):
    """Solve for xp, a, y0 that describe the catenary satisfying endpoints.

    Returns (xp, a, y0) or None on failure.
    """
    y_diff = yL - yR
    K = L**2 - y_diff**2

    # Physical feasibility check: chain length must exceed straight-line distance
    if K <= d**2:
        st.error("Error: Length L must be greater than the straight-line distance between endpoints.")
        return None

    # 1. Solve for 'a' using scalar equation
    func_a = lambda a: 2.0 * (a ** 2) * (np.cosh(d / a) - 1.0) - K

    # Safe initial guess for 'a'
    try:
        guess_a = np.sqrt(d ** 4 / (12.0 * (K - d ** 2)))
        if not np.isfinite(guess_a) or guess_a <= 0:
            guess_a = max(1.0, d / 2.0)
    except Exception:
        guess_a = max(1.0, d / 2.0)

    try:
        a_sol = float(fsolve(func_a, guess_a, maxfev=2000)[0])
    except Exception as exc:
        st.error(f"Failed computing parameter 'a': {exc}")
        return None

    if a_sol <= 0 or not np.isfinite(a_sol):
        st.error("Computed non-positive or non-finite 'a'.")
        return None

    # 2. Solve for 'xp' (horizontal shift of the lowest point)
    func_xp = lambda xp: a_sol * np.cosh(xp / a_sol) - a_sol * np.cosh((d - xp) / a_sol) - y_diff
    try:
        xp_sol = float(fsolve(func_xp, d / 2.0, maxfev=2000)[0])
    except Exception as exc:
        st.error(f"Failed computing 'xp': {exc}")
        return None

    # Compute y0 so that y(0) = yL
    y0 = yL - a_sol * np.cosh(xp_sol / a_sol)
    return xp_sol, a_sol, y0


# --- Execution and Plotting ---
params = solve_catenary(L, d, yL, yR)

if params is not None:
    xp, a, y0 = params

    x_vals = np.linspace(0.0, d, 300)
    y_vals = y0 + a * np.cosh((x_vals - xp) / a)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(x_vals, y_vals, color="tab:blue", linewidth=2, label="Catenary")
    ax.plot(0.0, yL, 'ro', label='Point (0, yL)')
    ax.plot(d, yR, 'go', label='Point (d, yR)')
    ax.plot(xp, y0 + a, 'bo', label='Lowest point')
    ax.grid(True)
    ax.set_xlabel('x')
    ax.set_ylabel('y(x)')
    ax.legend()

    st.pyplot(fig)

    col1, col2, col3 = st.columns(3)
    col1.metric("xp", f"{xp:.4f}")
    col2.metric("a", f"{a:.4f}")
    col3.metric("y0", f"{y0:.4f}")
