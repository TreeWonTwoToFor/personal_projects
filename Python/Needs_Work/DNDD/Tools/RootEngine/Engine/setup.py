from setuptools import setup
from Cython.Build import cythonize

import os

if not os.path.isfile("Rasterizer.pyx"):
	os.system("cp Rasterizer.py Rasterizer.pyx")
setup(
	ext_modules = cythonize("Rasterizer.pyx")
)
