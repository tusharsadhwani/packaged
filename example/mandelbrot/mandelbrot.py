"""
Calculate the Mandelbrot set. Program taken from RealPython:
https://realpython.com/mandelbrot-set-python
"""

import time
import warnings

import matplotlib.pyplot as plt
import numba
import numpy as np

warnings.filterwarnings("ignore")


@numba.njit
def create_mandelbrot(pixel_density, num_iterations):
    xmin, xmax, ymin, ymax = -2, 0.5, -1.5, 1.5
    re = np.linspace(xmin, xmax, int((xmax - xmin) * pixel_density))
    im = np.linspace(ymin, ymax, int((ymax - ymin) * pixel_density))
    c = re[np.newaxis, :] + im[:, np.newaxis] * 1j

    z = np.zeros_like(c)
    for _ in range(num_iterations):
        z = z**2 + c
    return z.real**2 + z.imag**2 <= 2


def main():
    print("Calculating the mandelbrot set...")
    t0 = time.time()
    mandelbrot = create_mandelbrot(pixel_density=2048, num_iterations=20)
    t1 = time.time()
    print(f"Mandelbrot calculed in {t1 - t0:.2f} seconds")

    plt.imshow(mandelbrot, cmap="binary")
    plt.gca().set_aspect("equal")
    plt.axis("off")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
