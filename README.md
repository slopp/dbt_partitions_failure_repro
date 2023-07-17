# dbt_partitions

To reproduce:

```bash
pip install -e ".[dev]"
dbt parse --project-dir dbt_proj
pytest dbt_partitions_tests
```

The output you will see: 

```
========================================================= short test summary info ==========================================================
FAILED dbt_partitions_tests/test_assets.py::test_adhoc_asset_job - ValueError: Asset 'AssetKey(['my_first_dbt_model'])' has partitions, but no 'partition_expr' metadata value, so we don't know what colu...
================================================= 1 failed, 3 passed, 15 warnings in 8.47s =================================================
{"data": {"description": "sql table model public.my_first_dbt_model", "execution_time": 0.05741906, "index": 1, "node_info": {"materialized": "table", "meta": {}, "node_finished_at": "2023-07-17T20:06:03.980649", "node_name": "my_first_dbt_model", "node_path": "example/my_first_dbt_model.sql", "node_relation": {"alias": "my_first_dbt_model", "database": "example", "relation_name": "\"example\".\"public\".\"my_first_dbt_model\"", "schema": "public"}, "node_started_at": "2023-07-17T20:06:03.922301", "node_status": "success", "resource_type": "model", "unique_id": "model.dbt_proj.my_first_dbt_model"}, "status": "OK", "total": 2}, "info": {"category": "", "code": "Q012", "extra": {}, "invocation_id": "edc0acdd-c232-4941-b9eb-b6f8b51abe3c", "level": "info", "msg": "1 of 2 OK created sql table model public.my_first_dbt_model .................... [\u001b[32mOK\u001b[0m in 0.06s]", "name": "LogModelResult", "pid": 59230, "thread": "Thread-1", "ts": "2023-07-17T20:06:03.981088Z"}}
2 of 2 START sql view model public.my_second_dbt_model ......................... [RUN]
Exception ignored in: <generator object DbtCliInvocation.stream_raw_events at 0x162502a50>
Traceback (most recent call last):
  File "/Users/lopp/Projects/hooli-data-eng-pipelines/.venv/lib/python3.8/site-packages/dagster_dbt/core/resources_v2.py", line 814, in stream
RuntimeError: generator ignored GeneratorExit
```

In summary, the metadata is correctly set if you access the dbt decorated multi asset's metadata_by_key directly, or if you run the asset via a job or via `materialize`. The issue only occurs if you use an implied ad hoc asset job - the equivalent of running a materialization through the UI.