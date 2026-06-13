<!-- markdownlint-disable MD033 MD041 -->

[discussions]: https://github.com/cpp-linter/clang-include-cleaner/discussions
[issues]: https://github.com/cpp-linter/clang-include-cleaner/issues
[contributing]: https://github.com/cpp-linter/clang-include-cleaner/blob/main/CONTRIBUTING.md
[security]: https://github.com/cpp-linter/clang-include-cleaner/blob/main/SECURITY.md
[license]: https://github.com/cpp-linter/clang-include-cleaner/blob/main/LICENSE.md

[llvm-docs]: https://clang.llvm.org/extra/clang-include-cleaner.html
[llvm-releases]: https://github.com/llvm/llvm-project/releases
[cpp-linter-hub]: https://cpp-linter.github.io/

[iwyu]: https://include-what-you-use.org/
[clangd]: https://clangd.llvm.org/
[compile-commands]: https://clang.llvm.org/docs/JSONCompilationDatabase.html
[pipx-docs]: https://pipx.pypa.io/
[gh-actions-docs]: https://docs.github.com/en/actions

[cpp-linter-action]: https://github.com/cpp-linter/cpp-linter-action
[cpp-linter-hooks]: https://github.com/cpp-linter/cpp-linter-hooks
[clang-tools-pip]: https://github.com/cpp-linter/clang-tools-pip
[scikit-build]: https://github.com/scikit-build/scikit-build
[cibuildwheel]: https://github.com/pypa/cibuildwheel
[ninja-python-distributions]: https://github.com/scikit-build/ninja-python-distributions
[cmake-python-distributions]: https://github.com/scikit-build/cmake-python-distributions

# clang-include-cleaner <sub><sup>| unused #include detection for C++</sup></sub>

[![PyPI version](https://img.shields.io/pypi/v/clang-include-cleaner.svg?color=blue)](https://pypi.org/project/clang-include-cleaner/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/clang-include-cleaner)](https://pypi.org/project/clang-include-cleaner/)
[![Downloads](https://img.shields.io/pypi/dw/clang-include-cleaner)](https://pypistats.org/packages/clang-include-cleaner)
[![Platform](https://img.shields.io/badge/platform-linux--64%20%7C%20linux--arm64%20%7C%20win--64%20%7C%20osx--64%20%7C%20osx--arm64-blue)](https://pypi.org/project/clang-include-cleaner/#files)
[![License](https://img.shields.io/github/license/cpp-linter/clang-include-cleaner?label=license)](https://github.com/cpp-linter/clang-include-cleaner/blob/main/LICENSE.md)
[![Build & Release](https://github.com/cpp-linter/clang-include-cleaner/actions/workflows/release.yml/badge.svg)](https://github.com/cpp-linter/clang-include-cleaner/actions/workflows/release.yml)
[![cpp-linter hub](https://img.shields.io/badge/%F0%9F%8F%A0_cpp--linter_hub-%E2%86%90_home-22863a)](https://cpp-linter.github.io/)

A Python distribution of [`clang-include-cleaner`][llvm-docs] — the
LLVM-based tool that analyzes C++ source files to find unused `#include`
directives. Install it with a single `pip install`, no LLVM toolchain
required.

---

## Table of Contents

- [Why clang-include-cleaner?](#why-clang-include-cleaner)
- [Quick Start](#quick-start)
- [Requirements](#requirements)
- [Installation](#installation)
  - [pip](#pip)
  - [pipx (CI-friendly / zero install)](#pipx-ci-friendly--zero-install)
  - [Verify the install](#verify-the-install)
- [Usage](#usage)
  - [Scan a single file](#scan-a-single-file)
  - [Scan with a compilation database](#scan-with-a-compilation-database)
  - [Integrate into a CI pipeline](#integrate-into-a-ci-pipeline)
- [How It Works](#how-it-works)
- [Platform Support](#platform-support)
- [FAQ](#faq)
- [Troubleshooting](#troubleshooting)
- [Related Projects](#related-projects)
- [Contributing](#contributing)
- [Security](#security)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Why clang-include-cleaner?

C++ codebases accumulate unused `#include` directives over time. They
slow down builds, obscure dependencies, and make refactoring harder.
While several tools exist for cleaning headers,
`clang-include-cleaner` stands out because:

| | clang-include-cleaner | [include-what-you-use][iwyu] |
|---|---|---|
| **Approach** | Finds *removable* includes | Suggests *additions + removals* |
| **Philosophy** | Safe-by-default removals only | Aggressive rewrite (IWYU pragmas) |
| **CLI ergonomics** | Drop-in `pip install` | Requires mapping file, complex setup |
| **Clang versioning** | Ships its own clang, no host conflict | Links against system LLVM |
| **CI readiness** | `pipx run` in one line, zero install | Needs a mapped build environment |

> **Bottom line:** use `clang-include-cleaner` when you want a **safe,
> zero-config tool** to find includes you can delete. Use IWYU when you
> need full header rewriting with custom mapping rules.

## Quick Start

```bash
# install
pip install clang-include-cleaner

# scan a file
clang-include-cleaner src/main.cpp

# check what was found
echo $?   # 0 = clean, non-zero = unused includes detected
```

> **New to the tool?** Read the [official LLVM docs][llvm-docs] for the
> full list of command-line flags.

## Requirements

- **Python** — 3.10 or newer
- **OS** — Linux (glibc ≥ 2.17 or musl), macOS (x86-64 or arm64),
  Windows (x86-64)
- **Compiler database** (optional but recommended) — a
  [`compile_commands.json`][compile-commands] for accurate analysis

## Installation

### pip

```bash
pip install clang-include-cleaner
```

The wheel bundles a statically-linked `clang-include-cleaner` binary and
the clang builtin headers, so **no LLVM installation is required** on the
host.

### pipx (CI-friendly / zero install)

`pipx` lets you run the tool without installing anything permanently —
ideal for CI pipelines and disposable environments:

```bash
pipx run clang-include-cleaner src/main.cpp
```

All [default GitHub Actions / Azure runners][gh-actions-docs] ship with
`pipx`, so this works out of the box without `actions/setup-python`.

### Verify the install

```bash
clang-include-cleaner --version
# clang-include-cleaner 22.1.7  (bundled LLVM 22.1.7)
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

For accurate results — especially in projects with complex include paths
or preprocessor macros — provide a
[`compile_commands.json`][compile-commands]:

```bash
# Generate with CMake
cmake -DCMAKE_EXPORT_COMPILE_COMMANDS=ON -B build .
cmake --build build

# Point clang-include-cleaner at the build directory
clang-include-cleaner -p build src/main.cpp
```

### Integrate into a CI pipeline

#### GitHub Actions (pipx)

```yaml
- name: Check for unused includes
  run: pipx run clang-include-cleaner -p build src/**/*.cpp
```

#### GitHub Actions (pip)

```yaml
- name: Install clang-include-cleaner
  run: pip install clang-include-cleaner

- name: Check for unused includes
  run: clang-include-cleaner -p build src/**/*.cpp
```

Combine with the full [cpp-linter-action][] for a complete
format + tidy + include-clean pipeline.

## How It Works

When you `pip install clang-include-cleaner`, the wheel delivers:

- **A statically-linked native binary** — built from the official LLVM
  source tree for your platform
- **Clang builtin headers** — bundled in the wheel so the tool can
  resolve standard library includes

The Python package acts as a thin wrapper: its entry-point script locates
the bundled binary and forwards all arguments to it. No additional
compilation, no system LLVM, no shared-library dependencies.

## Platform Support

Pre-built wheels are available for:

| Platform | Architecture |
|----------|-------------|
| Linux (manylinux) | x86_64, i686, aarch64, armv7l |
| Linux (musllinux) | x86_64, i686, armv7l |
| macOS | x86_64 (Intel), arm64 (Apple Silicon) |
| Windows | x86-64 (AMD64), x86 |

Source distributions are also published on PyPI for platforms without a
pre-built wheel.

## FAQ

### What’s the difference between clang-include-cleaner and include-what-you-use?

See the [comparison table](#why-clang-include-cleaner) above. In short:
`clang-include-cleaner` tells you what you can **safely delete**; IWYU
tells you what you **should add and remove** (with pragmas). They’re
complementary.

### Does this tool modify my code?

No. `clang-include-cleaner` is a diagnostic tool — it reports findings
but never edits files. Use `--edit` if you want it to automatically
remove the unused includes (supported since LLVM 19).

> ⚠️ Always review auto-removals. Some seemingly-unused includes may be
> required for transitive dependencies or platform-specific builds.

### What LLVM version is bundled?

The bundled LLVM version is encoded in the Python package version. For
`clang-include-cleaner==22.1.7`, the LLVM version is `22.1.7`. Check the
[release tags](https://github.com/cpp-linter/clang-include-cleaner/tags)
for available versions.

### Why not just use `apt install clang-tools-extra`?

- **Version pinning** — `pip install` lets you pin an exact LLVM version
  per project
- **No system-level install** — works in virtual environments and
  containers without `sudo`
- **Cross-platform** — same install command on Linux, macOS, and Windows
- **CI-native** — `pipx run` requires zero setup on GitHub Actions

### Can I use this alongside clang-format and clang-tidy?

Absolutely. The [cpp-linter][] ecosystem provides
[pre-commit hooks][cpp-linter-hooks] and a [GitHub Action][cpp-linter-action]
that run `clang-format`, `clang-tidy`, and `clang-include-cleaner`
together. See the [cpp-linter hub][cpp-linter-hub] for all integrations.

## Troubleshooting

### The binary isn't found

Set `CLANG_INCLUDE_CLEANER_WHEEL_VERBOSE=1` to see which binary the
package is using:

```bash
CLANG_INCLUDE_CLEANER_WHEEL_VERBOSE=1 clang-include-cleaner --version
# Found binary: /path/to/venv/lib/.../data/bin/clang-include-cleaner
```

If no binary is printed, your wheel may be corrupted. Reinstall:

```bash
pip uninstall clang-include-cleaner
pip install --no-cache-dir clang-include-cleaner
```

### "stddef.h not found" or similar header errors

The wheel bundles clang builtin headers, but if you see header-not-found
errors, try running with `--extra-arg=-resource-dir=...` to point
clang-include-cleaner at the bundled headers. In most cases the wrapper
script resolves this automatically; if not, please [open an issue][issues].

### Slow analysis on large projects

Use a `compile_commands.json` to avoid re-parsing headers from scratch,
and consider limiting the scan to recently-changed files in CI:

```bash
git diff --name-only origin/main..HEAD -- '*.cpp' '*.h' \
  | xargs clang-include-cleaner -p build
```

## Related Projects

- [**cpp-linter-action**][cpp-linter-action] — GitHub Action for clang-format + clang-tidy + include cleaning
- [**cpp-linter-hooks**][cpp-linter-hooks] — pre-commit hooks with auto-detect for `compile_commands.json`
- [**clang-tools-pip**][clang-tools-pip] — CLI for installing clang-format, clang-tidy, and clang-query binaries
- [**cpp-linter hub**][cpp-linter-hub] — organization website with docs, guides, and benchmarks

## Contributing

We welcome contributions! See [CONTRIBUTING.md][contributing] for
development setup, build instructions, and release procedures.

Please use [GitHub issues][issues] for bug reports and feature requests,
and [discussions][discussions] for questions and ideas.

## Security

See [SECURITY.md][security] for our security policy and how to report
vulnerabilities.

## License

This project is licensed under the Apache License 2.0 with LLVM
exceptions — see [LICENSE.md][license] for details.

The `clang-include-cleaner` binary bundled in the wheels is part of the
LLVM Project and is provided under the same license.

## Acknowledgments

This project extends the great work of several other projects:

- [`clang-include-cleaner`][llvm-docs] itself is part of the
  [LLVM Project][llvm-releases], provided under the Apache 2.0 License
  with LLVM exceptions.
- The build logic is based on [scikit-build][] which greatly reduces the
  amount of low-level code necessary to package the utility.
- The packaging examples of [CMake][cmake-python-distributions] and
  [Ninja][ninja-python-distributions] by scikit-build were very helpful
  in setting up this project.
- The CI build matrix is powered by [cibuildwheel][], making
  cross-platform wheel builds a pleasant experience.
- GitHub's generous CI resources for open-source projects make this
  multi-platform release pipeline possible.
