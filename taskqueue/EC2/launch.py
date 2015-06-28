from EC2JobsDaemon import EC2JobsDaemon

def main ():
    """
    Initializes the EC2 program.
    """
    # TODO: Send args

    ec2JobsDaemon = EC2JobsDaemon()
    # ec2JobsDaemon.start()
    ec2JobsDaemon.run()

    print "Job started!"


# App entry point
if __name__ == "__main__":
    main()