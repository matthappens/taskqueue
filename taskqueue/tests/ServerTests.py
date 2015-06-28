import sys
sys.path.append("..")

from time import sleep
from subprocess import Popen, PIPE
import unittest2 as unittest
import requests
import json

from AmazonS3Manager import AmazonS3Manager
from AmazonSQSManager import AmazonSQSManager
from AmazonSQSMessage import AmazonSQSMessage
from JobManager import JobManager

# serverProcess = Popen(['python', 'C:\Users\Aldarn\Documents\Visual Studio 2012\Projects\ScarecrowTaskQueue\ScarecrowTaskQueue\launch.py', '-d'], stdout = PIPE)
amazonS3Manager = AmazonS3Manager()
amazonSQSManager = AmazonSQSManager()
jobManager = JobManager(amazonSQSManager)

def tearDownModule ():
    """
    Close any connects left open after all tests.
    """
    amazonS3Manager.disconnect()
    amazonSQSManager.disconnect()


class ServerTests (unittest.TestCase):
    """
    Tests for operations offered by the Flask server.
    """

    def donttestAddJob (self):
        """
        Tests adding a job to the Server.
        """
        # Create watermark job data
        jobData = {
            "name": "Test Job"
        }

        # Test it
        self.jobFromData(jobData)


    def donttestAddWatermarkJob (self):
        """
        Tests adding a watermark job to the Server.
        """
        # Create watermark job data
        jobData = {
            "name":               "Watermark",
            "username":           "Aldarn",
            "contentWidth":       "256",
            "contentHeight":      "256",
            "contentType":        "Generic 720p",
            "bucket":             amazonS3Manager.getBucket().name,
            "destinationBucket":  amazonS3Manager.getBucket().name,
            "filePath":           r"misc/sc0108_edit_ref_v1_nhd_srgb.mov",
            "destinationPath":    r"misc/watermark.mov"
        }

        # Test it
        self.jobFromData(jobData)


    def donttestAddArchiveJob (self):
        """
        Tests adding an archive job to the Server.
        """
        # Create watermark job data

        jobData = {
            "name":               "Archive",
            "bucket":             amazonS3Manager.getBucket().name,
            "destinationBucket":  amazonS3Manager.getBucket().name,
            "filePath":           r"misc/sc0108_edit_ref_v1_nhd_srgb.mov",
            "destinationPath":    r"misc/watermarked_movie.zip"
        }

        # Test it
        self.jobFromData(jobData)


    def test_TEArchiveJob(self):
        te_s3_loc = "te/assets/ba220/pix/plates/bg/v001/default/ba220_plates_bg_ingest_v001.%s.dpx"
        frames = ['1001','1002','1003','1004','1005','1010','1011','1012','1013','1014']
        filepaths = [te_s3_loc % s for s in frames]
        jobData = {
            "name":               "Archive",
            "bucket":             amazonS3Manager.getBucket().name,
            "destinationBucket":  amazonS3Manager.getBucket().name,
            "filePath":           [r'te/assets/ba220/pix/plates/bg/v001/default/ba220_plates_bg_ingest_v001.1001.dpx',
                                   r'te/assets/ba220/pix/plates/bg/v001/default/ba220_plates_bg_ingest_v001.1002.dpx',
                                   r'te/assets/ba220/pix/plates/bg/v001/default/ba220_plates_bg_ingest_v001.1003.dpx',
                                   r'te/assets/ba220/pix/plates/bg/v001/default/ba220_plates_bg_ingest_v001.1004.dpx',
                                   r'te/assets/ba220/pix/plates/bg/v001/default/ba220_plates_bg_ingest_v001.1005.dpx'],
            "destinationPath":    r"te/assets/ba220/pix/plates/bg/v001/default/ba220_plates_bg_ingest_v001.zip"
        }
        self.jobFromData(jobData)

    def donttestAddTranscodeJob (self):
        """
        Tests adding a transcode job to the Server.
        """
        # Create transcode job data
        jobData = {
            "name":               "Transcode",
            "bucket":             amazonS3Manager.getBucket().name,
            "destinationBucket":  amazonS3Manager.getBucket().name,
            "filePath":           r"misc/sc0108_edit_ref_v1_nhd_srgb.mov",
            "destinationPath":    r"misc/transcoded.mov"
        }

        # Test it
        self.jobFromData(jobData)


    def jobFromData (self, data):
        """
        Creates a test job using data.
        """
        newJobMessage = jobManager.getJobMessageFromData(data)

        print str(newJobMessage)
        print json.dumps(newJobMessage)

        # Create and send a post request
        headers = {
            'Content-length': len(json.dumps(newJobMessage)), 
            'Content-type': 'application/json', 
            'Accept': 'text/plain'
        }

        # TODO: For some reason this submits the data in the wrong format for flask, fix it!
        request = requests.post("http://localhost:5000/addJob", data = json.dumps(newJobMessage), headers = headers)
        print "request: %s" % str(request.text)

        # Wait
        sleep(10)

        # Check it's now in the queue
        watermarkJobMessage = amazonSQSManager.getMessage(amazonSQSManager.jobsQueue)

        print str(watermarkJobMessage)

        # Test equality
        #self.assertEquals(watermarkJobMessage, newWatermarkJobMessage, "Job added and job received unequal.")


if __name__ == '__main__':
    try:
        unittest.main()
    except SystemExit as inst:
        if inst.args[0] is True: # raised by sys.exit(True) when tests failed
            raise