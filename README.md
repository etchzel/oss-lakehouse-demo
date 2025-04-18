# Simple Demo of Lakehouse Architecture with Open Source stack

Software used:

- Apache Airflow (Orchestrator)
- Apache Spark (Compute)
- Trino (Compute/Query Engine)
- MinIO (Storage)
- Hive Metastore Service (Metadata)
- PostgreSQL (Metadata & Data Source)

NOTE: Missing components before this can run (excl.uded because large filesize):

- data.dump (in ./data-source)
- jar files

To run simply install `make` and then:

```bash
make up
```

once all services are up, open jupyter notebook on `localhost:8888`, create a notebook and run some spark sql commands:

```python
spark.sql('CREATE DATABASE bronze;')
spark.sql('CREATE DATABASE silver;')
spark.sql('CREATE DATABASE gold;')
```

Copy the contents of `./airflow/scripts/extract.py` into vi in the spark container and save it:

```bash
docker exec -it spark bash
vi extract.py
```

finally run (still in the spark container):

```bash
spark-submit --master local[*] extract.py
```

to load some table into spark.

To test some queries in trino (trino hosted on 8081 in this case), run:

```bash
docker exec -it trino trino --server=http://localhost:8081
```

and finally run:

```bash
trino> SELECT COUNT(*) FROM iceberg.bronze.events;
```

to test query.
