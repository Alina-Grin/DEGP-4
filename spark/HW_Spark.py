from pyspark.sql import SparkSession, Window
from pyspark.sql.functions import *

spark = ( SparkSession.builder.appName('HW_app').master('local').getOrCreate() )

df_covid = spark.read.option('header', True).option('inferSchema', True).csv('owid-covid-data.csv')
print(df_covid.where(col('date') == '2021-03-31')\
	.select('iso_code', 'location', (col('total_cases') / col('population')))\
	.orderBy((col('total_cases') / col('population')).desc()).show(15))

w = Window.partitionBy('location')
print(df_covid.where((col('date') >= '2021-03-25') & (col('date') <= '2021-03-31'))\
	.select('date', 'location', 'new_cases')\
	.withColumn('max_new_cases', max('new_cases').over(w)).where(col('new_cases') == col('max_new_cases')).drop('max_new_cases')\
	.orderBy(col('new_cases').desc()).show(10))


print(df_covid.where((col('date') >= '2021-03-25') & (col('date') <= '2021-03-31') & (col('location') == 'Russia'))\
	.withColumn('yesterday_cases', lag('new_cases', 1, 8769).over(Window.orderBy('date')))\
	.select('date', 'yesterday_cases', 'new_cases', col('new_cases') - col('yesterday_cases')).where(col('yesterday_cases') > 0).show())

#WARN WindowExec: No Partition Defined for Window operation! Moving all data to a single partition, this can cause serious performance degradation.