load("@my_deps//:requirements.bzl", "requirement")

py_binary(
    name = "dashboard",
    srcs = ["dashboard.py"],
    deps = [
        requirement("dash"),
        ":charts",
        ":components",
        ":tables",
        "//:p2p",
    ],
)

py_library(
    name = "charts",
    srcs = ["charts.py"],
    deps = [
        requirement("pandas"),
        requirement("plotly"),
        "//marketplace",
    ],
    visibility = ["//visibility:public"],
)

py_library(
    name = "layouts",
    srcs = ["layouts.py"],
    deps = [
        requirement("dash"),
        "//reports",
    ],
    visibility = ["//visibility:public"],
)

py_library(
    name = "tables",
    srcs = ["tables.py"],
    deps = [
        requirement("pandas"),
        requirement("plotly"),
        "//marketplace",
    ],
    visibility = ["//visibility:public"],
)

py_library(
    name = "figures",
    srcs = ["figures.py"],
    deps = [
        requirement("plotly"),
    ],
    visibility = ["//visibility:public"],
)

py_library(
    name = "components",
    srcs = ["components.py"],
    deps = [
        requirement("dash"),
        ":figures",
    ],
    visibility = ["//visibility:public"],
)
