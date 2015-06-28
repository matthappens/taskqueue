import traceback

from ArchiveJob import ArchiveJob
from TranscodeJob import TranscodeJob
from WatermarkJob import WatermarkJob

from AmazonSQSMessage import AmazonSQSMessage
from ArchiveJobMessage import ArchiveJobMessage
from TranscodeJobMessage import TranscodeJobMessage
from WatermarkJobMessage import WatermarkJobMessage

class JobManager (object):
    """
    Provides shared utility methods for Job objects.
    """

    # Mapping of job name to job object
    # TODO: Improve this, make it more generic somehow
    JobNameToObject = {
        "Archive": ArchiveJob,
        "Transcode": TranscodeJob,
        "Watermark": WatermarkJob
    }

    # Mapping of job name to message object
    # TODO: Improve this, make it more generic somehow
    JobNameToMessage = {
        "Archive": ArchiveJobMessage,
        "Transcode": TranscodeJobMessage,
        "Watermark": WatermarkJobMessage
    }

    def __init__ (self, amazonSQSManager):
        """
        Initialize the job manager.
        """
        # Save the parameters
        self.amazonSQSManager = amazonSQSManager


    def getJobFromJobsQueue (self):
        """
        Gets a job object from the jobs queue.
        """
        # Read a job message using the sqs manager
        jobMessage = self.amazonSQSManager.getMessage(self.amazonSQSManager.jobsQueue)

        if jobMessage:
            # Try and convert it based on the name
            try:
                return self.JobNameToObject[jobMessage["name"]].fromJobMessage(jobMessage)

            # Couldn't create a job from the message for some reason
            except Exception, invalidMessageException:
                print "Could not convert message '%s' to job (%s)." % (str(jobMessage), str(invalidMessageException))
                traceback.print_exc()
                return False

        # Found nothing
        return None


    def getJobMessageFromData (self, data):
        """
        Gets a job message object from the given data.
        """
        # We can only create a message if there is a name
        if "name" in data:
            # Create a specific object if we match the name
            if data["name"] in self.JobNameToMessage:
                return self.JobNameToMessage[data["name"]](**data)

            # Create a generic object
            return AmazonSQSMessage(**data)

        return None