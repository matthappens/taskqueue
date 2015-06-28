import os

import common

class Job (object):
    """
    Generic job object.
    """

    @classmethod
    def fromJobMessage (cls, jobMessage):
        """
        Creates a job object from a JobMessage.
        """
        print "class %s" % str(cls)
        print "jobMessage %s" % str(jobMessage)
        return cls(**jobMessage)


    def __init__ (name = None):
        """
        Initialize the job.
        """
        self.name = name


    def run (self, daemonHandle):
        """
        Runs the job.

        Must be implemented by specific job object.
        """
        raise NotImplementedError


    def getTempPath (self, filePath, job_id=""):
        """
        Gets a temporary location to store this file.

        Usually by EC2 instances to store S3 files being processed.

        TODO filepath may contain directories.  If so, shave them off
        and replace with a tmp uuid, 
        """
        # Check the temp directory exists and make it if not
        if not os.path.exists(os.path.join(common.TMP_DIR, job_id)):
            os.makedirs(os.path.join(common.TMP_DIR, job_id))

        # Return the path
        return os.path.join(common.TMP_DIR, job_id, os.path.basename(filePath))


    def __str__ (self):
        """
        Return the job in a string form.
        """
        return "[Job(%s)]" % self.name


