#!/bin/bash
# This script performs feature engineering and data transformation

cd /home/abhishek/Documents/Study/dmml_assignment/group_4_dmml

set -x

#execute ddl if table does not exist
echo "Executing DDL script to create tables if they do not exist"
spark-sql \
  --packages io.delta:delta-spark_2.12:3.1.0 \
  --conf "spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension" \
  --conf "spark.sql.catalog.spark_catalog=org.apache.spark.sql.delta.catalog.DeltaCatalog" \
  -f code/sql/table_ddl.sql
if [ $? -ne 0 ]; then
  echo "Error executing DDL script"
  exit 1
fi

#execute feature engineering and transformation
echo "Executing feature engineering and transformation script"
spark-sql \
  --packages io.delta:delta-spark_2.12:3.1.0 \
  --conf "spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension" \
  --conf "spark.sql.catalog.spark_catalog=org.apache.spark.sql.delta.catalog.DeltaCatalog" \
  -f code/sql/06_FE_and_transformation.sql
if [ $? -ne 0 ]; then
  echo "Error executing feature engineering and transformation script"
  exit 1
fi