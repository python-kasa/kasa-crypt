"""Build optional cython modules."""

import contextlib
import os
from distutils.command.build_ext import build_ext
from os.path import join
from typing import Any

try:
    from setuptools import Extension
except ImportError:
    from distutils.core import Extension

kasa_crypt_module = Extension(
    "kasa_crypt._crypt_impl",
    [
        join("src", "kasa_crypt", "_crypt_impl.pyx"),
    ],
    language="c",
    extra_compile_args=["-O3", "-g0"],
)


class BuildExt(build_ext):
    def build_extensions(self) -> None:
        with contextlib.suppress(Exception):
            super().build_extensions()


def build(setup_kwargs: dict[Any, Any]) -> None:
    if os.environ.get("SKIP_CYTHON", False):
        return
    try:
        from Cython.Build import cythonize

        setup_kwargs.update(
            dict(
                ext_modules=cythonize(
                    [
                        kasa_crypt_module,
                    ],
                    compiler_directives={"language_level": "3"},  # Python 3
                ),
                cmdclass=dict(build_ext=BuildExt),
            )
        )
        setup_kwargs["exclude_package_data"] = {
            pkg: ["*.c"] for pkg in setup_kwargs["packages"]
        }
    except Exception:
        if os.environ.get("REQUIRE_CYTHON"):
            raise
        pass
