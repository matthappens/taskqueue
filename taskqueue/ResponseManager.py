from ResponseMessage import ResponseMessage

class ResponseManager (object):
    """
    Provides shared utility methods for response objects.
    """

    # Static list of responses received
    responses = []

    def __init__ (self, amazonSQSManager):
        """
        Initialize the job manager.
        """
        # Save the parameters
        self.amazonSQSManager = amazonSQSManager


    def getResponseFromResponsesQueue (self):
        """
        Gets a respone object from the responses queue.
        """
        # Read a response message using the sqs manager
        response = self.amazonSQSManager.getMessage(self.amazonSQSManager.responsesQueue)

        # Convert it to a ResponseMessage object if we get one
        if response:
            response = ResponseMessage(**response)

        # Add it to the list
        if response:
            self.responses.append(response)

        return response
