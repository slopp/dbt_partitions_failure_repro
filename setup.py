from setuptools import find_packages, setup

setup(
    name="dbt_partitions",
    packages=find_packages(exclude=["dbt_partitions_tests"]),
    install_requires=["dagster", "dagster-cloud", "dbt-duckdb", "dagster-dbt"],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)
