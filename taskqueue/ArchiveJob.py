import os
import zipfile


from Job  import Job
from uuid import uuid4
import common

class ArchiveJob (Job):
    """
    Job object holding details about what to archive.
    """

    def __init__ (self, name, bucket, destinationBucket, filePath, destinationPath):
        """
        Initializes the job object with data.
        """
        # Job.__init__(self, name = name)
        self.name               = name
        self.bucket             = bucket
        self.destinationBucket  = destinationBucket
        self.filePaths          = filePath # changed to array
        self.destinationPath    = destinationPath


    def run (self, daemonHandle):
        """
        Archives the chosen S3 file to the chosen S3 destination.
        """
        print "running archive job"
        # Get a temp path to download to
        job_id = str(uuid4())
        tempPathBase = None
        for filePath in self.filePaths:
            tempPath = self.getTempPath(filePath, job_id)
            # Download the file from S3 to a temporary location
            file = daemonHandle.amazonS3Manager.downloadFile(filePath, tempPath, bucket = daemonHandle.amazonS3Manager.getBucket(self.bucket))
            tempPathBase = os.path.dirname(tempPath)
        # Get a temp destination to zip to
        tempDestinationPath = self.getTempPath(self.destinationPath)

        # Create the zip file
        self.zipPath(tempPathBase, tempDestinationPath)

        # Send the zip file to S3
        daemonHandle.amazonS3Manager.createFile(tempDestinationPath, self.destinationPath, bucket = daemonHandle.amazonS3Manager.getBucket(self.destinationBucket))


    def zipPath (self, filePath, destinationPath):
        """
        Zips a file or directory at one path to a file at another path.
        """
        print "zipping %s to %s" % (filePath, destinationPath)
        zip = zipfile.ZipFile(destinationPath, "w")
        if os.path.isdir(filePath):
            for root, dirs, files in os.walk(filePath):
                for file in files:
                    print "writing %s to zip" % str(file)
                    zip.write(os.path.join(root, file))
        else:
            zip.write(filePath, os.path.basename(filePath))
        zip.close()


    def __str__ (self):
        """
        Returns this object in string format.
        """
        return "[ArchiveJob(%s, %s, %s, %s)]" % (self.bucket, self.destinationBucket, self.filePaths, self.destinationPath)
