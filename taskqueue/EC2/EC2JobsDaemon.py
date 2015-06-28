# from gevent import sleep
# from gevent import Greenlet
from time import sleep
import traceback

# Hack to make python play nicely on windows and linux
import sys
sys.path.append("..")
sys.path.append("/home/ec2-user/ScarecrowTaskQueue")

from AmazonS3Manager import AmazonS3Manager
from AmazonSQSManager import AmazonSQSManager
from AmazonETManager import AmazonETManager
from AmazonSQSMessage import AmazonSQSMessage
from ResponseMessage import ResponseMessage
from JobManager import JobManager

class EC2JobsDaemon (object):
    """
    Greenlet responsible for monitoring the jobs queue to pull off and run any new jobs found.

    TODO: Proper logging
    """

    # Wait 5 seconds between polls
    PAUSE_TIME = 5

    def __init__ (self):
        """
        Initializes the managers for the jobs daemon.
        """
        # Init the Greenlet
        # Greenlet.__init__(self)

        # Create amazon handles
        self.amazonS3Manager    = AmazonS3Manager()
        self.amazonSQSManager   = AmazonSQSManager()
        self.amazonETManager    = AmazonETManager()

        # Create the job manager
        self.jobManager = JobManager(self.amazonSQSManager)


    def run(self):
        """
        Loops checking for new jobs and runs them if it gets one.
        """
        self.running = True

        while self.running:
            try:
                print "Checking for new jobs..."

                # Read from the queue
                job = self.jobManager.getJobFromJobsQueue()

                # Create an empty response message
                responseMessage = None

                # Run the job if we got one
                if job is not None and job is not False:
                    job.run(self)

                    # Add a success response
                    responseMessage = ResponseMessage(name = "Response", success = True, message = "Completed job %s successfully." % str(job))

                # If job is false it means it failed at converting a message to a job
                elif job is False:
                    # Add a failure response
                    responseMessage = ResponseMessage(name = "Response", success = False, message = "Failed to convert job message.")
                    
                if responseMessage:
                    self.amazonSQSManager.addQueueMessage(self.amazonSQSManager.responsesQueue, responseMessage)

            except Exception, jobsDaemonException:
                print "Jobs daemon failed with exception %s." % str(jobsDaemonException)
                traceback.print_exc()

                try:
                    # Add a failure response
                    responseMessage = ResponseMessage(name = "Response", success = False, message = "Failed to complete job %s." % str(job))
                    self.amazonSQSManager.addQueueMessage(self.amazonSQSManager.responsesQueue, responseMessage)

                except Exception, jobsDaemonFailureResponseException:
                    print "Jobs daemon failed to add failure response with exception %s." % str(jobsDaemonFailureResponseException)

            finally:
                # Wait for a bit
                sleep(self.PAUSE_TIME)
