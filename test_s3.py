import boto3


BUCKET_NAME = "bank-data-analysis-403659230784-403659230784-ap-south-1-an"
AWS_REGION = "ap-south-1"


s3 = boto3.client(
    "s3",
    region_name=AWS_REGION
)


response = s3.list_objects_v2(
    Bucket=BUCKET_NAME
)


print("S3 connection successful")
print("Bucket:", BUCKET_NAME)
print("Objects:", response.get("KeyCount", 0))