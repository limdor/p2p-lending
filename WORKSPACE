load("//third_party:third_party.bzl", "load_third_party_libraries")

load_third_party_libraries()

load("//third_party:transitive_dependencies.bzl", "load_transitive_dependencies")

load_transitive_dependencies()

load("@rules_python//python:pip.bzl", "pip_install")

pip_install(
    requirements = "//:requirements.txt",
)
