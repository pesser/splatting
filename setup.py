from setuptools import setup
import torch
from torch.utils import cpp_extension
import os
import glob

ext_modules = [
    cpp_extension.CppExtension(
        "splatting.cpu",
        ["cpp/splatting.cpp"],
    ),
]

if torch.cuda.is_available():
    ext_modules.append(
        cpp_extension.CUDAExtension(
            "splatting.cuda",
            ["cuda/splatting_cuda.cpp", "cuda/splatting.cu"],
        ),
    )

setup(
    name="splatting",
    ext_modules=ext_modules,
    cmdclass={"build_ext": cpp_extension.BuildExtension},
    packages=["splatting"],
    install_requires=["torch"],
    extras_require={
        "dev": ["pytest", "pytest-cov", "pre-commit"]
    },
)
