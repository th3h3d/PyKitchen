"""The logger module provides interface for keeping logs of all operations.
"""

#Magic Methods
__version__ = '1.0'

__author__ = ("Haci Emre Dasgin <haci.dasgin@gmail.com>")

__all__ = ["_debug", "_warning", "_info", "_error"]



import logging
import time


class Logger():
	"""The class contain all needed functions which are used for logging all operation going on.
	"""
	
	def __init__(self):
		"""Set mandatory input.
		"""
		self._FILE_NAME = time.strftime("%Y%m%d", time.localtime())
		self._FILE_NAME = str(self._FILE_NAME)+".log"
		self._FILE_MODE = "a"
		self._FORMAT = '%(asctime)s - %(levelname)s - %(message)s'

	def _warning(self, Message):
		"""This method is used to create a log for warning type.
		"""
		logging.basicConfig(filename=self._FILE_NAME, filemode=self._FILE_MODE, format=self._FORMAT, level=logging.WARNING)
		logging.warning(Message)

	def _info(self, Message):
		"""This method is used to create a log for info type.
		"""
		logging.basicConfig(filename=self._FILE_NAME, filemode=self._FILE_MODE, format=self._FORMAT, level=logging.INFO)
		logging.info(Message)

	def _error(self, Message):
		"""This method is used to create a log for error type.
		"""
		logging.basicConfig(filename=self._FILE_NAME, filemode=self._FILE_MODE, format=self._FORMAT, level=logging.ERROR)
		logging.error(Message)




