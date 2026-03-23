# Use Python base image
FROM python:3.9

# Set working directory
WORKDIR /app

# Copy file
COPY read_s3.py .

# Install libraries
RUN pip install boto3 pandas sqlalchemy pymysql

# Run script
CMD ["python", "read_s3.py"]