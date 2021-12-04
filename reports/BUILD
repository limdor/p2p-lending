load("@my_deps//:requirements.bzl", "requirement")
load("@rules_python//python:defs.bzl", "py_binary")
load("//tools/pytest:defs.bzl", "pytest_test")

pytest_test(
    name = "calculator_test",
    srcs = ["calculator_test.py"],
    deps = [
        ":reports",
        requirement("pandas"),
    ],
)

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
