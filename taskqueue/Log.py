#!/usr/bin/env python

# Python imports
import inspect

class Log:
	"""
	Leight weight logger.
	"""

	INFO = 1
	DEBUG = 2

	def __init__ (self, level = INFO):
		"""
		Initialises the log.
		"""
		# Set the level
		self.level = level

		# Store past logs
		self.logs = []


	def log (self, message, warning = False):
		"""
		Creates a new log.
		"""
		# Add it to the list
		self.logs.append(message)

		# Print it if debug mode
		if self.level == Log.DEBUG or warning:
			# Get the class name
			try:
				className = inspect.stack()[1][0].f_locals["self"].__class__.__name__
			except:
				className = "Unknown"

			# Get the function name
			try:
				functionName = inspect.stack()[1][3]
			except:
				functionName = "Unknown"

			# Print the message with some info of which class & method it's in
			if warning:
				print "WARNING: %s.%s: %s" % (str(className), str(functionName), str(message))
			else:
				print "%s.%s: %s" % (str(className), str(functionName), str(message))


	def warn (self, message):
		"""
		Wrapper around log for a warning.
		"""
		self.log(message, warning = True)


	def setLevel (self, level):
		"""
		Sets the log level.
		"""
		self.level = level


# Log handle
log = Log()
