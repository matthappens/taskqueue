import Log
from Server import Server
from AmazonEC2Manager import AmazonEC2Manager
from AmazonS3Manager import AmazonS3Manager
from AmazonSQSManager import AmazonSQSManager
from JobManager import JobManager
from ResponseManager import ResponseManager

class Scarecrow (object):
    """
    Main object, creates connections and maintains handles.
    """

    def __init__ (self, args = None):
        """
        Initialize all the managers used by the system.
        """
        # Create an EC2 manager
        self.amazonEC2Manager = AmazonEC2Manager()

        # Create an S3 connection
        self.amazonS3Manager = AmazonS3Manager()

        # Create an SQS connection (& queues)
        self.amazonSQSManager = AmazonSQSManager()

        # Create a job manager
        self.jobManager = JobManager(self.amazonSQSManager)

        # Create a response manager
        self.responseManager = ResponseManager(self.amazonSQSManager)

        # Start the server
        # TODO: Send host / port args
        self.server = Server(self)


    def __str__ (self):
        """
        Return a string representing this object.
        """
        return "<Scarecrow Object>"