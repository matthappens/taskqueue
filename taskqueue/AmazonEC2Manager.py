import boto
# boto.set_stream_logger('boto')
import boto.manage.cmdshell

from gevent import sleep

import common

class AmazonEC2Manager (object):
    """
    A manager to handle EC2 nodes.
    """

    # Create an empty list of EC2 nodes
    ec2s = []

    def __init__ (self):
        """
        Initializes the EC2 connection.
        """
        # Create a connection to EC2
        self.handle = self.connect()
        #key_pair = self.handle.get_key_pair("srcrwtq-ec2-key")
        #key_pair.save('.ssh')


    def connect (self):
        """
        Connects to EC2 and returns a handle.
        """
        # return boto.ec2.connect_to_region(common.REGION)
        return boto.connect_ec2()
    

    def getAllNodes (self):
        """
        Return all nodes running.
        """
        return self.handle.get_only_instances()


    def getAllReservations (self):
        """
        Returns all node reservations.
        """
        return self.handle.get_all_reservations()


    def getUnusedNode (self):
        """
        Returns an unused node if available.
        """
        for node in self.getAllNodes():
            # Skip non-running nodes
            if node.state != "running":
                continue

            foundNode = False
            for usedNode in self.ec2s:
                if usedNode.id == node.id:
                    foundNode = True
                    break

            if not foundNode:
                return node

        return None


    def createNode (self):
        """
        Creates an EC2 node.
        """
        # Use an existing one if possible
        unusedNode = self.getUnusedNode()
        if unusedNode:
            print "Reusing old node (%s)." % str(unusedNode)
            self.setupNode(unusedNode)
            self.ec2s.append(unusedNode)
            return unusedNode

        # Check we haven't reached the limit
        if self.getNodeCount() >= common.EC2_MAX_NODES:
            print "Max nodes reached, can't create a new one."
            return None

        print "Creating new node..."

        # Reserve a node
        ec2NodeReservation = self.handle.run_instances(image_id = common.EC2_IMAGE_NAME, key_name = common.EC2_SSH_KEY_NAME, instance_type = common.EC2_INSTANCE_TYPE)
        ec2Node = ec2NodeReservation.instances[0]

        # Wait for the node to launch
        status = ec2Node.update()
        while status == "pending":
            sleep(5)
            status = ec2Node.update() 

        if status == "running":
            print "Node running!"
            print ec2Node.public_dns_name

            # Copy the source over to the node
            self.setupNode(ec2Node)

            # Add the node to the list
            self.ec2s.append(ec2Node)

            # Return the node
            return ec2Node

        print "Failed to launch instance (status %s)." % str(status)
        return None


    def getNodeCount (self):
        """
        Gets the number of EC2 nodes created.
        """
        return len(self.ec2s)
   

    def disconnect (self):
        """
        Disconnects from SQS.
        """
        self.handle.close()

 
    def sshToNode (self, node, sshKeyPath = common.EC2_SSH_KEY_PATH, userName = common.EC2_SSH_USER_NAME):
        """
        Method that will keep trying to SSH to a node until it succeeds. 

        This can be used when a node is started as it takes some time before it can be SSHed to.
        """
        attempts = 50
        while attempts > 0:
            try:
                return boto.manage.cmdshell.sshclient_from_instance(node, sshKeyPath, user_name = userName)
            except Exception, sshException:
                print "Failed to SSH into node with exception %s" % str(sshException)
            attempts -= 1
            sleep(5)

        return None


    def setupNode (self, node):
        """
        Uploads the source files to run on the EC2 instances and kicks it off.

        TODO: Automate this build somehow
        """
        # TODO: This doesn't work immediately after the instance begins running, we need to wait a bit!

        print "Setting up node..."

        # Create an ssh client to the node if not given one
        print "SSHing into node..."
        sshClient = self.sshToNode(node)

        if sshClient is None:
            print "Failed to SSH into node!"
            return

        # Set a kill timer for 50 minutes - I don't want instances staying around too long!
        # TODO: Take this out for production
        # TODO: Fix this
        print sshClient.run("shutdown -h +5 &")

        # Install gcc :(
        # TODO: Need auto-yes?
        print sshClient.run_pty("sudo yum install gcc --noplugins -y").recv(2048)

        # Install python dev
        print sshClient.run_pty("sudo yum install python-devel --noplugins").recv(2048)

        # Install pip
        # print sshClient.run_pty("sudo yum install python-pip --noplugins").recv(2048)

        # Install python libs
        # print sshClient.run_pty("sudo pip install gevent").recv(2048)

        # Create the directory to hold our source
        print sshClient.run("mkdir ScarecrowTaskQueue")
        print sshClient.run("mkdir ScarecrowTaskQueue/EC2")

        # Copy our boto config
        print sshClient.put_file(common.EC2_LOCAL_BOTO_CFG_PATH, r"ScarecrowTaskQueue/boto.cfg")
        print sshClient.run_pty("sudo mv ScarecrowTaskQueue/boto.cfg /etc/boto.cfg").recv(2048)

        # Upload the source
        sshClient.put_file(r"EC2/__init__.py", r"ScarecrowTaskQueue/EC2/__init__.py")
        sshClient.put_file(r"EC2/EC2JobsDaemon.py", "ScarecrowTaskQueue/EC2/EC2JobsDaemon.py")
        sshClient.put_file(r"EC2/launch.py", "ScarecrowTaskQueue/EC2/launch.py")

        sshClient.put_file(r"__init__.py", r"ScarecrowTaskQueue/__init__.py")
        sshClient.put_file(r"AmazonETManager.py", r"ScarecrowTaskQueue/AmazonETManager.py")
        sshClient.put_file(r"AmazonS3Manager.py", r"ScarecrowTaskQueue/AmazonS3Manager.py")
        sshClient.put_file(r"AmazonSQSManager.py", r"ScarecrowTaskQueue/AmazonSQSManager.py")
        sshClient.put_file(r"AmazonSQSMessage.py", r"ScarecrowTaskQueue/AmazonSQSMessage.py")
        sshClient.put_file(r"ArchiveJobMessage.py", r"ScarecrowTaskQueue/ArchiveJobMessage.py")
        sshClient.put_file(r"ArchiveJob.py", r"ScarecrowTaskQueue/ArchiveJob.py")
        sshClient.put_file(r"WatermarkJobMessage.py", r"ScarecrowTaskQueue/WatermarkJobMessage.py")
        sshClient.put_file(r"WatermarkJob.py", r"ScarecrowTaskQueue/WatermarkJob.py")
        sshClient.put_file(r"TranscodeJobMessage.py", r"ScarecrowTaskQueue/TranscodeJobMessage.py")
        sshClient.put_file(r"TranscodeJob.py", r"ScarecrowTaskQueue/TranscodeJob.py")
        sshClient.put_file(r"Job.py", r"ScarecrowTaskQueue/Job.py")
        sshClient.put_file(r"JobManager.py", r"ScarecrowTaskQueue/JobManager.py")
        sshClient.put_file(r"ResponseMessage.py", r"ScarecrowTaskQueue/ResponseMessage.py")
        sshClient.put_file(r"ResponseManager.py", r"ScarecrowTaskQueue/ResponseManager.py")
        sshClient.put_file(r"common.py", r"ScarecrowTaskQueue/common.py")

        # Run the program
        print "Running EC2 daemon..."
        # print sshClient.run_pty("python ScarecrowTaskQueue/EC2/launch.py &").recv(2048)
        #print sshClient.run("python ScarecrowTaskQueue/EC2/launch.py > /dev/null 2>&1 &")
        #print "EC2 daemon running!"
