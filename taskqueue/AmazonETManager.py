import boto
# boto.set_stream_logger('boto')
import boto.manage.cmdshell

import common

class AmazonETManager (object):
    """
    A manager to handle Amazon elastic transcoder operations.
    """

    def __init__ (self):
        """
        Initializes the EC2 connection.
        """
        # Create a connection to AET.
        self.handle = self.connect()


    def connect (self):
        """
        Connects to AET and returns a handle.
        """
        return boto.connect_elastictranscoder()
        # return boto.elastictranscoder.connect_to_region(common.REGION)


    def createPipeline (self, name, fromBucket, toBucket, notifications = {'Progressing': '', 'Completed': '', 'Warning': '', 'Error': ''}):
        """
        Creates a transcoder pipeline.
        """
        return self.handle.create_pipeline(name, fromBucket, toBucket, common.AET_IAM, notifications)


    def getPipeline (self, name, fromBucket, toBucket, create = True):
        """
        Returns a pipeline by the given name or creates a new one if not found.
        """
        for pipeline in self.handle.list_pipelines():
            print "found existing pipeline %s (%s)" % (str(pipeline), str(dir(pipeline)))
            if pipeline == name:
                return pipeline

        if create:
            return self.createPipeline(name, fromBucket, toBucket)
        return None


    def createInputObject (self, fileName, frameRate = "auto", resolution = "auto", aspectRatio = "auto", interlaced = "auto", container = "auto"):
        """
        Creates an input object to be used in a transcode.

        More info at http://docs.aws.amazon.com/elastictranscoder/latest/developerguide/create-job.html.

        Options:
            "Key":"name of the file to transcode",
            "FrameRate":"auto"|"10"|"15"|"23.97"|"24"|"25"|"29.97"|"30"|"60",
            "Resolution":"auto"|"width in pixelsxheight in pixels",
            "AspectRatio":"auto"|"1:1"|"4:3"|"3:2"|"16:9",
            "Interlaced":"auto"|"true"|"false",
            "Container":"auto"|"3gp"|"asf"|"avi"|"divx"|"flv"|"mkv"|"mov"|"mp4"|"mpeg"|"mpeg-ps"|"mpeg-ts"|"mxf"|"ogg"|"vob"|"wav"|"webm"
        """
        # TODO: Validate input against enums

        return {
             "Key": fileName,
             "FrameRate": frameRate,
             "Resolution": resolution,
             "AspectRatio": aspectRatio,
             "Interlaced": interlaced,
             "Container": container 
        }


    def createOutputObject (self, fileName, presetId = None, rotate = "auto", thumbnail = False, watermarkFileName = None):
        """
        Creates an output object to be used in a transcode.

        More info at http://docs.aws.amazon.com/elastictranscoder/latest/developerguide/create-job.html.

        Presets at http://docs.aws.amazon.com/elastictranscoder/latest/developerguide/system-presets.html.

        Options:
            "Key":"name of the transcoded file",
            "ThumbnailPattern":""|"pattern",
            "Rotate":"auto|0|90|180|270",
            "PresetId":"preset to use for the job",
            "SegmentDuration":"[1, 60]",
            "Watermarks":[
                "InputKey":"name of the .png or .jpg file",
                "PresetWatermarkId":"value of Video:Watermarks:Id in preset"
            ]
        """
        # TODO: Validate input against enums

        outputObject = {
            "Key": fileName,
            "PresetId": presetId,
            "Rotate": rotate
        }

        if thumbnail:
            outputObject["ThumbnailPattern"] = common.AET_THUMBNAIL_NAME.replace("{fileName}", fileName)

        if watermarkFileName:
            outputObject["Watermarks"] = [{"InputKey": watermarkFileName, "PresetWatermarkId": "scarecrow.watermark"}]

        return  [outputObject]


    def createJob (self, pipelineId, inputObject, outputObjects):
        """
        Creates a job for the transcoder on the given pipeline with given transcode objects.
        """
        return self.handle.create_job(pipelineId, input_name = inputObject, outputs = outputObjects)


    def getPresets (self):
        """
        Returns all presets.
        """
        return self.handle.list_presets()


    def getPreset (self, name):
        """
        Returns a preset by the given name if found.
        """
        for preset in self.getPresets():
            print "found preset %s (%s) %s" % (str(preset), str(dir(preset)), str(type(preset)))
            if preset == "Presets":
                print str(preset[0])
            if preset == name:
                return preset

        return None