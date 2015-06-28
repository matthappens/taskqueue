import boto
# boto.set_stream_logger('boto')

import common

class AmazonS3Manager (object):
    """
    A manager to handle S3 communications.
    """

    def useDefaultBucket (method):
        """
        Decorator that injects the default bucket into methods, unless specified.
        """
        def wrapper (self, *arg, **kwargs):
            if "bucket" in kwargs:
                result = method(self, kwargs["bucket"], *arg)
            else:
                result = method(self, self.getBucket(), *arg)
            return result

        return wrapper


    def __init__ (self):
        """
        Initializes the S3 connection.
        """
        # Create a connection to S3
        self.handle = self.connect()


    def connect (self):
        """
        Connects to S3 and returns a handle.
        """
        return boto.connect_s3()
        # return boto.s3.connect_to_region(common.REGION)


    def createBucket (self, name = "scarecrow_assets"):
        """
        Creates a bucket for storing files in.
        """
        return self.handle.create_bucket(name)

    # edit, using scarecrow_assets for testing
    def getBucket (self, name = "scarecrow_assets"):
        """
        Returns the bucket with the given name.
        """
        try:
            return self.handle.get_bucket(name)

        except Exception, getBucketException:
            print "Exception getting bucket %s" % str(getBucketException)

        finally:
            return self.createBucket(name)


    @useDefaultBucket
    def createFile (self, bucket, filePath, destinationPath, public = True):
        """
        Creates a file in S3.
        """
        # Create a file key to save to
        # TODO uploaded archive files might be enormous,
        # requiring multipart upload
        key = bucket.new_key(destinationPath)
        key.set_contents_from_filename(str(filePath))

        # Set public access if chosen
        if public:
            key.set_acl('public-read')

        return key


    @useDefaultBucket
    def downloadFile (self, bucket, fileName, destination):
        """
        Downloads a file from S3 to a given location.
        """
        print bucket.name
        print fileName
        key = bucket.get_key(fileName)
        key.get_contents_to_filename(destination)


    @useDefaultBucket
    def moveFile (self, bucket, fileName, destinationBucket, destination):
        """
        Moves a file from one S3 location to another.
        """
        key     = bucket.get_key(fileName)
        newKey  = key.copy(destinationBucket.name, destination)

        if newKey.exists:
            key.delete()
        else:
            raise Exception("Failed to move file '%s' to (%s) %s." % (fileName, destinationBucket.name, destination))

        return newKey


    def disconnect (self):
        """
        Disconnects from S3.
        """
        self.handle.close()
