<!-- markdownlint-disable MD033 MD041 -->

[issues]: https://github.com/cpp-linter/clang-include-cleaner/issues
[contributing]: https://github.com/cpp-linter/clang-include-cleaner/blob/main/CONTRIBUTING.md
[clang-format-wheel]: https://github.com/ssciwr/clang-format-wheel
[clang-tidy-wheel]: https://github.com/ssciwr/clang-tidy-wheel
[clang-apply-replacements-wheel]: https://github.com/cpp-linter/clang-apply-replacements
[license]: https://github.com/cpp-linter/clang-include-cleaner/blob/main/LICENSE.md

[llvm-releases]: https://github.com/llvm/llvm-project/releases
[cpp-linter-hub]: https://cpp-linter.github.io/

# clang-include-cleaner

[![PyPI version](https://img.shields.io/pypi/v/clang-include-cleaner.svg?color=blue)](https://pypi.org/project/clang-include-cleaner/)
[![Platform](https://img.shields.io/badge/platform-linux--64%20%7C%20linux--arm64%20%7C%20win--64%20%7C%20osx--64%20%7C%20osx--arm64-blue)](https://github.com/cpp-linter/clang-include-cleaner)
[![Build](https://github.com/cpp-linter/clang-include-cleaner/actions/workflows/release.yml/badge.svg)](https://github.com/cpp-linter/clang-include-cleaner/actions/workflows/release.yml)
[![PyPI - Downloads](https://img.shields.io/pypi/dw/clang-include-cleaner)](https://pypistats.org/packages/clang-include-cleaner)
[![cpp-linter hub](https://img.shields.io/badge/%F0%9F%8F%A0_cpp--linter_hub-%E2%86%90_home-22863a)](https://cpp-linter.github.io/)

A Python distribution of `clang-include-cleaner` - the LLVM-based tool
that finds **unused `#include` directives** in C++ source files. Install
it with a single `pip install`, no LLVM toolchain required.

---

## Table of Contents

- [Installation](#installation)
- [Related Projects](#related-projects)
- [Contributing](#contributing)
- [License](#license)

## Installation

```bash
pip install clang-include-cleaner
```

The wheel bundles a statically-linked binary and clang builtin
headers - **no LLVM installation is required** on the host machine.

> [!TIP]
> In CI, use `pipx run clang-include-cleaner` — no install needed.
> All [GitHub Actions runners](https://docs.github.com/en/actions)
> ship with `pipx` pre-installed.

Verify:

```bash
clang-include-cleaner --version
```

Run `clang-include-cleaner --help` to see all available options.

For full usage documentation, see the
[upstream docs](https://clang.llvm.org/extra/clang-include-cleaner.html).

## Related Projects

- [**clang-format-wheel**][clang-format-wheel] — pip-installable clang-format binary
- [**clang-tidy-wheel**][clang-tidy-wheel] — pip-installable clang-tidy binary
- [**clang-apply-replacements-wheel**][clang-apply-replacements-wheel] — pip-installable clang-apply-replacements binary

## Contributing

We welcome contributions! See [CONTRIBUTING.md][contributing] for
development setup, build instructions, and the release process.

Please use [GitHub issues][issues] for bug reports and feature requests.

## License

This project is licensed under the Apache License 2.0 with LLVM
exceptions - see [LICENSE.md][license] for details.

The `clang-include-cleaner` binary bundled in the wheels is part of the
[LLVM Project][llvm-releases] and is provided under the same license.


