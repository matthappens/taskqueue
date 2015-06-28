from AmazonSQSMessage import AmazonSQSMessage

class ResponseMessage (AmazonSQSMessage):
    """
    Interface for a Response message.
    """

    def __init__ (self, name = None, success = True, message = None):
        """
        Initializes the response message and validates the data.
        """
        # Init the generic message
        super(AmazonSQSMessage, self).__init__(name = name, success = success, message = message)

        # Validate args
        self.validate(success, message)


    def validate (self, success, message):
        """
        Validate the arguments.

        TODO
        """
        pass
