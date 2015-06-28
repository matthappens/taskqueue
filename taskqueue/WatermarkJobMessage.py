from AmazonSQSMessage import AmazonSQSMessage

class WatermarkJobMessage (AmazonSQSMessage):
    """
    Interface for a WatermarkJob message.
    """

    def __init__ (self, name = None, username = None, contentWidth = None, contentHeight = None, contentType = None, bucket = None, destinationBucket = None, filePath = None, destinationPath = None):
        """
        Initializes the message and validates the inputs.
        """
        # Init the generic message
        super(WatermarkJobMessage, self).__init__(name = name, username = username, contentWidth = contentWidth, contentHeight = contentHeight, contentType = contentType, bucket = bucket, destinationBucket = destinationBucket, filePath = filePath, destinationPath = destinationPath)

        # Validate args
        self.validate()


    def validate (self):
        """
        Validate the arguments.

        TODO
        """
        pass
