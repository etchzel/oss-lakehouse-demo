import logging
from pyspark.sql import SparkSession

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S %Z"
)

def read_data(spark):
    read_properties = {
        "url": "jdbc:postgresql://postgres:5432/postgres",
        "driver": "org.postgresql.Driver",
        "user": "postgres",
        "password": "postgres",
        "dbtable": "events"
    }
    return spark.read \
                .format("jdbc") \
                .options(**read_properties)  \
                .load()

def write_data(df, data_format, mode, table_name):
    return df.write \
             .format(data_format) \
             .mode(mode)  \
             .saveAsTable(f"bronze.{table_name}")
          
def main():
    spark = SparkSession.builder \
        .appName("PySpark ETL") \
        .config("spark.jars.packages", "org.postgresql:postgresql:42.7.4,org.apache.hadoop:hadoop-aws:3.3.4,com.amazonaws:aws-java-sdk-bundle:1.12.262") \
        .config("spark.hadoop.fs.s3a.endpoint", "http://minio:9000") \
        .config("spark.hadoop.fs.s3a.access.key", "admin") \
        .config("spark.hadoop.fs.s3a.secret.key", "password") \
        .config("spark.hadoop.fs.s3a.connection.ssl.enabled", "false") \
        .config("spark.hadoop.fs.s3a.path.style.access", "true") \
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
        .config("spark.hadoop.fs.s3a.aws.credentials.provider", "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider") \
        .config("spark.hadoop.hive.metastore.uris", "thrift://hive-metastore:9083") \
        .config("spark.sql.extensions", "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.iceberg.spark.SparkCatalog") \
        .config("spark.sql.catalog.spark_catalog.type", "hive") \
        .config("spark.sql.catalog.spark_catalog.uri", "thrift://hive-metastore:9083") \
        .config("spark.sql.warehouse.dir", "s3a://lakehouse/") \
        .getOrCreate()

    # Step 1: Read Data
    logging.info("Reading PostgreSQL data")
    df = read_data(spark)

    # Step 2: Write Parquet files
    logging.info("Writing to spark warehouse as Parquet files")
    write_data(df, 
               data_format="parquet", 
               mode="overwrite", 
               table_name="events")

    logging.info("Job completed successfully!")

if __name__ == "__main__":
    main()
