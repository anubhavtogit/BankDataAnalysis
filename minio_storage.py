import json
from io import BytesIO
from datetime import datetime, timezone

from minio import Minio


# =========================================================
# MINIO CONFIGURATION
# =========================================================

MINIO_ENDPOINT = "localhost:9000"

MINIO_ACCESS_KEY = "minioadmin"

MINIO_SECRET_KEY = "minioadmin123"

MINIO_BUCKET = "bankflow-data"


# =========================================================
# MINIO CLIENT
# =========================================================

minio_client = Minio(

    MINIO_ENDPOINT,

    access_key=MINIO_ACCESS_KEY,

    secret_key=MINIO_SECRET_KEY,

    secure=False
)


# =========================================================
# ENSURE BUCKET
# =========================================================

def ensure_bucket():

    if not minio_client.bucket_exists(
        MINIO_BUCKET
    ):

        minio_client.make_bucket(
            MINIO_BUCKET
        )

        print(
            f"Created bucket: {MINIO_BUCKET}"
        )


# =========================================================
# CONVERT PYDANTIC MODELS
# =========================================================

def convert_records(records):

    return [

        record.model_dump()

        for record in records
    ]


# =========================================================
# UPLOAD JSON
# =========================================================

def upload_json(
    data,
    object_name
):

    ensure_bucket()


    json_data = json.dumps(

        data,

        indent=4,

        ensure_ascii=False,

        default=str

    ).encode("utf-8")


    minio_client.put_object(

        bucket_name=MINIO_BUCKET,

        object_name=object_name,

        data=BytesIO(json_data),

        length=len(json_data),

        content_type="application/json"
    )


    print(
        f"Uploaded: "
        f"s3://{MINIO_BUCKET}/{object_name}"
    )


    return object_name


# =========================================================
# UPLOAD PYDANTIC RECORDS
# =========================================================

def upload_records(
    records,
    object_name
):

    data = convert_records(
        records
    )

    return upload_json(
        data,
        object_name
    )


# =========================================================
# TIMESTAMP
# =========================================================

def get_timestamp():

    return datetime.now(
        timezone.utc
    ).strftime(
        "%Y%m%d_%H%M%S_%f"
    )