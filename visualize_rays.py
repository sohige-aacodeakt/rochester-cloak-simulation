#!/usr/bin/env python3
"""
Visualization of ray paths through the Rochester Cloak.

This script uses the simulation functions from simulate_cloak.py to trace
multiple rays through the four-lens system and plots their trajectories,
clearly showing the cloaked region where objects can be hidden.
"""

import numpy as np
import matplotlib.pyplot as plt
from simulate_cloak import lens_matrix, translation_matrix, system_matrix


def trace_ray(y0: float, theta0: float, f1: float = 200.0, f2: float = 75.0):
    """
    Trace a paraxial ray step-by-step through the four-lens cloak.
    
    Returns arrays of x (axial position) and y (height) coordinates that can
    be used for plotting.
    
    Parameters
    ----------
    y0 : float
        Initial height (mm) at the entrance of the first lens.
    theta0 : float
        Initial angle (rad) at the entrance.
    f1, f2 : float, optional
        Focal lengths (default 200 mm, 75 mm).
    
    Returns
    -------
    x_pts : ndarray, shape (N,)
        Axial positions (mm) along the optical axis.
    y_pts : ndarray, shape (N,)
        Ray heights (mm) at those positions.
    """
    # Lens separations
    t1 = f1 + f2
    t2 = 2.0 * f2 * (f1 + f2) / (f1 - f2)
    L_total = 2.0 * t1 + t2
    
    # Positions of the four lenses (thin lenses assumed at these x coordinates)
    x_lens1 = 0.0
    x_lens2 = t1
    x_lens3 = t1 + t2
    x_lens4 = L_total
    
    # We will store (x, y) points after each optical element
    x_pts = []
    y_pts = []
    
    # Start just before the first lens
    x = x_lens1
    y = y0
    theta = theta0
    x_pts.append(x)
    y_pts.append(y)
    
    # Lens 1
    M_lens1 = lens_matrix(f1)
    vec = np.array([y, theta])
    vec = M_lens1 @ vec
    y, theta = vec[0], vec[1]
    x_pts.append(x)   # lens is infinitely thin, same x
    y_pts.append(y)
    
    # Propagation to lens 2
    x = x_lens2
    y = y + theta * t1   # linear propagation in paraxial approximation
    x_pts.append(x)
    y_pts.append(y)
    
    # Lens 2
    M_lens2 = lens_matrix(f2)
    vec = np.array([y, theta])
    vec = M_lens2 @ vec
    y, theta = vec[0], vec[1]
    x_pts.append(x)
    y_pts.append(y)
    
    # Propagation to lens 3
    x = x_lens3
    y = y + theta * t2
    x_pts.append(x)
    y_pts.append(y)
    
    # Lens 3
    M_lens3 = lens_matrix(f2)
    vec = np.array([y, theta])
    vec = M_lens3 @ vec
    y, theta = vec[0], vec[1]
    x_pts.append(x)
    y_pts.append(y)
    
    # Propagation to lens 4
    x = x_lens4
    y = y + theta * t1
    x_pts.append(x)
    y_pts.append(y)
    
    # Lens 4
    M_lens4 = lens_matrix(f1)
    vec = np.array([y, theta])
    vec = M_lens4 @ vec
    y, theta = vec[0], vec[1]
    x_pts.append(x)
    y_pts.append(y)
    
    # A short propagation after the last lens to see the exit direction
    x_end = x + 50.0   # extra 50 mm
    y_end = y + theta * 50.0
    x_pts.append(x_end)
    y_pts.append(y_end)
    
    return np.array(x_pts), np.array(y_pts)


def plot_rays(f1=200.0, f2=75.0, save_path='ray_paths.png'):
    """
    Generate a figure showing multiple ray trajectories through the cloak.
    
    Parameters
    ----------
    f1, f2 : float
        Focal lengths of the outer and inner lenses.
    save_path : str
        File name for the saved figure.
    """
    t1 = f1 + f2
    t2 = 2.0 * f2 * (f1 + f2) / (f1 - f2)
    L_total = 2.0 * t1 + t2
    
    # Lens positions
    lens_x = [0.0, t1, t1 + t2, L_total]
    lens_labels = ['L1 (f1)', 'L2 (f2)', 'L3 (f2)', 'L4 (f1)']
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Draw lenses as vertical lines
    for x, label in zip(lens_x, lens_labels):
        ax.axvline(x, color='black', linestyle='--', linewidth=1, alpha=0.7)
        ax.text(x, ax.get_ylim()[1] * 0.95, label,
                horizontalalignment='center', fontsize=9, backgroundcolor='white')
    
    # Draw the cloaked region (approximate doughnut shape)
    # The cloaked volume lies between the inner lenses (L2 and L3) and
    # is bounded by rays that would hit the optical axis.
    # We shade a rectangle between x = t1 and x = t1 + t2, y from -r to +r.
    r_cloak = 15.0   # approximate radius of the cloaked region (mm)
    ax.axvspan(t1, t1 + t2, facecolor='lightgray', alpha=0.3,
               label='Cloaked region (approx.)')
    
    # Trace several rays with different entrance heights
    entrance_heights = np.linspace(-20.0, 20.0, 9)   # mm
    angles = [0.0, 0.005, -0.005]   # rad
    
    colors = plt.cm.viridis(np.linspace(0.2, 0.8, len(entrance_heights)))
    for y0, color in zip(entrance_heights, colors):
        for theta0 in angles:
            x_pts, y_pts = trace_ray(y0, theta0, f1, f2)
            ax.plot(x_pts, y_pts, color=color, linewidth=1.5, alpha=0.8)
    
    # Decorate the plot
    ax.set_xlabel('Axial position (mm)', fontsize=12)
    ax.set_ylabel('Height (mm)', fontsize=12)
    ax.set_title('Ray trajectories through the Rochester Cloak', fontsize=14)
    ax.grid(True, linestyle=':', alpha=0.5)
    ax.axhline(0, color='k', linewidth=0.5)   # optical axis
    ax.legend(loc='upper right')
    ax.set_xlim(-10, L_total + 60)
    ax.set_ylim(-30, 30)
    
    # Add text box with parameters
    param_text = (f'$f_1 = {f1:.0f}$ mm, $f_2 = {f2:.0f}$ mm\n'
                  f'$t_1 = {t1:.0f}$ mm, $t_2 = {t2:.0f}$ mm\n'
                  f'$L = {L_total:.0f}$ mm')
    ax.text(0.02, 0.02, param_text, transform=ax.transAxes,
            fontsize=9, verticalalignment='bottom',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    print(f"Figure saved as '{save_path}'")
    plt.show()


def main():
    """Run the visualization and optionally display the total ABCD matrix."""
    f1, f2 = 200.0, 75.0
    print("Rochester Cloak Ray Visualization")
    print("=================================")
    print(f"Using f1 = {f1} mm, f2 = {f2} mm")
    
    M = system_matrix(f1, f2)
    print("\nTotal ABCD matrix:")
    print(f"  A = {M[0, 0]:.6f}, B = {M[0, 1]:.6f}")
    print(f"  C = {M[1, 0]:.6f}, D = {M[1, 1]:.6f}")
    
    plot_rays(f1, f2)


if __name__ == "__main__":
    main()