import logging

from pyspark.sql import DataFrame, SparkSession
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Schemagenerator:
    def __init__(self):
        try:
            logger.info(f"Starting SparkSession")  

            self.df: DataFrame = None
            self.spark_session: SparkSession = SparkSession.builder \
                .appName("inferschema") \
                .config('spark.jars.packages', 'org.apache.spark:spark-avro_2.12:3.1.1') \
                .getOrCreate()
            
        except Exception as ex:
                logger.error(f"Unable to retrieve schema due to {ex}")
        
    def generate_schema(self, file_path: Path, has_header: bool):

        self.file_path = str(file_path)
        self.file_type = self.determine_mimetype(self.file_path)

        if self.file_type != "unknown":
            logger.info(f"Processing {self.file_type} from: {self.file_path}")

            self.df = self.spark_session.read \
                            .format(self.file_type) \
                            .option("header", has_header) \
                            .option("inferSchema", True) \
                            .load(self.file_path)

        
            self.df = self.df.select([self.df[column].alias(column.replace('_c', 'col_')) for column in self.df.columns])         
            
            schema = self.df.schema
        
        else:
            logger.info(f"Cannot process {self.file_type} from: {self.file_path}")
            schema = None

        
        return schema

    
    def determine_mimetype(self, file_path):

        logger.info(f"Determining file type for: {file_path}")

        if file_path.endswith('csv'):
            return 'csv'
        elif file_path.endswith('avro'):
            return 'avro'
        elif file_path.endswith('.parquet'):
            return 'parquet'
            
        return 'unknown'
    

    def close(self):
        logger.info(f"Stopping SparkSession")
        self.spark_session.stop()