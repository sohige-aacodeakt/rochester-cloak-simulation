# Rochester Cloak Simulation

An open-source simulation of the Rochester Cloak using optical ray tracing in the paraxial approximation. This project provides a Python implementation of the four-lens cloaking system based on ABCD matrix formalism, enabling visualization of light ray paths around a cloaked region.

## Background

The Rochester Cloak is a paraxial invisibility device developed at the University of Rochester that uses four standard lenses to bend light around an object, making it invisible across a continuous range of viewing angles. The design relies on symmetric lens pairs and specific separations that satisfy the conditions for a "perfect" paraxial cloak (C = 0, B = L/n, A = 1 in the ABCD matrix).

## Mathematical Model

The simulation uses ray‑transfer matrices (ABCD matrices) for thin lenses and free‑space propagation:

- **Lens matrix** (focal length \(f\)):
  \[
  M_{\text{lens}} = \begin{bmatrix}1 & 0 \\ -\frac{1}{f} & 1\end{bmatrix}
  \]

- **Translation matrix** (distance \(d\)):
  \[
  M_{\text{trans}} = \begin{bmatrix}1 & d \\ 0 & 1\end{bmatrix}
  \]

For the four‑lens Rochester Cloak the optical system is:

\[
M_{\text{total}} = M_{\text{lens}}(f_4) \; M_{\text{trans}}(t_1) \; M_{\text{lens}}(f_3) \; M_{\text{trans}}(t_2) \; M_{\text{lens}}(f_2) \; M_{\text{trans}}(t_1) \; M_{\text{lens}}(f_1)
\]

with the symmetric configuration:
- \(f_1 = f_4\) (outer lenses),
- \(f_2 = f_3\) (inner lenses),
- \(t_1 = f_1 + f_2\),
- \(t_2 = \dfrac{2 f_2 (f_1 + f_2)}{f_1 - f_2}\).

The default parameters used in the simulation are:
- \(f_1 = 200\,\text{mm}\),
- \(f_2 = 75\,\text{mm}\),
- \(t_1 = 275\,\text{mm}\),
- \(t_2 \approx 330\,\text{mm}\).

A ray described by a column vector \(\begin{bmatrix} y \\ \theta \end{bmatrix}\) (height \(y\), angle \(\theta\)) propagates through the system via:
\[
\begin{bmatrix} y_{\text{out}} \\ \theta_{\text{out}} \end{bmatrix} = M_{\text{total}} \begin{bmatrix} y_{\text{in}} \\ \theta_{\text{in}} \end{bmatrix}.
\]

For a perfect paraxial cloak the matrix satisfies \(C = 0\) (afocal) and \(A = 1\), meaning the exit angle equals the entrance angle while the ray is laterally shifted.

## Installation & Dependencies

The simulation requires Python 3.7+ and the following packages:
- `numpy` – matrix operations
- `matplotlib` – ray visualization

Install the dependencies with pip:

```bash
pip install numpy matplotlib
```

## Usage

### Core Simulation

The main simulation function is provided in `simulate_cloak.py`. It can be used as a module or run directly to compute ray propagation.

```python
from simulate_cloak import propagate_ray, system_matrix

# Compute the ABCD matrix for the default cloak
M = system_matrix(f1=200.0, f2=75.0)

# Propagate a ray entering at height 10 mm with angle 0.01 rad
y_in = 10.0    # mm
theta_in = 0.01  # rad
y_out, theta_out = propagate_ray(y_in, theta_in, M)

print(f"Output height: {y_out:.3f} mm, output angle: {theta_out:.6f} rad")
```

### Visualization

The script `visualize_rays.py` produces a plot of multiple rays passing through the cloak, clearly showing the region where an object can be hidden.

Run the visualization directly:

```bash
python visualize_rays.py
```

This generates a figure `ray_paths.png` illustrating the ray trajectories and the cloaked “doughnut” zone.

## Project Structure

- `simulate_cloak.py` – Core ABCD‑matrix simulation of the four‑lens system.
- `visualize_rays.py` – Visualizes ray paths through the cloak.
- `README.md` – This documentation.
- `LICENSE` – MIT License (optional).

## Development Workflow

This repository follows a standard GitHub workflow:
1. **Issues** track feature requests and bug reports.
2. **Branches** are used for developing new features.
3. **Pull requests** merge changes after review.
4. **Releases** tag stable versions of the simulation.

## Releases

The first stable version of the simulation is tagged as [v1.0.0](https://github.com/sohige-aacodeakt/rochester-cloak-simulation/releases/tag/v1.0.0). This release includes:

- Core ABCD‑matrix simulation (`simulate_cloak.py`)
- Ray‑trajectory visualization (`visualize_rays.py`)
- Complete documentation (`README.md`)
- MIT License (`LICENSE`)

All release assets (source code and pre‑generated ray‑path plot) can be downloaded from the [releases page](https://github.com/sohige-aacodeakt/rochester-cloak-simulation/releases).

## References

1. J. S. Choi and J. C. Howell, “Paraxial ray optics cloaking,” *Optics Express* **22**, 29465‑29478 (2014).
2. University of Rochester News Center, “Invisibility cloaking device hides objects across range of angles” (2014).
3. NBC News, “Scientists show you how to make an invisibility cloak (sort of)” (2014).

## License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.