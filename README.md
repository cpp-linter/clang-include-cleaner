<!-- markdownlint-disable MD033 MD041 -->

[issues]: https://github.com/cpp-linter/clang-include-cleaner/issues
[contributing]: https://github.com/cpp-linter/clang-include-cleaner/blob/main/CONTRIBUTING.md
[clang-format-wheel]: https://github.com/ssciwr/clang-format-wheel
[clang-tidy-wheel]: https://github.com/ssciwr/clang-tidy-wheel
[clang-apply-replacements-wheel]: https://github.com/cpp-linter/clang-apply-replacements-wheel
[license]: https://github.com/cpp-linter/clang-include-cleaner/blob/main/LICENSE.md

[llvm-releases]: https://github.com/llvm/llvm-project/releases
[clang-tools-extra]: https://clang.llvm.org/extra/index.html
[cpp-linter-hub]: https://cpp-linter.github.io/

[iwyu]: https://include-what-you-use.org/
[compile-commands]: https://clang.llvm.org/docs/JSONCompilationDatabase.html

[cpp-linter-action]: https://github.com/cpp-linter/cpp-linter-action
[cpp-linter-hooks]: https://github.com/cpp-linter/cpp-linter-hooks
[clang-tools-pip]: https://github.com/cpp-linter/clang-tools-pip
[scikit-build]: https://github.com/scikit-build/scikit-build
[cibuildwheel]: https://github.com/pypa/cibuildwheel
[ninja-python-distributions]: https://github.com/scikit-build/ninja-python-distributions
[cmake-python-distributions]: https://github.com/scikit-build/cmake-python-distributions

# clang-include-cleaner

[![PyPI version](https://img.shields.io/pypi/v/clang-include-cleaner.svg?color=blue)](https://pypi.org/project/clang-include-cleaner/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/clang-include-cleaner)](https://pypi.org/project/clang-include-cleaner/)
[![PyPI - Downloads](https://img.shields.io/pypi/dw/clang-include-cleaner)](https://pypistats.org/packages/clang-include-cleaner)
[![Platform](https://img.shields.io/badge/platform-linux--64%20%7C%20linux--arm64%20%7C%20win--64%20%7C%20osx--64%20%7C%20osx--arm64-blue)](https://github.com/cpp-linter/clang-include-cleaner)
[![Build](https://github.com/cpp-linter/clang-include-cleaner/actions/workflows/release.yml/badge.svg)](https://github.com/cpp-linter/clang-include-cleaner/actions/workflows/release.yml)
[![cpp-linter hub](https://img.shields.io/badge/%F0%9F%8F%A0_cpp--linter_hub-%E2%86%90_home-22863a)](https://cpp-linter.github.io/)

A Python distribution of `clang-include-cleaner` - the LLVM-based tool
that finds **unused `#include` directives** in C++ source files. Install
it with a single `pip install`, no LLVM toolchain required.

> [!TIP]
> Looking for a complete C++ linting solution? Check out
> [**cpp-linter-action**][cpp-linter-action] (GitHub Action) and
> [**cpp-linter-hooks**][cpp-linter-hooks] (pre-commit hooks) -
> they run `clang-format`, `clang-tidy`, and clang-include-cleaner
> together.

---

## Table of Contents

- [Why clang-include-cleaner?](#why-clang-include-cleaner)
- [Quick Start](#quick-start)
- [Requirements](#requirements)
- [Installation](#installation)
  - [pip](#pip)
  - [pipx (CI-friendly)](#pipx-ci-friendly)
  - [Verify the install](#verify-the-install)
- [Usage](#usage)
  - [Scan a single file](#scan-a-single-file)
  - [Scan with a compilation database](#scan-with-a-compilation-database)
  - [Integrate into a CI pipeline](#integrate-into-a-ci-pipeline)
- [How It Works](#how-it-works)
- [Platform Support](#platform-support)
- [FAQ](#faq)
- [Related Projects](#related-projects)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Why clang-include-cleaner?

C++ codebases accumulate unused `#include` directives over time. They
slow down builds, obscure real dependencies, and make refactoring
riskier. `clang-include-cleaner` finds includes you can **safely
delete**.

| | clang-include-cleaner | [include-what-you-use][iwyu] |
|---|---|---|
| **Approach** | Find *removable* includes | Suggest *additions + removals* |
| **Philosophy** | Safe removals, no pragmas needed | Full rewrite with IWYU pragmas |
| **Setup** | `pip install` (bundles its own clang) | Mapping file + system LLVM |
| **CI readiness** | `pipx run` in one line | Needs a mapped build environment |
| **Output** | Warnings on unused `#include` lines | Add/remove recommendations per file |

> [!NOTE]
> Use `clang-include-cleaner` when you want a **safe, zero-config tool**
> to find dead includes. Use IWYU when you need comprehensive header
> rewriting with custom mapping rules. The two tools are complementary.

## Quick Start

```bash
# install
pip install clang-include-cleaner

# scan a file
clang-include-cleaner src/main.cpp

# check what was found
echo $?   # 0 = clean, non-zero = unused includes detected
```

> [!NOTE]
> New to the tool? See the [clang-tools-extra documentation][clang-tools-extra]
> for an overview of all available tools in the suite.

## Requirements

| Requirement | Details |
|-------------|---------|
| **Python** | 3.10 or newer |
| **OS** | Linux (glibc ≥ 2.17 or musl), macOS, Windows |
| **Architecture** | x86-64, arm64, i686, armv7l |
| **Compile database** (optional) | [`compile_commands.json`][compile-commands] for accurate analysis |

## Installation

### pip

```bash
pip install clang-include-cleaner
```

The wheel bundles a statically-linked binary and clang builtin
headers - **no LLVM installation is required** on the host machine.

### pipx (CI-friendly)

`pipx` runs the tool without installing anything permanently - ideal for
CI pipelines and disposable environments:

```bash
pipx run clang-include-cleaner src/main.cpp
```

All [default GitHub Actions runners](https://docs.github.com/en/actions)
ship with `pipx`, so this works without `actions/setup-python`.

### Verify the install

```bash
clang-include-cleaner --version
```

## Usage

### Scan a single file

```bash
clang-include-cleaner src/main.cpp
```

Example output:

```
src/main.cpp:3:1: warning: included header iostream is not used directly [include-cleaner]
#include <iostream>
^~~~~~~~~~~~~~~~~~
```

### Scan with a compilation database

For projects with complex include paths, provide a
[`compile_commands.json`][compile-commands]:

```bash
# Generate with CMake
cmake -DCMAKE_EXPORT_COMPILE_COMMANDS=ON -B build .
cmake --build build

# Point clang-include-cleaner at the build directory
clang-include-cleaner -p build src/main.cpp
```

### Integrate into a CI pipeline

#### GitHub Actions with pipx (zero install)

```yaml
- name: Check for unused includes
  run: pipx run clang-include-cleaner -p build src/**/*.cpp
```

#### GitHub Actions with pip

```yaml
- name: Install clang-include-cleaner
  run: pip install clang-include-cleaner

- name: Check for unused includes
  run: clang-include-cleaner -p build src/**/*.cpp
```

Combine with [cpp-linter-action][] for a complete format + tidy +
include-clean pipeline.

## How It Works

When you `pip install clang-include-cleaner`, the wheel delivers:

- **A statically-linked native binary** - built from the official
  [LLVM source tree][llvm-releases] for your platform
- **Clang builtin headers** - bundled so the tool can resolve standard
  library includes

The Python package acts as a thin wrapper: its entry-point locates the
bundled binary and forwards all arguments to it. No system LLVM, no
shared-library dependencies, no additional compilation.

## Platform Support

Pre-built wheels are available for:

| Platform | Architectures |
|----------|--------------|
| Linux (manylinux) | x86_64, i686, aarch64, armv7l |
| Linux (musllinux) | x86_64, i686, armv7l |
| macOS | x86_64 (Intel), arm64 (Apple Silicon) |
| Windows | AMD64, x86 |

Source distributions are also published on PyPI for platforms without a
pre-built wheel.

## FAQ

### What's the difference between clang-include-cleaner and include-what-you-use?

See the [comparison table](#why-clang-include-cleaner) above. In short:
`clang-include-cleaner` tells you what you can **safely delete**; IWYU
tells you what to **add and remove**. They're complementary - many teams
use both.

### Does this tool modify my code?

No. `clang-include-cleaner` is a diagnostic tool - it reports findings
but does not edit files. You decide which includes to remove.

> [!IMPORTANT]
> Always review findings manually. An include that appears unused may
> still be required for transitive dependencies or platform-specific
> builds.

### What LLVM version is bundled?

The bundled LLVM version is encoded in the Python package version.
For `clang-include-cleaner==22.1.7`, the LLVM version is `22.1.7`.
Check the [release tags](https://github.com/cpp-linter/clang-include-cleaner/tags)
for all available versions.

### Why not just `apt install clang-tools-extra`?

- **Version pinning** - `pip install` pins an exact LLVM version per project
- **No system deps** - works in virtual environments and containers without `sudo`
- **Cross-platform** - same command on Linux, macOS, and Windows
- **CI-native** - `pipx run` requires zero setup on GitHub Actions runners

### Can I use this alongside clang-format and clang-tidy?

Absolutely. The [cpp-linter hub][cpp-linter-hub] provides
[pre-commit hooks][cpp-linter-hooks] and a [GitHub Action][cpp-linter-action]
that run `clang-format`, `clang-tidy`, and `clang-include-cleaner`
together as a unified pipeline.

## Related Projects

- [**clang-format-wheel**][clang-format-wheel] — pip-installable clang-format binary
- [**clang-tidy-wheel**][clang-tidy-wheel] — pip-installable clang-tidy binary
- [**clang-apply-replacements-wheel**][clang-apply-replacements-wheel] — pip-installable clang-apply-replacements binary
- [**cpp-linter-action**][cpp-linter-action] — GitHub Action for clang-format + clang-tidy + include cleaning
- [**cpp-linter-hooks**][cpp-linter-hooks] — pre-commit hooks with auto-detect for `compile_commands.json`
- [**clang-tools-pip**][clang-tools-pip] — CLI for installing clang-format, clang-tidy, and clang-query binaries
- [**cpp-linter hub**][cpp-linter-hub] — organization website with docs, guides, and benchmarks

## Contributing

We welcome contributions! See [CONTRIBUTING.md][contributing] for
development setup, build instructions, and the release process.

Please use [GitHub issues][issues] for bug reports and feature requests.

## License

This project is licensed under the Apache License 2.0 with LLVM
exceptions - see [LICENSE.md][license] for details.

The `clang-include-cleaner` binary bundled in the wheels is part of the
[LLVM Project][llvm-releases] and is provided under the same license.

## Acknowledgments

This project extends the great work of several other projects:

- [`clang-include-cleaner`][clang-tools-extra] itself is part of the
  [LLVM Project][llvm-releases], provided under the Apache 2.0 License
  with LLVM exceptions.
- The build logic is based on [scikit-build][] which greatly reduces the
  amount of low-level code necessary to package the utility.
- The packaging examples of [CMake][cmake-python-distributions] and
  [Ninja][ninja-python-distributions] by scikit-build were helpful
  in setting up this project.
- The CI build matrix is powered by [cibuildwheel][], making
  cross-platform wheel builds a pleasant experience.
- GitHub's generous CI resources for open-source projects make this
  multi-platform release pipeline possible.
