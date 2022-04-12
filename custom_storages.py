from storages.backends.s3boto3 import S3Boto3Storage

class StaticStorage(S3Boto3Storage):
    bucket_name = 'shortsqueeze'
    location = 'static'

class MediaStorage(S3Boto3Storage):
    bucket_name = 'shortsqueeze'
    location = 'media'