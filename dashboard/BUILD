load("@my_deps//:requirements.bzl", "requirement")

py_binary(
    name = "dashboard",
    srcs = ["dashboard.py"],
    deps = [
        requirement("dash"),
        ":charts",
    ],
)


py_binary(
    name = "charts",
    srcs = ["charts.py"],
    deps = [
        requirement("pandas"),
        requirement("plotly"),
        "//marketplace",
    ],
    visibility = ["//visibility:public"],
)