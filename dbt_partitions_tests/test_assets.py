from dbt_partitions import (
    downstream_asset,
    test_dbt_assets,
    daily_partitions,
    manifest,
)
from dagster_dbt import DbtCli
from dagster_duckdb_pandas import DuckDBPandasIOManager
from dagster._utils import file_relative_path
from dagster import define_asset_job, AssetSelection, Definitions, AssetKey, build_asset_context, materialize
import duckdb

DBT_PROJECT_DIR = file_relative_path(__file__, "../dbt_proj")

test_job = define_asset_job(
    name="test_job",
    selection=AssetSelection.keys(
        manifest.get_asset_key_for_model("my_first_dbt_model"),
        manifest.get_asset_key_for_model("my_second_dbt_model"),
        AssetKey("downstream_asset"),
    ),
    partitions_def=daily_partitions,
)
test_resources = {
    "dbt": DbtCli(project_dir=DBT_PROJECT_DIR),
    "io_manager": DuckDBPandasIOManager(database=f"{DBT_PROJECT_DIR}/example.duckdb"),
}

defs = Definitions(
    assets=[test_dbt_assets, downstream_asset],
    resources=test_resources,
    jobs=[test_job],
)

def test_partition_expr_exists():
    metadata = test_dbt_assets.metadata_by_key[AssetKey(['my_second_dbt_model'])]
    print(metadata.keys())
    assert 'partition_expr' in metadata

def test_partitioned_assets_job_with_metadata():
    test_job_def = defs.get_job_def("test_job")
    try:
        test_job_def.execute_in_process(
            tags={"dagster/partition": "2023-07-16"}, resources=test_resources
        )
    except duckdb.BinderException as e:
        print(f"failed as expected with: {e}")
    

def test_partitioned_assets_materialize():
    try:
        materialize(
            assets=[test_dbt_assets, downstream_asset],
            resources=test_resources,
            partition_key="2023-07-16"
        )
    except duckdb.BinderException as e:
        print(f"failed as expected with: {e}")

def test_adhoc_asset_job():
    asset_job = defs.get_implicit_job_def_for_assets([AssetKey("my_first_dbt_model"), AssetKey("my_second_dbt_model"), AssetKey("downstream_asset")])
    asset_job.execute_in_process(
        tags={"dagster/partition": "2023-07-16"}
    )
