from setuptools import setup
from torch.utils import cpp_extension
import os
import glob


ext_modules = [
    cpp_extension.CppExtension(
        "splatting.cpu",
        ["cpp/splatting.cpp"],
    ),
]


ext_modules.append(
    cpp_extension.CUDAExtension(
        "splatting.cuda",
        ["cuda/splatting_cuda.cpp", "cuda/splatting.cu"],
        extra_compile_args={"nvcc": ["-gencode=arch=compute_61,code=sm_61",
                                     "-gencode=arch=compute_80,code=sm_80"]},
    ),
)


setup(
    name="splatting",
    ext_modules=ext_modules,
    cmdclass={"build_ext": cpp_extension.BuildExtension},
    install_requires=["torch"],
    extras_require={
        "dev": ["pytest", "pytest-cov", "pre-commit"]
    },  # pip install -e '.[dev]'
)
