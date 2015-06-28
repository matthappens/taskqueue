import os
import zipfile

from Job import Job
import common

class TranscodeJob (Job):
    """
    A job responsible for transcoding videos from one format to another.
    """

    def __init__ (self, name, bucket, destinationBucket, filePath, destinationPath):
        """
        Initalizes the job with data.
        """
        self.name               = name
        self.bucket             = bucket
        self.destinationBucket  = destinationBucket
        self.filePath           = filePath
        self.destinationPath    = destinationPath


    def run (self, daemonHandle):
        """
        Runs the transcoding and saves the result to S3.
        """
        # Get a transcoder pipeline
        # pipeline = daemonHandle.amazonETManager.getPipeline("TranscodePipeline", self.bucket, self.destinationBucket)

        # print "got pipeline %s" % str(pipeline)

        # Create the input object
        inputObject = daemonHandle.amazonETManager.createInputObject(self.filePath)

        # Get the preset for the content type
        # typePreset = daemonHandle.amazonETManager.getPreset(self.contentType)

        # Create the output object
        outputObjects = daemonHandle.amazonETManager.createOutputObject(self.destinationPath, presetId = common.TRANSCODE_PRESET_ID, thumbnail = True)

        # Create the job
        daemonHandle.amazonETManager.createJob(common.TRANSCODE_PIPELINE_ID, inputObject, outputObjects)


    def __str__ (self):
        """
        Returns this object in string format.
        """
        return "[TranscodeJob(%s, %s, %s, %s)]" % (self.bucket, self.destinationBucket, self.filePath, self.destinationPath)
