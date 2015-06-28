from AmazonSQSMessage import AmazonSQSMessage

class ArchiveJobMessage (AmazonSQSMessage):
    """
    Interface for an ArchiveJob message.
    """

    def __init__ (self, name = None, bucket = None, destinationBucket = None, filePath = None, destinationPath = None):
        """
        Initializes the message and validates the inputs.
        """
        # Init the generic message
        super(ArchiveJobMessage, self).__init__(name = name, bucket = bucket, destinationBucket = destinationBucket, filePath = filePath, destinationPath = destinationPath)

        # Validate args
        self.validate()


    def validate (self):
        """
        Validate the message.

        TODO
        """
        pass
