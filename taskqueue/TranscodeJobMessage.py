from AmazonSQSMessage import AmazonSQSMessage

class TranscodeJobMessage (AmazonSQSMessage):
    """
    Interface for an TranscodeJobMessage message.
    """

    def __init__ (self, name = None, bucket = None, destinationBucket = None, filePath = None, destinationPath = None):
        """
        Initializes the message and validates the inputs.
        """
        # Init the generic message
        super(TranscodeJobMessage, self).__init__(name = name, bucket = bucket, destinationBucket = destinationBucket, filePath = filePath, destinationPath = destinationPath)

        # Validate args
        self.validate()


    def validate (self):
        """
        Validate the arguments.

        TODO
        """
        pass
