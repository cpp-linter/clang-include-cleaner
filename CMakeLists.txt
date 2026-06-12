cmake_minimum_required(VERSION 3.16...3.31)
project(${SKBUILD_PROJECT_NAME} VERSION ${SKBUILD_PROJECT_VERSION})

message(STATUS "clang-include-cleaner wheel version: ${SKBUILD_PROJECT_VERSION}")
string(REGEX MATCH "^([0-9]+)\.([0-9]+)\.([0-9]+)" LLVM_VERSION "${SKBUILD_PROJECT_VERSION}")
set(LLVM_VERSION_MAJOR ${CMAKE_MATCH_1}) # https://cmake.org/cmake/help/latest/variable/CMAKE_MATCH_n.html
message(STATUS "LLVM version: ${LLVM_VERSION}")

# Define a build rule for clang-include-cleaner
set(LLVM_DOWNLOAD_URL "https://github.com/llvm/llvm-project/releases/download/llvmorg-${LLVM_VERSION}/llvm-project-${LLVM_VERSION}.src.tar.xz")
include(ExternalProject)
ExternalProject_add(build-clang-include-cleaner
  URL "${LLVM_DOWNLOAD_URL}"
  SOURCE_SUBDIR llvm
  SOURCE_DIR ${CMAKE_BINARY_DIR}/llvm-project
  BINARY_DIR ${CMAKE_BINARY_DIR}/llvm
  UPDATE_COMMAND ""
  INSTALL_COMMAND ""
  USES_TERMINAL_DOWNLOAD 1
  USES_TERMINAL_CONFIGURE 1
  USES_TERMINAL_BUILD 1
  CMAKE_ARGS -DCMAKE_BUILD_TYPE=Release -DBUILD_SHARED_LIBS=OFF -DLLVM_ENABLE_ZSTD=OFF -DLLVM_ENABLE_PROJECTS=clang$<SEMICOLON>clang-tools-extra
  BUILD_COMMAND ${CMAKE_COMMAND} --build . --target clang-include-cleaner
)

set(config-subfolder "")
if(CMAKE_GENERATOR MATCHES "Visual Studio")
  set(config-subfolder "Release")
endif()
set(clang-include-cleaner-executable ${CMAKE_BINARY_DIR}/llvm/${config-subfolder}/bin/clang-include-cleaner${CMAKE_EXECUTABLE_SUFFIX})

# Reduce the size of the executable by executing strip if it is present on the system
find_program(STRIP_EXECUTABLE strip)
if(STRIP_EXECUTABLE)
  add_custom_target(
    strip-clang-include-cleaner
    ALL
    COMMAND ${STRIP_EXECUTABLE} ${clang-include-cleaner-executable}
    COMMENT "Stripping clang-include-cleaner executable for size reduction"
  )
  add_dependencies(strip-clang-include-cleaner build-clang-include-cleaner)
endif()

# Define an installation rule that copies the executable to our Python package
install(
  PROGRAMS
    ${clang-include-cleaner-executable}
  DESTINATION clang_include_cleaner/data/bin
)

install(
  DIRECTORY
    ${CMAKE_BINARY_DIR}/llvm/lib/clang/${LLVM_VERSION_MAJOR}/include
  DESTINATION clang_include_cleaner/data/lib/clang/${LLVM_VERSION_MAJOR}
)
