# Contributing

Thank you for investing your time in contributing to this project! ✨

## Table of Contents

- [Reporting Issues](#reporting-issues)
- [Pull Requests](#pull-requests)
- [Development Setup](#development-setup)
- [Building New Releases](#building-new-releases)
- [Release Process](#release-process)

## Reporting Issues

- **Bugs** — [open an issue](https://github.com/cpp-linter/clang-include-cleaner/issues/new?template=bug_report.yml)
- **Feature requests** — [open an issue](https://github.com/cpp-linter/clang-include-cleaner/issues/new?template=feature_request.yml)
- **Questions** — use [GitHub Discussions](https://github.com/cpp-linter/clang-include-cleaner/discussions)

## Pull Requests

- Please help reviewers understand the purpose of your pull request.
- Link the PR to the issue you are solving.
- If you run into merge conflicts, resolve them before requesting review.

## Development Setup

### Clone and install

```bash
git clone git@github.com:cpp-linter/clang-include-cleaner.git
cd clang-include-cleaner
pip install -e ".[test]"
```

### Run tests

```bash
pytest
```

## Building New Releases

This repository provides the logic to build and publish binary wheels of
`clang-include-cleaner`. The build process:

1. Downloads the LLVM source tree from the official GitHub releases
2. Compiles `clang-include-cleaner` statically via CMake
3. Strips the binary for size reduction
4. Packages the binary and clang builtin headers into a Python wheel

The build is orchestrated by [scikit-build-core][] and
[cibuildwheel][].

[scikit-build-core]: https://github.com/scikit-build/scikit-build-core
[cibuildwheel]: https://github.com/pypa/cibuildwheel

### Versioning

The version is stored in [`clang-include-cleaner_version.txt`](clang-include-cleaner_version.txt).
The format is `<LLVM_MAJOR>.<LLVM_MINOR>.<LLVM_PATCH>`, optionally
followed by `.<WHEEL_PACKAGING>` for rebuilds of the same LLVM version.

### Triggering a Release

#### Automated (tag push)

Push a version tag matching `v?<major>.<minor>.<patch>` (or with a
4th component) to trigger the [release workflow][]:

```bash
git tag v22.1.7
git push origin v22.1.7
```

[release workflow]: https://github.com/cpp-linter/clang-include-cleaner/actions/workflows/release.yml

#### Manual (workflow dispatch)

Go to the [release workflow][] page and click "Run workflow". The
following inputs are available:

| Input | Description | Default |
|-------|-------------|---------|
| `llvm_version` | Override the LLVM version (e.g. `22.1.7`) | (from version file) |
| `wheel_version` | Version suffix for rebuilds of the same LLVM version | `0` |
| `deploy_to_testpypi` | Deploy to [TestPyPI](https://test.pypi.org/) instead of PyPI | `false` |
| `use_qemu` | Build QEMU-emulated targets (armv7l, i686) | `true` |

## Release Process

1. Edit [`clang-include-cleaner_version.txt`](clang-include-cleaner_version.txt) to the desired version.
2. Create a pull request with the version bump.
3. Once merged, push a matching git tag to trigger the release workflow.
4. The workflow builds wheels for all platforms, tests them, and
   publishes to PyPI.
5. A GitHub Release is created automatically for tagged commits.
