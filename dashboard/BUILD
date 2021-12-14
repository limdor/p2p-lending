load("@my_deps//:requirements.bzl", "requirement")

py_binary(
    name = "dashboard",
    srcs = ["dashboard.py"],
    deps = [
        requirement("dash"),
        requirement("pandas"),
        requirement("plotly"),
    ],
)