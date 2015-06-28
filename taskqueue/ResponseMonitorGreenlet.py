from gevent import sleep
from gevent import Greenlet

class ResponseMonitorGreenlet (Greenlet):
    """
    Greenlet responsible for monitoring the responses queue to manage active EC2 nodes.
    """

    # Wait 5 seconds between polls
    PAUSE_TIME = 5

    def __init__ (self, scHandle):
        """
        Initializes the response monitor with the Scarecrow handle.
        """
        Greenlet.__init__(self)

        self.scHandle = scHandle


    def _run(self):
        """
        Continuously checks for response messages and processes them if found.

        TODO: Make use of responses somehow
        """
        self.running = True

        while self.running:
            try:
                print "Response monitor running..."

                # Get the message count
                messageCount = self.scHandle.amazonSQSManager.getQueueCount(self.scHandle.amazonSQSManager.responsesQueue)

                print '%i messages in queue...' % messageCount

                # Read a response
                response = self.scHandle.responseManager.getResponseFromResponsesQueue()

                # TODO: Do something with the response
                if response:
                    print(response)

            except Exception, responseMonitorException:
                print "Response monitor failed with exception %s." % str(responseMonitorException)

            finally:
                # Wait for a bit
                sleep(self.PAUSE_TIME)