load("@my_deps//:requirements.bzl", "requirement")
load("@rules_python//python:defs.bzl", "py_binary")

py_binary(
    name = "main",
    srcs = [
        "main.py",
    ],
    data = [
        "//data/iuvo",
        "//data/mintos",
        "//schemas"
    ],
    deps = [
        ":p2p",
    ]
)

py_library(
    name = "p2p",
    srcs = [
        "__init__.py",
        "logger.py",
        "p2p.py",
    ],
    deps = [
        "//marketplace",
        "//reports",
        requirement("pandas"),
        requirement("xlrd"),
        requirement("openpyxl"),
    ],
    visibility = ["//test:__pkg__"],
)
