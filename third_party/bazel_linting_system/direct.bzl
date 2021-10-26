"""
Dependency to Bazel linting system developed by thundergolfer
"""

load("@bazel_tools//tools/build_defs/repo:utils.bzl", "maybe")
load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

def load_bazel_linting_system():
    maybe(
        http_archive,
        name = "linting_system",
        strip_prefix = "bazel-linting-system-0.4.1",
        urls = [
            "https://github.com/thundergolfer/bazel-linting-system/archive/refs/tags/v0.4.1.zip",
        ],
        patches = ["//third_party/bazel_linting_system:output.patch"],
        sha256 = "fa62cecb008e6f319a81f4f619c0d632ad7e3087c7d0c331028eb91c027d49e5",
    )
