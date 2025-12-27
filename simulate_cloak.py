#!/usr/bin/env python3
"""
Rochester Cloak Simulation using ABCD ray-transfer matrices.

This module provides functions to compute the propagation of a light ray
through the four-lens Rochester Cloak in the paraxial approximation.
"""

import numpy as np

def lens_matrix(f: float) -> np.ndarray:
    """
    Return the ABCD matrix for a thin lens of focal length f (mm).
    
    Parameters
    ----------
    f : float
        Focal length in millimeters. Positive for converging lens.
    
    Returns
    -------
    M : ndarray, shape (2,2)
        Matrix [[1, 0], [-1/f, 1]].
    """
    return np.array([[1.0, 0.0], [-1.0 / f, 1.0]], dtype=float)


def translation_matrix(d: float) -> np.ndarray:
    """
    Return the ABCD matrix for free-space propagation over distance d (mm).
    
    Parameters
    ----------
    d : float
        Propagation distance in millimeters.
    
    Returns
    -------
    M : ndarray, shape (2,2)
        Matrix [[1, d], [0, 1]].
    """
    return np.array([[1.0, d], [0.0, 1.0]], dtype=float)


def system_matrix(f1: float = 200.0, f2: float = 75.0) -> np.ndarray:
    """
    Compute the total ABCD matrix of the symmetric four‑lens Rochester Cloak.
    
    The lens order is: f1, f2, f2, f1.
    Distances are:
        t1 = f1 + f2   (between lenses 1–2 and 3–4),
        t2 = 2*f2*(f1+f2)/(f1-f2)   (between lenses 2–3).
    
    Parameters
    ----------
    f1 : float, optional
        Focal length of the outer lenses (default 200 mm).
    f2 : float, optional
        Focal length of the inner lenses (default 75 mm).
    
    Returns
    -------
    M_total : ndarray, shape (2,2)
        Overall ABCD matrix for the four‑lens system.
    """
    t1 = f1 + f2
    t2 = 2.0 * f2 * (f1 + f2) / (f1 - f2)
    
    # Matrices from left to right (light enters lens 1 first)
    M1 = lens_matrix(f1)                     # lens 1
    M2 = translation_matrix(t1)              # propagate to lens 2
    M3 = lens_matrix(f2)                     # lens 2
    M4 = translation_matrix(t2)              # propagate to lens 3
    M5 = lens_matrix(f2)                     # lens 3
    M6 = translation_matrix(t1)              # propagate to lens 4
    M7 = lens_matrix(f1)                     # lens 4
    
    # Multiply in reverse order because successive matrices act on the right:
    # M_total = M7 @ M6 @ M5 @ M4 @ M3 @ M2 @ M1
    M_total = M7 @ M6 @ M5 @ M4 @ M3 @ M2 @ M1
    return M_total


def propagate_ray(y_in: float, theta_in: float,
                  M: np.ndarray) -> tuple[float, float]:
    """
    Propagate a paraxial ray through an optical system described by ABCD matrix M.
    
    Parameters
    ----------
    y_in : float
        Initial ray height (mm) from the optical axis.
    theta_in : float
        Initial ray angle (rad) relative to the optical axis.
    M : ndarray, shape (2,2)
        ABCD matrix of the optical system.
    
    Returns
    -------
    y_out : float
        Final ray height (mm).
    theta_out : float
        Final ray angle (rad).
    """
    vec_in = np.array([y_in, theta_in], dtype=float)
    vec_out = M @ vec_in
    return vec_out[0], vec_out[1]


def cloak_condition_check(M: np.ndarray, L: float, tol: float = 1e-6) -> bool:
    """
    Verify that the ABCD matrix satisfies the perfect paraxial cloak conditions:
        C = 0 (afocal),  A = 1 (or D = 1),  B = L (for air, n=1).
    
    Parameters
    ----------
    M : ndarray, shape (2,2)
        ABCD matrix [[A, B], [C, D]].
    L : float
        Total physical length of the system (t1 + t2 + t1).
    tol : float, optional
        Numerical tolerance for equality.
    
    Returns
    -------
    bool
        True if the matrix satisfies the cloak conditions within tolerance.
    """
    A, B, C, D = M[0, 0], M[0, 1], M[1, 0], M[1, 1]
    return (abs(C) < tol and
            abs(A - 1.0) < tol and
            abs(B - L) < tol)


def main():
    """Example usage: compute and print the cloak matrix and ray propagation."""
    f1, f2 = 200.0, 75.0
    t1 = f1 + f2
    t2 = 2.0 * f2 * (f1 + f2) / (f1 - f2)
    L_total = 2.0 * t1 + t2
    
    print("Rochester Cloak Simulation")
    print("==========================")
    print(f"Focal lengths: f1 = {f1} mm, f2 = {f2} mm")
    print(f"Separations: t1 = {t1:.1f} mm, t2 = {t2:.1f} mm")
    print(f"Total length: L = {L_total:.1f} mm")
    print()
    
    M = system_matrix(f1, f2)
    print("Total ABCD matrix:")
    print(f"  A = {M[0, 0]:.8f}, B = {M[0, 1]:.8f} mm")
    print(f"  C = {M[1, 0]:.8f}, D = {M[1, 1]:.8f}")
    print()
    
    # Check cloak conditions
    is_cloak = cloak_condition_check(M, L_total)
    print(f"Perfect paraxial cloak conditions satisfied: {is_cloak}")
    print()
    
    # Example ray
    y0 = 10.0   # mm
    th0 = 0.01  # rad
    y1, th1 = propagate_ray(y0, th0, M)
    print(f"Ray entering at y = {y0} mm, θ = {th0} rad")
    print(f"Ray exits at   y = {y1:.3f} mm, θ = {th1:.6f} rad")
    
    # Verify that exit angle equals entrance angle (C = 0)
    print(f"Angle change (θ_out - θ_in) = {th1 - th0:.6f} rad")
    print(f"Lateral shift (y_out - y_in) = {y1 - y0:.3f} mm")


if __name__ == "__main__":
    main()