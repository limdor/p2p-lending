load("@my_dev_deps//:requirements.bzl", "requirement")
load("//tools/pytest:defs.bzl", "pytest_test")

pytest_test(
    name = "test_p2p",
    srcs = ["test_p2p.py"],
    deps = [
        "//:p2p",
    ],
)

pytest_test(
    name = "test_jsonReportSchema",
    srcs = ["test_jsonReportSchema.py"],
    data = ["//schemas"],
    deps = [
        requirement("jsonschema")
    ],
)
