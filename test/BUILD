load("@my_dev_deps//:requirements.bzl", "requirement")
load("//tools/pytest:defs.bzl", "pytest_test")

pytest_test(
    name = "test_json_report_schema",
    srcs = ["test_json_report_schema.py"],
    data = ["//schemas"],
    deps = [
        requirement("jsonschema")
    ],
)

pytest_test(
    name = "test_overall_reports",
    srcs = ["test_overall_reports.py"],
    deps = [
        "//reports",
        requirement("pandas"),
    ],
)

pytest_test(
    name = "test_diversification_reports",
    srcs = ["test_diversification_reports.py"],
    deps = [
        "//reports",
        requirement("pandas"),
    ],
)
