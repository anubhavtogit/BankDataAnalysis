import json
import boto3

from datetime import datetime, timezone


# =========================================================
# AWS S3 CONFIGURATION
# =========================================================

BUCKET_NAME = "bank-data-analysis-403659230784-403659230784-ap-south-1-an"

AWS_REGION = "ap-south-1"


# =========================================================
# S3 CLIENT
# =========================================================

s3_client = boto3.client(
    "s3",
    region_name=AWS_REGION
)


# =========================================================
# TIMESTAMP
# =========================================================

def get_timestamp():

    return datetime.now(
        timezone.utc
    ).strftime(
        "%Y%m%d_%H%M%S"
    )


# =========================================================
# UPLOAD RECORDS TO S3
# =========================================================

def upload_records(
    records,
    object_name
):

    records_as_dict = [

        record.model_dump()
        if hasattr(record, "model_dump")
        else record

        for record in records

    ]

    json_data = json.dumps(
        records_as_dict,
        indent=4,
        ensure_ascii=False,
        default=str
    )


    s3_client.put_object(

        Bucket=BUCKET_NAME,

        Key=object_name,

        Body=json_data.encode("utf-8"),

        ContentType="application/json"

    )


    print(
        f"Uploaded successfully:"
    )

    print(
        f"s3://{BUCKET_NAME}/{object_name}"
    )