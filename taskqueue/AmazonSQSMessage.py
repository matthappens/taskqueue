class AmazonSQSMessage (dict):
    """
    Encapsulates a message to be sent over an Amazon SQS.
    """

    def __init__(self, name = None, **kwargs):
        # Create the dict
        super(AmazonSQSMessage, self).__init__(name = name, **kwargs)
        self.itemlist = super(AmazonSQSMessage, self).keys()

        # Validate the arguments
        self.baseValidate()


    def __setitem__(self, key, value):    
        self.itemlist.append(key)
        super(AmazonSQSMessage, self).__setitem__(key, value)


    def __iter__(self):
        return iter(self.itemlist)


    def keys(self):
        return self.itemlist


    def values(self):
        return [self[key] for key in self]  


    def itervalues(self):
        return (self[key] for key in self)


    def baseValidate (self):
        """
        Validate the args.
        """
        if not self["name"]:
            raise ValueError("A name must be provided for the message.")

        if len(self["name"]) < 1:
            raise ValueError("Message name must not be blank.")


    def validate (self):
        """
        This should be extended by a child.
        """
        raise NotImplementedError


    # def __str__ (self):
    #   """
    #
    #   """
    #   return "<Message (%s)>" % self["name"]
