import math
import datetime
from PIL import Image, ImageDraw, ImageFont

from Job import Job
import common

class WatermarkJob (Job):
    """
    A job that uses the Amazon Elastic Transcoder to apply a watermark to a movie.
    """

    def __init__ (self, name, username, contentWidth, contentHeight, contentType, bucket, destinationBucket, filePath, destinationPath):
        """
        Initalizes the job with data.
        """
        self.name               = name
        self.username           = username
        self.contentWidth       = int(contentWidth)
        self.contentHeight      = int(contentHeight)
        self.contentType        = contentType
        self.bucket             = bucket
        self.destinationBucket  = destinationBucket
        self.filePath           = filePath
        self.destinationPath    = destinationPath


    def run (self, daemonHandle):
        """
        Runs the watermarking and saves the result to S3.
        """
        # Get a transcoder pipeline
        # pipeline = daemonHandle.amazonETManager.getPipeline("WatermarkPipeline", self.bucket, self.destinationBucket)

        # print "got pipeline %s" % str(pipeline)

        # Get a temp path for the watermark
        tempWatermarkDestinationPath = self.getTempPath(common.WATERMARK_DESTINATION_PATH)

        # Create the watermark
        self.createWatermark(tempWatermarkDestinationPath)

        # Copy the watermark to S3
        daemonHandle.amazonS3Manager.createFile(tempWatermarkDestinationPath, common.WATERMARK_DESTINATION_PATH, bucket = daemonHandle.amazonS3Manager.getBucket(self.destinationBucket))

        # Create the input object
        inputObject = daemonHandle.amazonETManager.createInputObject(self.filePath)

        # Get the preset for the content type
        # typePreset = daemonHandle.amazonETManager.getPreset(self.contentType)

        # Create the output object
        outputObjects = daemonHandle.amazonETManager.createOutputObject(self.destinationPath, presetId = common.WATERMARK_PRESET_ID, watermarkFileName = common.WATERMARK_DESTINATION_PATH)

        # Create the job
        daemonHandle.amazonETManager.createJob(common.WATERMARK_PIPELINE_ID, inputObject, outputObjects)


    def createWatermark (self, watermarkDestinationPath, watermarkDestinationType = common.WATERMARK_DESTINATION_TYPE):
        """
        Creates a watermark image to be used in the transcode job.
        """
        # Create a base watermark png
        watermark = Image.new("RGBA", (self.contentWidth, self.contentHeight))

        # Grab the draw object
        draw = ImageDraw.Draw(watermark)

        # Create the font
        font = ImageFont.truetype(common.WATERMARK_FONT_FACE, common.WATERMARK_FONT_SIZE, encoding = "unic")

        # Calculate offsets
        textWidth, textHeight = draw.textsize(self.username, font = font)
        margin = (self.contentWidth - textWidth) / 2
        offset = ((self.contentHeight - textHeight) / 2) - 25

        # Add the name
        draw.text((margin, offset), self.username, font = font, fill = common.WATERMARK_FONT_COLOR)

        # Get the date string
        dateString = str(datetime.date.today())

        # Calculate offsets
        textWidth, textHeight = draw.textsize(dateString, font = font)
        margin = (self.contentWidth - textWidth) / 2
        offset = ((self.contentHeight - textHeight) / 2) + 25

        # Add the date
        draw.text((margin, offset), dateString, font = font, fill = common.WATERMARK_FONT_COLOR)

        # Rotate the watermark 45 degrees
        watermark = watermark.rotate(45)

        # Add the scarecrow vfx text
        # font = ImageFont.truetype(FONT_FACE, FONT_SIZE / 2, encoding = "unic")
        # scarecrowText = "PROPERTY OF SCARECROW VFX "
        # textWidth, textHeight = draw.textsize(scarecrowText, font = font)
        # scarecrowText *= int(math.ceil(float(contentHeight) / float(textWidth)))
        # textWidth, textHeight = draw.textsize(scarecrowText, font = font)
        # margin = (contentWidth - textWidth) / 2
        # draw.text((margin, 10), scarecrowText, font = font, fill = FONT_COLOR)
        # draw.text((margin, contentHeight - textHeight - 5), scarecrowText, font = font, fill = FONT_COLOR)

        # Save the watermark locally
        # TODO: Factor in an ID so we don't overwrite this if nodes are ever multi-threaded
        watermark.save(watermarkDestinationPath, watermarkDestinationType)


    def __str__ (self):
        """
        Return this job in a string format.
        """
        return "[WatermarkJob()]"
