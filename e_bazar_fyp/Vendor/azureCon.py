
import os,uuid
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import uuid



def uploadimg(img):
    # file_upload_name = str(uuid.uuid4()) + img.name
    # connString= "DefaultEndpointsProtocol=https;AccountName=ebazarstorage;AccountKey=/7mecioPQmqSFAA0tjPgO3FbS3uJ2v8XDHYcBHeENnB2Acj963UpcmXyCOwyatIczjixmGER8Bzi+AStNQ1y+Q==;EndpointSuffix=core.windows.net"
    # blob_service_client = BlobServiceClient.from_connection_string(connString)
    # blob_client = blob_service_client.get_blob_client(container="imageserver", blob=file_upload_name)
    # content_type= "image/png"
    # blob_client.upload_blob(img.file,content_type=content_type)
    # blob_url = blob_client.url
    # return blob_url
    # from django.conf import settings
    # import os
    # from django.core.files.storage import FileSystemStorage
    #
    # base_dir = settings.STATICFILES_DIRS
    # static= base_dir[0]
    # file_path = os.path.join(static, 'imageserver')
    # fs = FileSystemStorage(location=file_path)
    # imgName= img.name
    # imgName= imgName.replace(" ","")
    # file_upload_name = str(uuid.uuid4()) + imgName
    # filename = fs.save(file_upload_name, img)
    # url= fs.url(filename)
    # link= "https://ebazarstorageserver.blob.core.windows.net/imageserver"
    # link+=url
    # return link

    import boto3
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
