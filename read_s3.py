import boto3
import pandas as pd
from io import StringIO
from sqlalchemy import create_engine

# S3 connection
s3 = boto3.client('s3', region_name='ap-south-1')

bucket_name = "my-data-bucket-project3"
file_key = "sample.csv"

# Read from S3
response = s3.get_object(Bucket=bucket_name, Key=file_key)
content = response['Body'].read().decode('utf-8')

df = pd.read_csv(StringIO(content))

print("✅ Data from S3:")
print(df)

# RDS connection
try:
    engine = create_engine(
        "mysql+pymysql://admin:admin123@my-rds-db.coxmeum0047d.us-east-1.rds.amazonaws.com/testdb"
    )

    df.to_sql('employees', con=engine, if_exists='replace', index=False)

    print("✅ Data uploaded to RDS successfully")

except Exception as e:
    print("❌ Error uploading to RDS:", e)
