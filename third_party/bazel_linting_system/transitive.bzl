"""
Transitive dependencies for Bazel linting system developed by thundergolfer
"""

load("@linting_system//repositories:repositories.bzl", linting_sys_repositories = "repositories")

def load_bazel_linting_system_transitive_dependencies():
    linting_sys_repositories()
