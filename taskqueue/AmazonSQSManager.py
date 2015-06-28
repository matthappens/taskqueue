import boto
# boto.set_stream_logger('boto')

import json

import common
from AmazonSQSMessage import AmazonSQSMessage

class AmazonSQSManager (object):
    """
    A manager to handle SQS communications.
    """

    def __init__ (self):
        """
        Initializes the SQS connection.
        """
        # Create a connection to SQS
        self.handle = self.connect()

        # Initialize the default queues
        self.initDefaultQueues()


    def connect (self):
        """
        Connects to S3 and returns a handle.
        """
        # return boto.sqs.connect_to_region(common.REGION)
        return boto.connect_sqs()


    def createQueue (self, name, clear = True):
        """
        Creates an SQS queue.
        """
        queue = self.handle.create_queue(name)
        if queue and clear:
            queue.clear()
        return queue


    def getQueue (self, name):
        """
        Gets an SQS queue.
        """
        return self.handle.get_queue(name)


    def connectToQueue (self, name):
        """
        Connects to an existing queue or creates a new one if it doesn't exist.
        """
        # Try and get the queue before creating a new one
        queue = self.getQueue(name)
        if queue is None:
            queue = self.createQueue(name)
        return queue


    def initDefaultQueues (self):
        """
        Connects to or creates the default queues.
        """
        self.jobsQueue      = self.connectToQueue("JobsQueue")
        self.responsesQueue = self.connectToQueue("ResponsesQueue")


    def getMessage (self, queue, delete = True):
        """
        Returns a message from the queue.
        """
        message = queue.read()

        if message:
            messageData = common.convertFromUnicode(json.loads(message.get_body()))
            if delete:
                queue.delete_message(message)
            # TODO: This should probably cast into the correct type of message
            return AmazonSQSMessage(**messageData)

        return None


    def getQueueCount (self, queue):
        """
        Returns the count of messages in the given queue.
        """
        return queue.count()


    def addQueueMessage (self, queue, message):
        """
        Adds a message to the given queue.
        """
        # Convert to an SQS message
        sqsMessage = queue.new_message(body = json.dumps(message))

        # Add it to the queue
        queue.write(sqsMessage)


    def removeQueueMessage (self, queue, message):
        """
        Removes a message from the given queue.
        """
        pass


    def disconnect (self):
        """
        Disconnects from SQS.
        """
        self.handle.close()
