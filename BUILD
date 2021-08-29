load("@pip//:requirements.bzl", "requirement")
load("@rules_python//python:defs.bzl", "py_binary")

py_binary(
    name = "main",
    srcs = [
        "main.py",
        "p2pplatform.py",
    ],
    data = [
        "//data/iuvo",
        "//data/mintos",
    ],
    deps = [
        requirement("pandas"),
        requirement("xlrd"),
        requirement("openpyxl"),
    ],
)
