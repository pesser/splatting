import os, re
if "CONDA_PREFIX" in os.environ:
    # fix compilation in conda env
    if "CUDA_HOME" not in os.environ and os.path.exists(
            os.path.join(os.environ["CONDA_PREFIX"], "bin/nvcc")):
        print("Detected CONDA_PREFIX containing nvcc but no CUDA_HOME, "
              "setting CUDA_HOME=${CONDA_PREFIX}.")
        os.environ["CUDA_HOME"] = os.environ["CONDA_PREFIX"]
    if "CXX" in os.environ and os.environ["CXX"].startswith(os.environ["CONDA_PREFIX"]):
        for FLAG in ["CXXFLAGS", "DEBUG_CXXFLAGS"]:
            if FLAG in os.environ and " -std=" in os.environ[FLAG]:
                print("Detected CONDA compiler with default std flags set. "
                      "Removing them to avoid compilation problems.")
                os.environ[FLAG] = re.sub(r' -std=[^ ]*', '', os.environ[FLAG])

from setuptools import setup
import torch
from torch.utils import cpp_extension
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
