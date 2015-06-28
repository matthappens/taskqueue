from gevent import sleep
from gevent import Greenlet

import common
import traceback

class JobsMonitorGreenlet (Greenlet):
    """
    Greenlet responsible for monitoring the jobs queue to manage active EC2 nodes.

    TODO: Improve the balancing
    """

    # Wait 5 seconds between polls
    PAUSE_TIME      = 5

    def __init__ (self, scHandle):
        """
        Saves the handle and initializes the greenlet.
        """
        Greenlet.__init__(self)

        self.scHandle = scHandle


    def _run(self):
        """
        Runs the greenlet, continuously monitoring the jobs message queue and spawning more nodes if neccessary.
        """
        self.running = True

        while self.running:
            try:
                print "Jobs monitor running..."

                # Get the message count
                messageCount = self.scHandle.amazonSQSManager.getQueueCount(self.scHandle.amazonSQSManager.jobsQueue)

                print '%i messages in queue...' % messageCount

                # Check the EC2 count
                nodeCount = self.scHandle.amazonEC2Manager.getNodeCount()

                # If we have messages but no EC2 instances, boot one up
                if messageCount > 0 and nodeCount < 1:
                    self.scHandle.amazonEC2Manager.createNode()

                else:
                    # See if we need to spawn another
                    if (nodeCount * common.JOBS_PER_NODE) < messageCount:
                        print "Too many messages, spawning new node!"
                        self.scHandle.amazonEC2Manager.createNode()

            except Exception, jobsMonitorException:
                print "Jobs monitor failed with exception %s." % str(jobsMonitorException)
                traceback.print_exc()

            finally:
                # Wait for a bit
                sleep(self.PAUSE_TIME)
