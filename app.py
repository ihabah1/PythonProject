import boto3
import uuid
import os
import tempfile

# Create a session
if __name__ == '__main__': 
    session = boto3.Session(region_name='eu-west-1')

# Create an S3 client and resource
s3_client = session.client('s3')
s3_resource = session.resource('s3')

# Create the first bucket using the s3_resource client
first_bucket_name = "firstpythonbucket-" + str(uuid.uuid4())
first_response = s3_resource.create_bucket(
    Bucket=first_bucket_name,
    CreateBucketConfiguration={"LocationConstraint": "eu-west-1"}
)

# Create the second bucket using the s3_client method
second_bucket_name = "secondpythonbucket-" + str(uuid.uuid4())
second_response = s3_client.create_bucket(
    Bucket=second_bucket_name,
    CreateBucketConfiguration={"LocationConstraint": "eu-west-1"}
)


# Create a new file and upload it using ServerSideEncryption:
def create_temp_file(size, filename, prefix="temp"):
    with tempfile.NamedTemporaryFile(prefix=prefix, dir="tmp", delete=False) as f:
        f.write(os.urandom(size))
        filename = f.name
    return filename

# create the fisrt file
first_file_name = "firstfile.txt"
with open(os.path.join("tmp", first_file_name), "w") as f:
    f.write("testt text")
    
# upload to the first bucket using Bucket instcance
s3_resource.Object(first_bucket_name, first_file_name).upload_file(os.path.join("tmp", first_file_name))

# upload to the first bucket using client
s3_resource.meta.client.upload_file(os.path.join("tmp", first_file_name), first_bucket_name, first_file_name)

# Copy the first file to the second bucket
second_file_name = "secondfile.txt"
s3_resource.Object(second_bucket_name, second_file_name).copy_from(
    CopySource={"Bucket": first_bucket_name, "Key": first_file_name}
)

#delete from second bucket 
s3_resource.Object(second_bucket_name, first_file_name).delete()

# Download the second file to /tmp directory
#s3_resource.Object(second_bucket_name, second_file_name).download_file(f'/tmp/{second_file_name}')


# access to anyone by conifg ACL attibute 
second_file_name = create_temp_file(400, 'thirdfile.txt', 's')
second_object = s3_resource.Object(first_bucket_name, second_file_name)
second_object.upload_file(second_file_name, ExtraArgs={'ACL': 'public-read'})

second_object_acl = second_object.Acl()

# Enable versioning for the first bucket
def enable_bucket_versioning(bucket_name):
    bkt_versioning = s3_resource.BucketVersioning(bucket_name)
    bkt_versioning.enable()
    print(bkt_versioning.status)

#Enable_bucket_versioning(first_bucket_name)
response = second_object_acl.put(ACL='private')
second_object_acl.grants

# Encryption
# With S3, you can protect your data using encryption. You’ll explore server-side encryption using the AES-256 algorithm where AWS manages both the encryption and the keys.

third_file_name = create_temp_file(300, os.path.join("tmp", "thirdfile.txt"), "t")
third_object = s3_resource.Object(second_bucket_name, third_file_name)
third_object.upload_file(third_file_name, ExtraArgs={"ServerSideEncryption": "AES256"})

# Upload the same file again to create a new version
s3_resource.Object(first_bucket_name, first_file_name).upload_file(
os.path.join("tmp", first_file_name),
ExtraArgs={"ServerSideEncryption": "AES256"}
)

# Print all existing buckets
    # Print all existing buckets
response = s3_client.list_buckets()
for bucket in response["Buckets"]:
    print(f"{bucket['Name']}\t{bucket['CreationDate']}")


# Get all objects in the first bucket
first_bucket = s3_resource.Bucket(first_bucket_name)
for obj in first_bucket.objects.all():
    print(obj.key)

# Delete all objects and versions inside the first and second bucket
bucket_names = [first_bucket_name, second_bucket_name]
for bucket_name in bucket_names:
    bucket = s3_resource.Bucket(bucket_name)
    bucket.object_versions.delete()
    bucket.objects.all().delete()

# Delete all buckets
for bucket_name in bucket_names:
    try:
        s3_client.delete_bucket(Bucket=bucket_name)
        print(f"Bucket {bucket_name} deleted.")
    except botocore.exceptions.ClientError as e:
        print(f"Error deleting bucket {bucket_name}: {e}")
