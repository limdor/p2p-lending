load("@my_dev_deps//:requirements.bzl", "requirement")
load("//tools/pytest:defs.bzl", "pytest_test")

filegroup(
    name = "schemas",
    srcs = ["monthlyReport.json"],
    visibility = ["//visibility:public"],
)

pytest_test(
    name = "test_json_report_schema",
    srcs = ["test_json_report_schema.py"],
    data = ["//schemas"],
    deps = [
        requirement("jsonschema")
    ],
)
