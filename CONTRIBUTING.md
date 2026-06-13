# Contributing

Thank you for investing your time in contributing to this project! ✨

This project packages `clang-include-cleaner` for PyPI. Contributions
that improve the packaging, build pipeline, CI, or platform support are
welcome. For changes to the tool itself, see the
[LLVM project](https://github.com/llvm/llvm-project).

## Table of Contents

- [Reporting Issues](#reporting-issues)
- [Pull Requests](#pull-requests)
- [Development Setup](#development-setup)
- [Releasing](#releasing)

## Reporting Issues

- **Bugs and feature requests** — [open an issue](https://github.com/cpp-linter/clang-include-cleaner/issues/new/choose)
- **Questions** — start a [discussion](https://github.com/cpp-linter/discussions) or use [issues](https://github.com/cpp-linter/clang-include-cleaner/issues)

## Pull Requests

- Link the PR to its issue.
- Resolve merge conflicts before requesting review.

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

## Releasing

### Build process

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

### How to release

1. Edit `clang-include-cleaner_version.txt` to the desired version.
2. Create a pull request with the version bump.
3. Once merged, push a matching git tag:

   ```bash
   git tag v<major>.<minor>.<patch>
   git push origin v<major>.<minor>.<patch>
   ```

4. The [release workflow][] builds wheels for all platforms, tests them,
   and publishes to PyPI. A GitHub Release is created automatically.

To rebuild the same LLVM version (e.g. to fix a packaging issue), use
`.post<N>` as the 4th version component, or trigger the workflow
manually via the [Actions tab][release workflow] with these inputs:

| Input | Description | Default |
|-------|-------------|---------|
| `llvm_version` | Override the LLVM version | (from version file) |
| `wheel_version` | Version suffix for rebuilds | `0` |
| `deploy_to_testpypi` | Deploy to [TestPyPI](https://test.pypi.org/) instead of PyPI | `false` |
| `use_qemu` | Build QEMU-emulated targets (armv7l, i686) | `true` |

[release workflow]: https://github.com/cpp-linter/clang-include-cleaner/actions/workflows/release.yml
