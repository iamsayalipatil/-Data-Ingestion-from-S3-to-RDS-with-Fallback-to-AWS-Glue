import boto3
import pandas as pd
from sqlalchemy import create_engine
import pymysql
import sys

print("Script started")

# Step 1: Read CSV from S3
df = None
try:
    s3 = boto3.client('s3')
    bucket_name = 'my-data-bucket-project3'  # <-- your actual bucket name
    file_key = 'sample.csv'                   # <-- your actual CSV file name
    print(f"Trying to read {file_key} from bucket {bucket_name}...")

    obj = s3.get_object(Bucket=bucket_name, Key=file_key)
    df = pd.read_csv(obj['Body'])
    print("CSV read successfully from S3:")
    print(df.head())

except Exception as e:
    print("Error reading CSV from S3:", e, file=sys.stderr)

# Step 2: Upload to RDS if CSV read successfully
if df is not None:
    try:
        rds_host = 'my-rds-db.coxmeum0047d.us-east-1.rds.amazonaws.com'
        rds_user = 'admin'
        rds_pass = 'admin123'
        rds_db = 'my-rds-db'
        print(f"Trying to connect to RDS at {rds_host}...")

        engine = create_engine(f"mysql+pymysql://{rds_user}:{rds_pass}@{rds_host}/{rds_db}")
        df.to_sql('my_table', con=engine, if_exists='replace', index=False)
        print("Data uploaded to RDS successfully!")

    except Exception as e:
        print("RDS upload failed, fallback to Glue.", e, file=sys.stderr)
        print("Fallback to Glue executed (not implemented here yet).")
else:
    print("Skipping RDS upload because CSV not loaded")
    print("Fallback to Glue executed (not implemented here yet).")

print("Script finished")