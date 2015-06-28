# Scarecrow imports
from JobsMonitorGreenlet import JobsMonitorGreenlet
from ResponseMonitorGreenlet import ResponseMonitorGreenlet

# Flask imports
from flask import Flask, request, redirect, url_for

# Gevent imports (& monkey patch for Flask compatability)
from gevent.pywsgi import WSGIServer
from gevent import monkey
monkey.patch_all()

import traceback

from AmazonEC2Manager import AmazonEC2Manager
from AmazonSQSManager import AmazonSQSManager
from AmazonSQSMessage import AmazonSQSMessage
from ArchiveJobMessage import ArchiveJobMessage

import common
from common import GlobalSCHandle

class Server (object):
    """
    Manages the Flask server and related processes.
    """

    FLASK_APP       = Flask(__name__)
    FLASK_APP.debug = True

    def __init__ (self, scHandle, host = common.FLASK_HOST, port = common.FLASK_PORT):
        """
        Creates the greenlets and flask server.
        """
        # Save the parameters
        global GlobalSCHandle
        GlobalSCHandle          = scHandle
        self.host               = host
        self.port               = port

        # Launch the greenlets
        self.jobsMonitor        = JobsMonitorGreenlet(scHandle)
        self.jobsMonitor.start()
        self.responseMonitor    = ResponseMonitorGreenlet(scHandle)
        self.responseMonitor.start()
        

        # Start the Flask server
        http                    = WSGIServer((host, port), self.FLASK_APP)
        http.serve_forever()


    # Index page
    @FLASK_APP.route("/")
    def index ():
        """
        Placeholder.
        
        TODO: Do something with this...
        """
        return "Hello World!"


    # Add job form page
    @FLASK_APP.route("/addJobForm", methods = ["GET"])
    def addJobForm ():
        """
        Provides a form to add a job.
        """
        form = "<html><head><title>Add Job</title></head><body>"

        if "success" in request.args:
            form += "<p><font color='green'><b>%s</b></font></p>" % str(request.args["success"])
        elif "error" in request.args:
            form += "<p><font color='red'><b>%s</b></font></p>" % str(request.args["error"])       

        #form += "<p><form action='/addJob' method='POST'>Job Name: <input type='text' name='name'/><br/>File Name: <input type='text' name='fileName'/><br/>Target Path: <input type='text' name='targetPath'/><br/><input type='hidden' name='fromForm' value='1'/><input type='submit' value='Add Job'></form></p>"
        form += "<p><form action='/addJob' method='POST'>Job Name: <input type='text' name='name'/><br/>File Name: <input type='text' name='filePath'/><br/>Target Path: <input type='text' name='destinationPath'/><br/><input type='submit' value='Add Job'></form></p>"
        return form


    @FLASK_APP.route("/addJob", methods = ["POST"])
    def addJob ():
        """
        Adds a job to the jobs queue from a post request.
        """
        try:
            if request.method == "POST":
                # If we get json data use that instead
                if request.json and len(request.json) > 0:
                    request.form = request.json

                # Create the job message
                jobMessage = GlobalSCHandle.jobManager.getJobMessageFromData(request.form)

                print "Job message: %s" % str(jobMessage) 

                # Add the job
                if jobMessage:
                    GlobalSCHandle.amazonSQSManager.addQueueMessage(GlobalSCHandle.amazonSQSManager.jobsQueue, jobMessage)

                # Redirect to form with 'success'
                if "fromForm" in request.form and request.form["fromForm"]:
                    return redirect(url_for("addJobForm", success = "%s job added!" % request.form["name"]))

                return "Job added successfully."

        except Exception, addJobError:
            print "Failed to add job with exception %s." % str(addJobError)

        return "Error adding job."


    @FLASK_APP.route("/queueStatus")
    def queueStatus ():
        """
        Displays a page with status information about the queues.
        """
        # amazonSQSManager = AmazonSQSManager()
        # ec2Manager = AmazonEC2Manager()

        page = "<html><head><title>Queue Status</title></head><body>"

        page += "<p><h1>Jobs Queue</h1></p>"
        page += "<p><b>Messages:</b> %s<br/>" % str(GlobalSCHandle.amazonSQSManager.getQueueCount(GlobalSCHandle.amazonSQSManager.jobsQueue))
        page += "<b>EC2 Nodes:</b> %s</p>" % str(GlobalSCHandle.amazonEC2Manager.getNodeCount())

        page += "<p><h1>Responses Queue</h1></p>"
        page += "<p><b>Messages:</b> %s<br/>" % str(GlobalSCHandle.amazonSQSManager.getQueueCount(GlobalSCHandle.amazonSQSManager.responsesQueue))

        if len(GlobalSCHandle.responseManager.responses) > 0:
            page += "<b>Responses:</b><br/>"
            for response in GlobalSCHandle.responseManager.responses:
                page += "Success: %s Message: %s<br/>" % (str(response["success"]), str(response["message"]))

        page += "</p></body></html>"

        return page


    @FLASK_APP.route("/uploadForm", methods = ["GET"])
    def uploadForm ():
        """
        Provides a form to upload a file to S3.
        """
        page = "<html><head><title>Upload File to S3</title></head><body>"
        page += "<p><h1>Upload a file to S3</h1></p>"

        if "success" in request.args:
            page += "<p><font color='green'><b>%s</b></font></p>" % str(request.args["success"])
        elif "error" in request.args:
            page += "<p><font color='red'><b>%s</b></font></p>" % str(request.args["error"])  
             
        page += "<p><form action='uploadFile' method='POST'>"
        page += "Destination File Name: <input type='text' name='destinationFilePath'/><br/>"
        page += "File Path: <input type='text' name='filePath'/><br/>"
        page += "<input type='submit' value='Upload File'/>"
        page += "</form></p>"

        page += "</body></html>"

        return page


    @FLASK_APP.route("/uploadFile", methods = ["POST"])
    def uploadFile ():
        """
        Uploads a file to S3.
        """
        try:
            if request.method == "POST":
                print "Uploading file '%s' to file '%s'." % (str(request.form["filePath"]), str(request.form["destinationFilePath"]))

                # Create an S3 file
                s3File = GlobalSCHandle.amazonS3Manager.createFile(request.form["filePath"], request.form["destinationFilePath"])

                # Redirect to upload form
                return redirect(url_for("uploadForm", success = "File %s uploaded!" % request.form["filePath"]))

        except Exception, uploadFileException:
            print "Failed to upload file with exception %s." % str(uploadFileException)

        return "Failed to upload file."
