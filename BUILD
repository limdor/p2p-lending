load("@pip//:requirements.bzl", "requirement")
load("@rules_python//python:defs.bzl", "py_binary")

py_binary(
    name = "main",
    srcs = ["main.py"],
    data = [":mintos", ":iuvo"],
    deps = [
        requirement("pandas"),
        requirement("xlrd"),
    ],
)

filegroup(
    name = "mintos",
    srcs = ["20201213-current-investments.xlsx"],
)

filegroup(
    name = "iuvo",
    srcs = ["MyInvestments-20201213-193645.xlsx"],
)