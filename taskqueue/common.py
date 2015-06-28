# General config
REGION  = "us-east-1a" # The AWS region to connect to; US-EAST is the cheapest!
TMP_DIR = r"ScarecrowTaskQueue/tmp/" # Temporary directory for files to be saved to

# Flask config
FLASK_HOST = "localhost"
FLASK_PORT = 5000

# EC2 config
EC2_IMAGE_NAME          = "ami-bba18dd2" # The image name of the virtual machines being used; defaults to an Amazon provided Fedora box
EC2_SSH_KEY_NAME        = "scrcrwtq-ec2-key" # Setup with:  key_pair = self.handle.create_key_pair(SSH_KEY_NAME); key_pair.save('.ssh')
EC2_SSH_KEY_PATH        = r".ssh/scrcrwtq-ec2-key.pem" # This is generated at the same time as the above; you can also do this on the AWS console
EC2_MAX_NODES           = 2 # Maximum number of virtual machines running at any one time 
EC2_INSTANCE_TYPE       = "m1.small" # The type of machine; defaults to super low power
EC2_SSH_USER_NAME       = "ec2-user" # The username on the machine, using Amazon default
EC2_LOCAL_BOTO_CFG_PATH = r"/etc/boto.cfg" # The location of the boto config file containing your AWS access keys

# Elastic transcoder config
AET_IAM             = "arn:aws:iam::143417950393:role/Elastic_Transcoder_Default_Role" # The security role used, can setup on AWS console
AET_THUMBNAIL_NAME  = "{fileName}_thumbnail_{count}_{resolution}" # The name of thumbnail files e.g. vid_thumbnail_00001_256x256

# Jobs monitor config
JOBS_PER_NODE = 5 # The number of jobs that can be in the queue, per node, before we need to spawn a new node

# Watermark config
WATERMARK_PRESET_ID         = r"1389829705009-b9m13s" # Setup on AWS for now
WATERMARK_PIPELINE_ID       = r"1389821940775-hrrvad" # Setup on AWS for now
WATERMARK_DESTINATION_PATH  = r"watermark.png"
WATERMARK_DESTINATION_TYPE  = "PNG"
WATERMARK_FONT_FACE         = r"/usr/share/fonts/dejavu/DejaVuSerif.ttf" # Must be available on the EC2 machine
WATERMARK_FONT_SIZE         = 40
WATERMARK_FONT_COLOR        = (0, 0, 0, 100)

# Transcode config
TRANSCODE_PRESET_ID         = r"1389838177708-x5fqw7" # Setup at https://console.aws.amazon.com/elastictranscoder/home?region=us-east-1#presets:
TRANSCODE_PIPELINE_ID       = r"1389838113472-cgvz46" # Setup at https://console.aws.amazon.com/elastictranscoder/home?region=us-east-1#pipelines:

# Globals
GlobalSCHandle = None # Used to access other managers at any point in the system (mainly for Flask)

###########
# Methods #
###########

import collections
def convertFromUnicode (data):
    """
    Converts the data of some object to be string instead of unicode.
    """
    if isinstance(data, basestring):
        return str(data)
    elif isinstance(data, collections.Mapping):
        return dict(map(convertFromUnicode, data.iteritems()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(convertFromUnicode, data))
    else:
        return data
