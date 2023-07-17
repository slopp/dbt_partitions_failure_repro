from dagster import Definitions, DailyPartitionsDefinition, asset
from dagster_dbt import dbt_assets, DbtCli, DbtManifest
from dagster._utils import file_relative_path
import json
from dagster_duckdb_pandas import DuckDBPandasIOManager

DBT_PROJECT_DIR = file_relative_path(__file__, "../dbt_proj")
DBT_PROFILES_DIR = file_relative_path(__file__, "../dbt_proj")
DBT_MANIFEST = file_relative_path(__file__, "../dbt_proj/target/manifest.json")

daily_partitions = DailyPartitionsDefinition(start_date="2023-07-15")


class CustomizedDbtManifest(DbtManifest):
    @classmethod
    def node_info_to_metadata(cls, node_info):
        metadata = {"partition_expr": "some_partitioned_column"}
        return metadata


manifest = CustomizedDbtManifest.read(path=DBT_MANIFEST)


@dbt_assets(
    manifest=manifest,
    partitions_def=daily_partitions,
)
def test_dbt_assets(context, dbt: DbtCli):
    dbt_vars = {"date": context.partition_key}
    dbt_args = ["run", "--vars", json.dumps(dbt_vars)]

    yield from dbt.cli(dbt_args, context=context).stream()


@asset(partitions_def=daily_partitions)
def downstream_asset(context, my_second_dbt_model):
    return


defs = Definitions(
    assets=[test_dbt_assets, downstream_asset],
    resources={
        "dbt": DbtCli(project_dir=DBT_PROJECT_DIR),
        "io_manager": DuckDBPandasIOManager(
            database=f"{DBT_PROJECT_DIR}/example.duckdb"
        ),
    },
)
