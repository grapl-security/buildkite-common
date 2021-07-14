shell_library(
    dependencies=[":py_lib"]
)

shunit2_tests(
    name="tests",
    # Currently using relative imports for tests, which aren't visible to Pants
    dependencies=[":lib"],
    runtime_package_dependencies=[":artifacts_json_into_pulumi"]
)

pex_binary(
    name="artifacts_json_into_pulumi",
    entry_point="artifacts_json_into_pulumi.py",
)

# Make python files available to python tests
python_library(
    name="py_lib"
)
python_tests(
    name="py_tests"
)