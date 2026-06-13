# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability, please **do not** open a public
issue. Instead, report it privately via
[GitHub's private vulnerability reporting](https://github.com/cpp-linter/clang-include-cleaner/security/advisories/new).

We'll respond as quickly as possible and keep you updated throughout the
process.

## Supported Versions

Only the latest release receives security patches.

## Binary Integrity

The `clang-include-cleaner` binary bundled in wheels is built from the
official [LLVM source tree](https://github.com/llvm/llvm-project) at the
tagged release version. Builds are performed on GitHub Actions runners
with no third-party dependencies beyond those declared in the build
pipeline.

If you need to verify a specific binary, you can reproduce the build
locally using the [release workflow](.github/workflows/release.yml) with
`cibuildwheel`.
