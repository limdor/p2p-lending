load("@my_deps//:requirements.bzl", "requirement")
load("@rules_python//python:defs.bzl", "py_binary")

py_library(
    name = "reports",
    srcs = [
        "__init__.py",
        "overall.py",
        "diversification.py",
        "calculator.py"
    ],
    deps = [
        "//:logger",
        "//marketplace",
        requirement("pandas"),
    ],
    visibility = ["//visibility:public"],
)
