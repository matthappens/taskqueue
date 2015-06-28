import sys
sys.path.append("..")

import unittest2 as unittest

from ScarecrowTaskQueue.AmazonS3Manager import AmazonS3Manager
from ScarecrowTaskQueue.AmazonSQSMessage import AmazonSQSMessage

class AmazonS3ManagerTests (unittest.TestCase):
    """
    Tests for AmazonS3Manager methods.
    """

    def setUp (self):
        """
        Create an AmazonS3Manager to test on.
        """
        # Create an S3 manager connection
        self.amazonS3Manager = AmazonS3Manager()


    def tearDown(self):
        """
        Disconnect the AmazonS3Manager.
        """
        # Disconnect from S3
        self.amazonS3Manager.disconnect()
        self.amazonS3Manager = None


if __name__ == '__main__':
    try:
        unittest.main()
    except SystemExit as inst:
        if inst.args[0] is True: # raised by sys.exit(True) when tests failed
            raise