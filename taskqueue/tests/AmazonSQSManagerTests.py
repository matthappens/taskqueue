import sys
sys.path.append("..")

import unittest2 as unittest

from ScarecrowTaskQueue.AmazonSQSManager import AmazonSQSManager
from ScarecrowTaskQueue.AmazonSQSMessage import AmazonSQSMessage

class AmazonSQSManagerTests (unittest.TestCase):
    """

    """

    def setUp (self):
        """
        Create an AmazonSQSManager to test on.
        """
        # Create an S3 manager connection
        self.amazonSQSManager = AmazonSQSManager()


    def tearDown(self):
        """
        Disconnect the AmazonSQSManager. 
        """
        # Disconnect from S3
        self.amazonSQSManager.disconnect()
        self.amazonSQSManager = None


    def testAddJobMessage (self):
        """
        Tests adding a job to an SQS.
        """
        # Create the message
        newJobMessage = AmazonSQSMessage(name = "Test Job Message")

        print str(newJobMessage)

        # Add it to the queue
        self.amazonSQSManager.addQueueMessage(self.amazonSQSManager.jobsQueue, newJobMessage)

        # Check it's now in the queue
        jobMessage = self.amazonSQSManager.getMessage(self.amazonSQSManager.jobsQueue)

        print str(jobMessage)

        # Test equality
        self.assertEquals(jobMessage, newJobMessage, "Job added and job received unequal.")
        # self.assertEquals(jobMessage["name"], newJobMessage["name"], "Job added and job received unequal.")


if __name__ == '__main__':
    try:
        unittest.main()
    except SystemExit as inst:
        if inst.args[0] is True: # raised by sys.exit(True) when tests failed
            raise