
import uuid
import boto3


def uploadimg(img):
    ACCESS_KEY = 'AKIAZGCSSIZ5UVPEFQLX'
    SECRET_KEY = "b4as/f23gOoe06ZufAZLhcMML8Rr1JvvIEAsnOcy"
    REGION_NAME = "us-east-1"
    imgName= img.name
    imgName= imgName.replace(" ","")
    file_name = str(uuid.uuid4()) + imgName


    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY,
                      region_name=REGION_NAME)
    bucket_name = 'ebazar-bucket'

    s3.upload_fileobj(img.file, bucket_name, file_name,ExtraArgs={'ContentType': 'image/png'})
    s3_url = f"https://{bucket_name}.s3.amazonaws.com/{file_name}"
    s3.put_object_acl(Bucket=bucket_name, Key=file_name, ACL='public-read')
    return s3_url
