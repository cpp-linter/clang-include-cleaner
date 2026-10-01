# clang-include-cleaner

[![PyPI](https://img.shields.io/pypi/v/clang-include-cleaner?labelColor=454a63&color=007ec6)](https://pypi.org/project/clang-include-cleaner/)
[![part of cpp-linter](https://img.shields.io/badge/part%20of-cpp--linter-ffc20a?labelColor=454a63)](https://cpp-linter.github.io/)

A Python wheel of `clang-include-cleaner`, the LLVM-based tool that finds unused and missing
`#include` directives in C++ source files.

[Website](https://cpp-linter.github.io/) · [Get started](https://cpp-linter.github.io/getting-started/#just-the-clang-tools) · [Discussions](https://github.com/orgs/cpp-linter/discussions)

## Quick start

```bash
pip install clang-include-cleaner
```

The wheel bundles the `clang-include-cleaner` binary and the clang builtin headers; no LLVM
installation is required on the host machine.

> [!TIP]
> In CI, use `pipx run clang-include-cleaner` — no install needed.
> [GitHub-hosted runners](https://github.com/actions/runner-images)
> ship with `pipx` pre-installed.

Verify:

```bash
clang-include-cleaner --version
```

## Usage

`clang-include-cleaner` reads the compile commands from a `compile_commands.json`. Point `-p` at
the directory that holds it, for example `build/` after
`cmake -B build -DCMAKE_EXPORT_COMPILE_COMMANDS=ON`:

```bash
clang-include-cleaner -p build --print=changes src/main.cpp
```

```text
- <vector> @Line:2
```

- `-` lines are includes the file does not use. `+` lines are headers the file uses but only
  includes indirectly.
- `--edit` applies the changes to the file. Without `--print`, `--edit` or `--html`, the tool
  prints nothing. `--print` and `--html` take a single source file.
- On macOS, set `SDKROOT=$(xcrun --show-sdk-path)` if the compile commands have no `-isysroot`
  and standard headers such as `<string>` are not found.

Run `clang-include-cleaner --help` to see all available options. The clang-tidy check
[misc-include-cleaner](https://clang.llvm.org/extra/clang-tidy/checks/misc/include-cleaner.html)
runs the same analysis.

## Supported versions

- PyPI has wheels for LLVM 22. `pip install clang-include-cleaner` installs the newest.
- Wheels exist for Linux (x86-64, x86, ARM64 and ARMv7 with glibc; x86-64, x86 and ARMv7 with
  musl), macOS (x86-64 and ARM64) and Windows (x86-64 and x86). On other platforms pip builds
  the source distribution, which downloads and compiles LLVM.
- For other LLVM versions, the
  [static binaries](https://github.com/cpp-linter/clang-tools-static-binaries/releases) include
  clang-include-cleaner for LLVM 18 to 23.

## Contributing

See [CONTRIBUTING.md](https://github.com/cpp-linter/clang-include-cleaner/blob/main/CONTRIBUTING.md) for development setup, build instructions, and the release process, and use [GitHub issues](https://github.com/cpp-linter/clang-include-cleaner/issues) for bug reports and feature requests.

## License

This project is licensed under the Apache License 2.0 - see [LICENSE.md](https://github.com/cpp-linter/clang-include-cleaner/blob/main/LICENSE.md) for details. The `clang-include-cleaner` binary bundled in the wheels is part of the [LLVM Project](https://github.com/llvm/llvm-project/releases) and is licensed under the [Apache License 2.0 with LLVM Exceptions](https://github.com/llvm/llvm-project/blob/main/LICENSE.TXT).
