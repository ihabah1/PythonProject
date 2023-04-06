#README 

this project stands for communicating with AWS tools and it includes commands to run in S3 AWS env using Client and Buckets adjustment. 
every phase used to handle different abilities of S3 hands-on communication.
and it tested with two different implementations. 

#Requirment 
Python 3.7 or higher
Boto3 1.18.47 or higher
AWS account with S3 access

#Setup
1. go install git@github.com:ihabah1/AWS-AND-PYTHON.git
$ github-clone-all
2.Configure your AWS credentials by following the steps in the AWS documentation.
Replace the region_name value in the session object with your preferred region.

#Usage
Run the Python script from your terminal: python s3_bucket_management.py
The script will create two S3 buckets, upload a file to the first bucket, copy it to the second bucket, and delete it from the second bucket.
It will also enable versioning and encryption for the buckets, set an access control policy, and print the list of buckets and objects.
Finally, it will delete all the objects and versions inside the buckets and delete the buckets themselves.

#Disclaimer
This script is provided as an example and should be tested and modified to fit your specific use case. Be aware of the AWS costs associated with S3 storage and 