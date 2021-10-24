load("@linting_system//:rules.bzl", "linter")

package(default_visibility = ['//visibility:public'])

linter(
    name = "python",
    executable_path = "pylint",
    config = "//tools/pytest:.pylintrc",
    config_option = "--rcfile",
)
