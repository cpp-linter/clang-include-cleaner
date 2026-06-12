# clang-include-cleaner Python distribution

[![PyPI Release](https://img.shields.io/pypi/v/clang-include-cleaner.svg)](https://pypi.org/project/clang-include-cleaner)

This project packages the `clang-include-cleaner` utility as a Python package. It allows you to install `clang-include-cleaner` directly from PyPI:

```
python -m pip install clang-include-cleaner
```

This project intends to release a new PyPI package for each major and minor release of `clang-include-cleaner`.

## What is clang-include-cleaner?

`clang-include-cleaner` is an LLVM-based tool that analyzes C++ source files and identifies unused `#include` directives that can be safely removed. It is part of the `clang-tools-extra` suite.

## Use with pipx

You can use `pipx` to run clang-include-cleaner, as well. For example, `pipx run clang-include-cleaner <args>` will run clang-include-cleaner without any previous install required on any machine with pipx (including all default GitHub Actions / Azure runners, avoiding requiring a pre-install step or even `actions/setup-python`).

## Building new releases

The [clang-include-cleaner repository](https://github.com/cpp-linter/clang-include-cleaner) provides the logic to build and publish binary wheels of the `clang-include-cleaner` utility.

In order to add a new release, the following steps are necessary:

* Edit the [version file](https://github.com/cpp-linter/clang-include-cleaner/blob/main/clang-include-cleaner_version.txt) to reflect the new version.
* Make a GitHub release to trigger the [GitHub Actions release workflow](https://github.com/cpp-linter/clang-include-cleaner/actions/workflows/release.yml). Alternatively, the workflow can be triggered manually.

On manual triggers, the following input variables are available:
* `use_qemu`: Whether to build targets that require emulation (default: `true`)
* `llvm_version`: Override the LLVM version (default: `""`)
* `wheel_version`: Override the wheel packaging version (default `"0"`)
* `deploy_to_testpypi`: Whether to deploy to TestPyPI instead of PyPI (default: `false`)

The repository with the precommit hook is automatically updated using a scheduled Github Actions workflow.

## Acknowledgments

This repository extends the great work of several other projects:

* `clang-include-cleaner` itself is [provided by the LLVM project](https://github.com/llvm/llvm-project) under the Apache 2.0 License with LLVM exceptions.
* The build logic is based on [scikit-build](https://github.com/scikit-build/scikit-build) which greatly reduces the amount of low level code necessary to package `clang-include-cleaner`.
* The `scikit-build` packaging examples of [CMake](https://github.com/scikit-build/cmake-python-distributions) and [Ninja](https://github.com/scikit-build/ninja-python-distributions) were very helpful in packaging `clang-include-cleaner`.
* The CI build process is controlled by [cibuildwheel](https://github.com/pypa/cibuildwheel) which makes building wheels across a number of platforms a pleasant experience (!)

We are grateful for the generous provisioning with CI resources that GitHub currently offers to Open Source projects.

## Troubleshooting

To see which clang-include-cleaner binary the package is using
you can set `CLANG_INCLUDE_CLEANER_WHEEL_VERBOSE` to `1` in your environment.
