load("@my_dev_deps//:requirements.bzl", "requirement")

py_test(
    name = "test_p2p",
    srcs = ["test_p2p.py"],
    deps = [
        requirement("pytest"),
        "//:p2p",
    ],
)

py_test(
    name = "test_jsonReportSchema",
    srcs = ["test_jsonReportSchema.py"],
    deps = [
        requirement("pytest"),
        requirement("jsonschema")
    ],
)
