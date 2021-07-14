shell_library()

shunit2_tests(
    name="tests",
    # Currently using relative imports for tests, which aren't visible to Pants
    dependencies=[":lib"]
)

python_library(
    name="py_lib"
)
python_tests(
    name="py_tests"
)