load("//tools/pytest:defs.bzl", "pytest_test")

pytest_test(
    name = "datacollection_test",
    srcs = ["datacollection_test.py"],
    deps = [
        ":datacollection",
        "//marketplace",
    ],
)

py_library(
    name = "datacollection",
    srcs = [
        "__init__.py",
        "datacollection.py",
    ],
    visibility = ["//visibility:public"],
)
