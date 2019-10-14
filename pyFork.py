"""---"""

import logger
import pandas
import re
import time
import argparse
import pyFork

#Magic Methods
__version__ = '1.0'

__author__ = ("Haci Emre Dasgin <haci.dasgin@gmail.com>")

__all__ = []


class TestCSV():
	"""-"""

	#overview messages
	_overview_msg = list()
	_passed = 0
	_failed = 0





	_logger = logger.Logger();

	_csv_file_name = "";
	_json_file_name = "";
	_data_frame = pandas.DataFrame();
	_mappng_frame = pandas.DataFrame();

	_found_bugs = list()

	_isinteger_regex = "^\\d+$";
	_isnegativeinteger_regex = "^\\-\\d+$";
	_isdouble_regex = "^\\d+[,.]+\\d+$";
	_isnegativedouble_regex = "^\\-\\d+[,.]+\\d+$";
	_isalphanumeric_regex = "^[A-Za-z0-9]+$";
	_isalphabetic_regex = "^[A-Za-z]+$";
	_isspace_regex = "^\\s+$";

	def __init__(self):
		"""Set mandatory input.
		"""
		pass

	@classmethod
	def _read_csv(cls) -> str:
		"""-"""
		try:
			TestCSV._data_frame = pandas.read_csv(TestCSV._csv_file_name);
			TestCSV._logger._info("CSV file '{}' is successfully loaded.".format(TestCSV._csv_file_name));
			TestCSV._data_frame = TestCSV._data_frame.applymap(str);
			TestCSV._logger._info("All data type is converted to 'string' data type.");
			return "0";
		except Exception as e:
			TestCSV._logger._error("Error occurred! in '_read_csv' -> "+str(e))
			return "1";
		pass

	@classmethod
	def _read_json(cls) -> str:
		"""-"""
		try:
			TestCSV._mapping_frame = pandas.read_json(TestCSV._json_file_name);
			TestCSV._logger._info("JSON file '{}' is successfully loaded.".format(TestCSV._json_file_name));
			return "0";
		except Exception as e:
			TestCSV._logger._error("Error occurred! in '_read_json' -> "+str(e))
			return "1";
		pass

	@classmethod
	def _case_iteration(cls) -> str:
		"""-"""
		try:
			for itr_index in range(len(TestCSV._mapping_frame["case"])):
				if TestCSV._mapping_frame["type"][itr_index].upper() == "ISINTEGER":
					TestCSV._isinteger(TestCSV._mapping_frame["column"][itr_index])
				elif TestCSV._mapping_frame["type"][itr_index].upper() == "ISNEGATIVEINTEGER":
					TestCSV._isnegativeinteger(TestCSV._mapping_frame["column"][itr_index])
				elif TestCSV._mapping_frame["type"][itr_index].upper() == "ISDOUBLE":
					TestCSV._isdouble(TestCSV._mapping_frame["column"][itr_index])
				elif TestCSV._mapping_frame["type"][itr_index].upper() == "ISNEGATIVEDOUBLE":
					TestCSV._isnegativedouble(TestCSV._mapping_frame["column"][itr_index])
				elif TestCSV._mapping_frame["type"][itr_index].upper() == "ISNULL":
					TestCSV._isnull(TestCSV._mapping_frame["column"][itr_index])
				elif TestCSV._mapping_frame["type"][itr_index].upper() == "ISNOTNULL":
					TestCSV._isnotnull(TestCSV._mapping_frame["column"][itr_index])
				elif TestCSV._mapping_frame["type"][itr_index].upper() == "ISALPHANUMERIC":
					TestCSV._isalphanumeric(TestCSV._mapping_frame["column"][itr_index])
				elif TestCSV._mapping_frame["type"][itr_index].upper() == "ISALPHABETIC":
					TestCSV._isalphabetic(TestCSV._mapping_frame["column"][itr_index])
				elif TestCSV._mapping_frame["type"][itr_index].upper() == "ISSPACE":
					TestCSV._isspace(TestCSV._mapping_frame["column"][itr_index])
				elif TestCSV._mapping_frame["type"][itr_index].upper() == "ISREGEX":
					TestCSV._isregex(TestCSV._mapping_frame["column"][itr_index],TestCSV._mapping_frame["arg1"][itr_index])
				elif TestCSV._mapping_frame["type"][itr_index].upper() == "ISLESSTHAN":
					TestCSV._islessthan(TestCSV._mapping_frame["column"][itr_index],TestCSV._mapping_frame["arg1"][itr_index])
				elif TestCSV._mapping_frame["type"][itr_index].upper() == "ISGREATERTHAN":
					TestCSV._isgreaterthan(TestCSV._mapping_frame["column"][itr_index],TestCSV._mapping_frame["arg1"][itr_index])
				elif TestCSV._mapping_frame["type"][itr_index].upper() == "ISLESSTHANOREQUALSTO":
					TestCSV._islessthanorequalsto(TestCSV._mapping_frame["column"][itr_index],TestCSV._mapping_frame["arg1"][itr_index])
				elif TestCSV._mapping_frame["type"][itr_index].upper() == "ISGREATERTHANOREQUALSTO":
					TestCSV._isgreaterthanorequalsto(TestCSV._mapping_frame["column"][itr_index],TestCSV._mapping_frame["arg1"][itr_index])
				elif TestCSV._mapping_frame["type"][itr_index].upper() == "ISINBETWEEN":
					TestCSV._isinbetween(TestCSV._mapping_frame["column"][itr_index],TestCSV._mapping_frame["arg1"][itr_index],TestCSV._mapping_frame["arg2"][itr_index])
				elif TestCSV._mapping_frame["type"][itr_index].upper() == "ISINBETWEENOREQUALSTO":
					TestCSV._isinbetweenorequalsto(TestCSV._mapping_frame["column"][itr_index],TestCSV._mapping_frame["arg1"][itr_index],TestCSV._mapping_frame["arg2"][itr_index])
				elif TestCSV._mapping_frame["type"][itr_index].upper() == "ISMAXLENGTH":
					TestCSV._ismaxlength(TestCSV._mapping_frame["column"][itr_index],TestCSV._mapping_frame["arg1"][itr_index])	
				elif TestCSV._mapping_frame["type"][itr_index].upper() == "ISMINLENGTH":
					TestCSV._isminlenght(TestCSV._mapping_frame["column"][itr_index],TestCSV._mapping_frame["arg1"][itr_index])
				elif TestCSV._mapping_frame["type"][itr_index].upper() == "ISEXACTLENGTH":
					TestCSV._isexactlength(TestCSV._mapping_frame["column"][itr_index],TestCSV._mapping_frame["arg1"][itr_index])
				elif TestCSV._mapping_frame["type"][itr_index].upper() == "ISLENGTHINBETWEEN":
					TestCSV._islenghtinbetween(TestCSV._mapping_frame["column"][itr_index],TestCSV._mapping_frame["arg1"][itr_index],TestCSV._mapping_frame["arg2"][itr_index])
				elif TestCSV._mapping_frame["type"][itr_index].upper() == "ISLENGTHINBETWEENOREQUALSTO":
					TestCSV._islenghtinbetweenorequalsto(TestCSV._mapping_frame["column"][itr_index],TestCSV._mapping_frame["arg1"][itr_index],TestCSV._mapping_frame["arg2"][itr_index])
				elif TestCSV._mapping_frame["type"][itr_index].upper() == "ISVALUERANGE":
					TestCSV._isvaluerange(TestCSV._mapping_frame["column"][itr_index],TestCSV._mapping_frame["arg1"][itr_index])
				elif TestCSV._mapping_frame["type"][itr_index].upper() == "ISUNIQUE":
					TestCSV._isunique(TestCSV._mapping_frame["column"][itr_index])
				else:
					pass
				TestCSV._logger._info("Case '{}' iteration is successfully finished.".format(itr_index+1))
				

			TestCSV._logger._info("All case iterations are successfully finished.")
			return "0"
		except Exception as e:
			TestCSV._logger._error("Error occurred! in '_case_iteration' -> "+str(e))
			return "1"
		pass

	@classmethod
	def _isinteger(cls, column_name) -> str:
		"""-"""
		try:
			buggy_column_name = "";
			buggy_row_data = "";
			for itr_index in range(len(TestCSV._data_frame)):
				bug_store = [];
				if len(re.findall(TestCSV._isinteger_regex, TestCSV._data_frame[column_name][itr_index])) == 1:
					TestCSV._passed =+ 1; 
				else:
					TestCSV._failed =+ 1; 
					buggy_column_name = column_name;
					bug_store.append(buggy_column_name)
					buggy_column_name = itr_index;
					bug_store.append(buggy_column_name)
					buggy_row_data =TestCSV._data_frame[column_name][itr_index];
					bug_store.append(buggy_row_data)
					TestCSV._found_bugs.append(bug_store)

			TestCSV._logger._info("IsInteger check is complated for column '{}'".format(column_name))
			return "0"
		except Exception as e:
			TestCSV._logger._error("Error occurred! in '_isinteger' -> "+str(e))
			return "1"
		pass

	@classmethod
	def _isnegativeinteger(cls, column_name) -> str:
		"""-"""
		try:
			buggy_column_name = "";
			buggy_row_data = "";
			for itr_index in range(len(TestCSV._data_frame)):
				bug_store = [];
				if len(re.findall(TestCSV._isnegativeinteger_regex, TestCSV._data_frame[column_name][itr_index])) == 1:
					TestCSV._passed =+ 1; 
				else:
					TestCSV._failed =+ 1; 
					buggy_column_name = column_name;
					bug_store.append(buggy_column_name)
					buggy_column_name = itr_index;
					bug_store.append(buggy_column_name)
					buggy_row_data =TestCSV._data_frame[column_name][itr_index];
					bug_store.append(buggy_row_data)
					TestCSV._found_bugs.append(bug_store)

			TestCSV._logger._info("IsNegativeInteger check is complated for column '{}'".format(column_name))
			return "0"
		except Exception as e:
			TestCSV._logger._error("Error occurred! in '_isnegativeinteger' -> "+str(e))
			return "1"
		pass
	@classmethod
	def _isdouble(cls, column_name) -> str:
		"""-"""
		try:
			buggy_column_name = "";
			buggy_row_data = "";
			for itr_index in range(len(TestCSV._data_frame)):
				bug_store = [];
				if len(re.findall(TestCSV._isdouble_regex, TestCSV._data_frame[column_name][itr_index])) == 1:
					TestCSV._passed =+ 1; 
				else:
					TestCSV._failed =+ 1; 
					buggy_column_name = column_name;
					bug_store.append(buggy_column_name)
					buggy_column_name = itr_index;
					bug_store.append(buggy_column_name)
					buggy_row_data =TestCSV._data_frame[column_name][itr_index];
					bug_store.append(buggy_row_data)
					TestCSV._found_bugs.append(bug_store)

			TestCSV._logger._info("IsDouble check is complated for column '{}'".format(column_name))
			return "0"
		except Exception as e:
			TestCSV._logger._error("Error occurred! in '_isdouble' -> "+str(e))
			return "1"
		pass

	@classmethod
	def _isnegativedouble(cls, column_name) -> str:
		"""-"""
		try:
			buggy_column_name = "";
			buggy_row_data = "";
			for itr_index in range(len(TestCSV._data_frame)):
				bug_store = [];
				if len(re.findall(TestCSV._isnegativedouble_regex, TestCSV._data_frame[column_name][itr_index])) == 1:
					TestCSV._passed =+ 1; 
				else:
					TestCSV._failed =+ 1; 
					buggy_column_name = column_name;
					bug_store.append(buggy_column_name)
					buggy_column_name = itr_index;
					bug_store.append(buggy_column_name)
					buggy_row_data =TestCSV._data_frame[column_name][itr_index];
					bug_store.append(buggy_row_data)
					TestCSV._found_bugs.append(bug_store)

			TestCSV._logger._info("IsNegativeDouble check is complated for column '{}'".format(column_name))
			return "0"
		except Exception as e:
			TestCSV._logger._error("Error occurred! in '_isnegativedouble' -> "+str(e))
			return "1"
		pass


	@classmethod
	def _isnull(cls, column_name) -> str:
		"""-"""
		try:
			buggy_column_name = "";
			buggy_row_data = "";
			for itr_index in range(len(TestCSV._data_frame)):
				bug_store = [];
				if TestCSV._data_frame[column_name][itr_index] == 'nan':
					TestCSV._passed =+ 1; 
				else:
					TestCSV._failed =+ 1; 
					buggy_column_name = column_name
					bug_store.append(buggy_column_name)
					buggy_column_name = itr_index;
					bug_store.append(buggy_column_name)
					buggy_row_data =TestCSV._data_frame[column_name][itr_index]
					bug_store.append(buggy_row_data)
					TestCSV._found_bugs.append(bug_store)

			TestCSV._logger._info("IsNull check is complated for column '{}'".format(column_name))
			return "0"
		except Exception as e:
			TestCSV._logger._error("Error occurred! in '_isnull' -> "+str(e))
			return "1"
		pass

	@classmethod
	def _isnotnull(cls, column_name) -> str:
		"""-"""
		try:
			buggy_column_name = "";
			buggy_row_data = "";
			for itr_index in range(len(TestCSV._data_frame)):
				bug_store = [];
				if TestCSV._data_frame[column_name][itr_index] != 'nan':
					TestCSV._passed =+ 1; 
				else:
					TestCSV._failed =+ 1; 
					buggy_column_name = column_name
					bug_store.append(buggy_column_name)
					buggy_column_name = itr_index;
					bug_store.append(buggy_column_name)
					buggy_row_data = "NULL"
					bug_store.append(buggy_row_data)
					TestCSV._found_bugs.append(bug_store)

			TestCSV._logger._info("IsNotNull check is complated for column '{}'".format(column_name))
			return "0"
		except Exception as e:
			TestCSV._logger._error("Error occurred! in '_isnotnull' -> "+str(e))
			return "1"
		pass


	@classmethod
	def _isalphanumeric(cls, column_name) -> str:
		"""-"""
		try:
			buggy_column_name = "";
			buggy_row_data = "";
			for itr_index in range(len(TestCSV._data_frame)):
				bug_store = [];
				if len(re.findall(TestCSV._isalphanumeric_regex, TestCSV._data_frame[column_name][itr_index])) == 1:
					TestCSV._passed =+ 1; 
				else:
					TestCSV._failed =+ 1; 
					buggy_column_name = column_name;
					bug_store.append(buggy_column_name)
					buggy_column_name = itr_index;
					bug_store.append(buggy_column_name)
					buggy_row_data = TestCSV._data_frame[column_name][itr_index];
					bug_store.append(buggy_row_data)
					TestCSV._found_bugs.append(bug_store)

			TestCSV._logger._info("IsAlphaNumeric check is complated for column '{}'".format(column_name))
			return "0"
		except Exception as e:
			TestCSV._logger._error("Error occurred! in '_isalphanumeric' -> "+str(e))
			return "1"
		pass

	@classmethod
	def _isalphabetic(cls, column_name) -> str:
		"""-"""
		try:
			buggy_column_name = "";
			buggy_row_data = "";
			for itr_index in range(len(TestCSV._data_frame)):
				bug_store = [];
				if len(re.findall(TestCSV._isalphabetic_regex, TestCSV._data_frame[column_name][itr_index])) == 1:
					TestCSV._passed =+ 1; 
				else:
					TestCSV._failed =+ 1; 
					buggy_column_name = column_name;
					bug_store.append(buggy_column_name)
					buggy_column_name = itr_index;
					bug_store.append(buggy_column_name)
					buggy_row_data = TestCSV._data_frame[column_name][itr_index];
					bug_store.append(buggy_row_data)
					TestCSV._found_bugs.append(bug_store)

			TestCSV._logger._info("IsAlphabetic check is complated for column '{}'".format(column_name))
			return "0"
		except Exception as e:
			TestCSV._logger._error("Error occurred! in '_isalphabetic' -> "+str(e))
			return "1"
		pass


	@classmethod
	def _isspace(cls, column_name) -> str:
		"""-"""
		try:
			buggy_column_name = "";
			buggy_row_data = "";
			for itr_index in range(len(TestCSV._data_frame)):
				bug_store = [];
				if len(re.findall(TestCSV._isspace_regex, TestCSV._data_frame[column_name][itr_index])) == 1:
					TestCSV._passed =+ 1; 
				else:
					TestCSV._failed =+ 1; 
					buggy_column_name = column_name;
					bug_store.append(buggy_column_name)
					buggy_column_name = itr_index;
					bug_store.append(buggy_column_name)
					buggy_row_data = TestCSV._data_frame[column_name][itr_index];
					bug_store.append(buggy_row_data)
					TestCSV._found_bugs.append(bug_store)

			TestCSV._logger._info("IsSpace check is complated for column '{}'".format(column_name))
			return "0"
		except Exception as e:
			TestCSV._logger._error("Error occurred! in '_isspace' -> "+str(e))
			return "1"
		pass


	@classmethod
	def _isregex(cls, column_name, arg1) -> str:
		"""-"""
		try:
			buggy_column_name = "";
			buggy_row_data = "";
			for itr_index in range(len(TestCSV._data_frame)):
				bug_store = [];
				if len(re.findall(arg1, TestCSV._data_frame[column_name][itr_index])) == 1:
					TestCSV._passed =+ 1; 
				else:
					TestCSV._failed =+ 1; 
					buggy_column_name = column_name;
					bug_store.append(buggy_column_name)
					buggy_column_name = itr_index;
					bug_store.append(buggy_column_name)
					buggy_row_data = TestCSV._data_frame[column_name][itr_index];
					bug_store.append(buggy_row_data)
					TestCSV._found_bugs.append(bug_store)

			TestCSV._logger._info("IsRegex check is complated for column '{}'".format(column_name))
			return "0"
		except Exception as e:
			TestCSV._logger._error("Error occurred! in '_isregex' -> "+str(e))
			return "1"
		pass


	@classmethod
	def is_value_numeric_at_all(cls, value):
		try:
			int(value)
			return True
		except ValueError:
			return  False

	@classmethod
	def _islessthan(cls, column_name, arg1) -> str:
		"""-"""
		try:
			buggy_column_name = "";
			buggy_row_data = "";
			for itr_index in range(len(TestCSV._data_frame)):
				bug_store = [];
				if TestCSV.is_value_numeric_at_all(TestCSV._data_frame[column_name][itr_index]):
					if int(TestCSV._data_frame[column_name][itr_index]) < int(arg1):
						TestCSV._passed += 1; 
					else:
						TestCSV._failed += 1; 
						buggy_column_name = column_name;
						bug_store.append(buggy_column_name)
						buggy_column_name = itr_index;
						bug_store.append(buggy_column_name)
						buggy_row_data = TestCSV._data_frame[column_name][itr_index];
						bug_store.append(buggy_row_data)
						TestCSV._found_bugs.append(bug_store)
				else:
					TestCSV._failed += 1; 
					buggy_column_name = column_name;
					bug_store.append(buggy_column_name)
					buggy_column_name = itr_index;
					bug_store.append(buggy_column_name)
					buggy_row_data = TestCSV._data_frame[column_name][itr_index];
					bug_store.append(buggy_row_data)
					TestCSV._found_bugs.append(bug_store)

			TestCSV._logger._info("IsLessThan check is complated for column '{}'".format(column_name))
			return "0"
		except Exception as e:
			TestCSV._logger._error("Error occurred! in '_islessthan' -> "+str(e))
			return "1"
		pass


	@classmethod
	def _isgreaterthan(cls, column_name, arg1) -> str:
		"""-"""
		try:
			buggy_column_name = "";
			buggy_row_data = "";
			for itr_index in range(len(TestCSV._data_frame)):
				bug_store = [];
				if TestCSV.is_value_numeric_at_all(TestCSV._data_frame[column_name][itr_index]):
					if int(TestCSV._data_frame[column_name][itr_index]) > int(arg1):
						TestCSV._passed += 1; 
					else:
						TestCSV._failed += 1; 
						buggy_column_name = column_name;
						bug_store.append(buggy_column_name)
						buggy_column_name = itr_index;
						bug_store.append(buggy_column_name)
						buggy_row_data = TestCSV._data_frame[column_name][itr_index];
						bug_store.append(buggy_row_data)
						TestCSV._found_bugs.append(bug_store)
				else:
					TestCSV._failed += 1; 
					buggy_column_name = column_name;
					bug_store.append(buggy_column_name)
					buggy_column_name = itr_index;
					bug_store.append(buggy_column_name)
					buggy_row_data = TestCSV._data_frame[column_name][itr_index];
					bug_store.append(buggy_row_data)
					TestCSV._found_bugs.append(bug_store)

			TestCSV._logger._info("IsGreaterThan check is complated for column '{}'".format(column_name))
			return "0"
		except Exception as e:
			TestCSV._logger._error("Error occurred! in '_isgreaterthan' -> "+str(e))
			return "1"
		pass

	@classmethod
	def _islessthanorequalsto(cls, column_name, arg1) -> str:
		"""-"""
		try:
			buggy_column_name = "";
			buggy_row_data = "";
			for itr_index in range(len(TestCSV._data_frame)):
				bug_store = [];
				if TestCSV.is_value_numeric_at_all(TestCSV._data_frame[column_name][itr_index]):
					if int(TestCSV._data_frame[column_name][itr_index]) <= int(arg1):
						TestCSV._passed += 1; 
					else:
						TestCSV._failed += 1; 
						buggy_column_name = column_name;
						bug_store.append(buggy_column_name)
						buggy_column_name = itr_index;
						bug_store.append(buggy_column_name)
						buggy_row_data = TestCSV._data_frame[column_name][itr_index];
						bug_store.append(buggy_row_data)
						TestCSV._found_bugs.append(bug_store)
				else:
					TestCSV._failed += 1; 
					buggy_column_name = column_name;
					bug_store.append(buggy_column_name)
					buggy_column_name = itr_index;
					bug_store.append(buggy_column_name)
					buggy_row_data = TestCSV._data_frame[column_name][itr_index];
					bug_store.append(buggy_row_data)
					TestCSV._found_bugs.append(bug_store)

			TestCSV._logger._info("IsLessThanOrEqualsTo check is complated for column '{}'".format(column_name))
			return "0"
		except Exception as e:
			TestCSV._logger._error("Error occurred! in '_islessthanorequalsto' -> "+str(e))
			return "1"
		pass


	@classmethod
	def _isgreaterthanorequalsto(cls, column_name, arg1) -> str:
		"""-"""
		try:
			buggy_column_name = "";
			buggy_row_data = "";
			for itr_index in range(len(TestCSV._data_frame)):
				bug_store = [];
				if TestCSV.is_value_numeric_at_all(TestCSV._data_frame[column_name][itr_index]):
					if int(TestCSV._data_frame[column_name][itr_index]) >= int(arg1):
						TestCSV._passed += 1; 
					else:
						TestCSV._failed += 1; 
						buggy_column_name = column_name;
						bug_store.append(buggy_column_name)
						buggy_column_name = itr_index;
						bug_store.append(buggy_column_name)
						buggy_row_data = TestCSV._data_frame[column_name][itr_index];
						bug_store.append(buggy_row_data)
						TestCSV._found_bugs.append(bug_store)
				else:
					TestCSV._failed += 1; 
					buggy_column_name = column_name;
					bug_store.append(buggy_column_name)
					buggy_column_name = itr_index;
					bug_store.append(buggy_column_name)
					buggy_row_data = TestCSV._data_frame[column_name][itr_index];
					bug_store.append(buggy_row_data)
					TestCSV._found_bugs.append(bug_store)

			TestCSV._logger._info("IsGreaterThanOrEqualsTo check is complated for column '{}'".format(column_name))
			return "0"
		except Exception as e:
			TestCSV._logger._error("Error occurred! in '_isgreaterthanorequalsto' -> "+str(e))
			return "1"
		pass


	@classmethod
	def _isinbetween(cls, column_name, arg1, arg2) -> str:
		"""-"""
		try:
			buggy_column_name = "";
			buggy_row_data = "";
			for itr_index in range(len(TestCSV._data_frame)):
				bug_store = [];
				if TestCSV.is_value_numeric_at_all(TestCSV._data_frame[column_name][itr_index]):
					if int(TestCSV._data_frame[column_name][itr_index]) > int(arg1) and int(TestCSV._data_frame[column_name][itr_index]) < int(arg2) :
						TestCSV._passed += 1; 
					else:
						TestCSV._failed += 1; 
						buggy_column_name = column_name;
						bug_store.append(buggy_column_name)
						buggy_column_name = itr_index;
						bug_store.append(buggy_column_name)
						buggy_row_data = TestCSV._data_frame[column_name][itr_index];
						bug_store.append(buggy_row_data)
						TestCSV._found_bugs.append(bug_store)
				else:
					TestCSV._failed += 1; 
					buggy_column_name = column_name;
					bug_store.append(buggy_column_name)
					buggy_column_name = itr_index;
					bug_store.append(buggy_column_name)
					buggy_row_data = TestCSV._data_frame[column_name][itr_index];
					bug_store.append(buggy_row_data)
					TestCSV._found_bugs.append(bug_store)

			TestCSV._logger._info("IsInBetween check is complated for column '{}'".format(column_name))
			return "0"
		except Exception as e:
			TestCSV._logger._error("Error occurred! in '_isinbetween' -> "+str(e))
			return "1"
		pass


	@classmethod
	def _isinbetweenorequalsto(cls, column_name, arg1, arg2) -> str:
		"""-"""
		try:
			buggy_column_name = "";
			buggy_row_data = "";
			for itr_index in range(len(TestCSV._data_frame)):
				bug_store = [];
				if TestCSV.is_value_numeric_at_all(TestCSV._data_frame[column_name][itr_index]):
					if int(TestCSV._data_frame[column_name][itr_index]) >= int(arg1) and int(TestCSV._data_frame[column_name][itr_index]) <= int(arg2) :
						TestCSV._passed += 1; 
					else:
						TestCSV._failed += 1; 
						buggy_column_name = column_name;
						bug_store.append(buggy_column_name)
						buggy_column_name = itr_index;
						bug_store.append(buggy_column_name)
						buggy_row_data = TestCSV._data_frame[column_name][itr_index];
						bug_store.append(buggy_row_data)
						TestCSV._found_bugs.append(bug_store)
				else:
					TestCSV._failed += 1; 
					buggy_column_name = column_name;
					bug_store.append(buggy_column_name)
					buggy_column_name = itr_index;
					bug_store.append(buggy_column_name)
					buggy_row_data = TestCSV._data_frame[column_name][itr_index];
					bug_store.append(buggy_row_data)
					TestCSV._found_bugs.append(bug_store)

			TestCSV._logger._info("IsInBetweenOrEqualsTo check is complated for column '{}'".format(column_name))
			return "0"
		except Exception as e:
			TestCSV._logger._error("Error occurred! in '_isinbetweenorequalsto' -> "+str(e))
			return "1"
		pass


	@classmethod
	def _ismaxlength(cls, column_name, arg1) -> str:
		"""-"""
		try:
			buggy_column_name = "";
			buggy_row_data = "";
			for itr_index in range(len(TestCSV._data_frame)):
				bug_store = [];
				if len(str(TestCSV._data_frame[column_name][itr_index])) < int(arg1):
					TestCSV._passed += 1; 
				else:
					TestCSV._failed += 1; 
					buggy_column_name = column_name;
					bug_store.append(buggy_column_name)
					buggy_column_name = itr_index;
					bug_store.append(buggy_column_name)
					buggy_row_data = TestCSV._data_frame[column_name][itr_index];
					bug_store.append(buggy_row_data)
					TestCSV._found_bugs.append(bug_store)

			TestCSV._logger._info("IsMaxLength check is complated for column '{}'".format(column_name))
			return "0"
		except Exception as e:
			TestCSV._logger._error("Error occurred! in '_ismaxlength' -> "+str(e))
			return "1"
		pass


	@classmethod
	def _isminlenght(cls, column_name, arg1) -> str:
		"""-"""
		try:
			buggy_column_name = "";
			buggy_row_data = "";
			for itr_index in range(len(TestCSV._data_frame)):
				bug_store = [];
				if len(str(TestCSV._data_frame[column_name][itr_index])) > int(arg1):
					TestCSV._passed += 1; 
				else:
					TestCSV._failed += 1; 
					buggy_column_name = column_name;
					bug_store.append(buggy_column_name)
					buggy_column_name = itr_index;
					bug_store.append(buggy_column_name)
					buggy_row_data = TestCSV._data_frame[column_name][itr_index];
					bug_store.append(buggy_row_data)
					TestCSV._found_bugs.append(bug_store)

			TestCSV._logger._info("IsMinLenght check is complated for column '{}'".format(column_name))
			return "0"
		except Exception as e:
			TestCSV._logger._error("Error occurred! in '_isminlenght' -> "+str(e))
			return "1"
		pass

	@classmethod
	def _isexactlength(cls, column_name, arg1) -> str:
		"""-"""
		try:
			buggy_column_name = "";
			buggy_row_data = "";
			for itr_index in range(len(TestCSV._data_frame)):
				bug_store = [];
				if len(str(TestCSV._data_frame[column_name][itr_index])) == int(arg1):
					TestCSV._passed += 1; 
				else:
					TestCSV._failed += 1; 
					buggy_column_name = column_name;
					bug_store.append(buggy_column_name)
					buggy_column_name = itr_index;
					bug_store.append(buggy_column_name)
					buggy_row_data = TestCSV._data_frame[column_name][itr_index];
					bug_store.append(buggy_row_data)
					TestCSV._found_bugs.append(bug_store)

			TestCSV._logger._info("IsExactLength check is complated for column '{}'".format(column_name))
			return "0"
		except Exception as e:
			TestCSV._logger._error("Error occurred! in '_isexactlength' -> "+str(e))
			return "1"
		pass


	@classmethod
	def _islenghtinbetween(cls, column_name, arg1, arg2) -> str:
		"""-"""
		try:
			buggy_column_name = "";
			buggy_row_data = "";
			for itr_index in range(len(TestCSV._data_frame)):
				bug_store = [];
				if len(str(TestCSV._data_frame[column_name][itr_index])) > int(arg1) and len(str(TestCSV._data_frame[column_name][itr_index])) < int(arg2):
					TestCSV._passed += 1; 
				else:
					TestCSV._failed += 1; 
					buggy_column_name = column_name;
					bug_store.append(buggy_column_name)
					buggy_column_name = itr_index;
					bug_store.append(buggy_column_name)
					buggy_row_data = TestCSV._data_frame[column_name][itr_index];
					bug_store.append(buggy_row_data)
					TestCSV._found_bugs.append(bug_store)

			TestCSV._logger._info("IsLenghtInBetween check is complated for column '{}'".format(column_name))
			return "0"
		except Exception as e:
			TestCSV._logger._error("Error occurred! in '_isexactlength' -> "+str(e))
			return "1"
		pass

	@classmethod
	def _islenghtinbetweenorequalsto(cls, column_name, arg1, arg2) -> str:
		"""-"""
		try:
			buggy_column_name = "";
			buggy_row_data = "";
			for itr_index in range(len(TestCSV._data_frame)):
				bug_store = [];
				if len(str(TestCSV._data_frame[column_name][itr_index])) >= int(arg1) and len(str(TestCSV._data_frame[column_name][itr_index])) <= int(arg2):
					TestCSV._passed+= 1; 
				else:
					TestCSV._failed += 1; 
					buggy_column_name = column_name;
					bug_store.append(buggy_column_name)
					buggy_column_name = itr_index;
					bug_store.append(buggy_column_name)
					buggy_row_data = TestCSV._data_frame[column_name][itr_index];
					bug_store.append(buggy_row_data)
					TestCSV._found_bugs.append(bug_store)

			TestCSV._logger._info("IsLenghtInBetweenOrEqualsTo check is complated for column '{}'".format(column_name))
			return "0"
		except Exception as e:
			TestCSV._logger._error("Error occurred! in '_islenghtinbetweenorequalsto' -> "+str(e))
			return "1"
		pass


	@classmethod
	def _isvaluerange(cls, column_name, arg1) -> str:
		"""-"""
		try:
			buggy_column_name = "";
			buggy_row_data = "";
			for itr_index in range(len(TestCSV._data_frame)):
				bug_store = [];
				if len(re.findall("^"+arg1+"$", TestCSV._data_frame[column_name][itr_index])) == 1:
					TestCSV._passed+= 1; 
				else:
					TestCSV._failed+= 1; 
					buggy_column_name = column_name;
					bug_store.append(buggy_column_name)
					buggy_column_name = itr_index;
					bug_store.append(buggy_column_name)
					buggy_row_data = TestCSV._data_frame[column_name][itr_index];
					bug_store.append(buggy_row_data)
					TestCSV._found_bugs.append(bug_store)

			TestCSV._logger._info("IsValueRange check is complated for column '{}'".format(column_name))
			return "0"
		except Exception as e:
			TestCSV._logger._error("Error occurred! in '_isvaluerange' -> "+str(e))
			return "1"
		pass

	@classmethod
	def _isunique(cls, column_name) -> str:
		"""-"""
		try:
			buggy_column_name = "";
			buggy_row_data = "";

			all_data = list(TestCSV._data_frame[column_name])
			for itr_index in range(len(all_data)):
				bug_store = [];
				if all_data.count(all_data[itr_index]) == 1:
					TestCSV._passed += 1; 
				else:
					TestCSV._failed += 1; 
					buggy_column_name = column_name;
					bug_store.append(buggy_column_name)
					buggy_column_name = itr_index;
					bug_store.append(buggy_column_name)
					buggy_row_data = all_data[itr_index];
					bug_store.append(buggy_row_data)
					TestCSV._found_bugs.append(bug_store)					


			TestCSV._logger._info("IsUnique check is complated for column '{}'".format(column_name))
			return "0"
		except Exception as e:
			TestCSV._logger._error("Error occurred! in '_isunique' -> "+str(e))
			return "1"
		pass


#Reporting part!

	@classmethod
	def _report_overview_table(cls) -> str:
		"""-"""
		try:
			
			overview_table = """  <tr id="t01"><td id="t01"><b>Test File:</b></td><td id="t01"><center>{}</center></td></tr><tr id="t01"><td id="t01"><b>Test Date and Time:</b></td><td id="t01"><center>{}</center></td></tr><tr id="t01"><td id="t01"><b>Total Column(s):</b></td><td id="t01"><center>{}</center></td></tr><tr id="t01"><td id="t01"><b>Total Row(s):</b></td><td id="t01"><center>{}</center></td></tr><tr id="t01"><td id="t01"><b>Test(s) Passed:</b></td><td id="t01"><center>{}</center></td></tr><tr id="t01"><td id="t01"><b>Test(s) Failed:</b></td><td id="t01"><center>{}</center></td></tr>""".format(str(TestCSV._csv_file_name),str(time.strftime("%Y/%m/%d-%H:%M:%S", time.localtime())),str(len(TestCSV._data_frame.columns)),str(len(TestCSV._data_frame)-1),str(TestCSV._passed),str(TestCSV._failed))

			TestCSV._logger._info("Overview table creation is complated for column.")
			return overview_table;
		except Exception as e:
			TestCSV._logger._error("Error occurred! in '_report_overview_table' -> "+str(e))
			return "1"
		pass

	@classmethod
	def _report_overview_chart(cls) -> str:
		"""-"""
		try:
			javascript_chart = """var data = [ [ "Failed", {} ], [ "Passed", {} ], [ "Not executed", 0 ]];var colors = [ "red", "green",  "orange" ];drawPieChart( data, colors, "-Cell Test Result-" ); </script>""".format(TestCSV._failed,TestCSV._passed)

			TestCSV._logger._info("Overview chart creation is complated for column.")
			return javascript_chart
		except Exception as e:
			TestCSV._logger._error("Error occurred! in '_report_overview_chart' -> "+str(e))
			return "1"
		pass

	@classmethod
	def _report_testcases(cls) -> str:
		"""-"""
		try:
			test_cases = ""
			for itr_index in range(len(TestCSV._mapping_frame["case"])):
				test_cases = test_cases + """<tr id="t01"><td id="t01"><center>{}</center></td><td id="t01"><center>{}</center></td><td id="t01"><center>{}</center></td><td id="t01"><center>{}</center></td></tr>""".format(TestCSV._mapping_frame["column"][itr_index],TestCSV._mapping_frame["type"][itr_index],TestCSV._mapping_frame["arg1"][itr_index],TestCSV._mapping_frame["arg2"][itr_index])

			TestCSV._logger._info("Test cases Report creation is complated for column.")
			return test_cases;
		except Exception as e:
			TestCSV._logger._error("Error occurred! in '_report_testcases' -> "+str(e))
			return "1"
		pass


	@classmethod
	def _report_failed(cls) -> str:
		"""-"""
		try:
			failed_tests = "";
			for itr_index in range(len(TestCSV._found_bugs)):
				failed_tests = failed_tests + """<tr id="t01"><td id="t01"><center>{}</center></td><td id="t01"><center>{}</center></td><td id="t01"><center>{}</center></td></tr>""".format(TestCSV._found_bugs[itr_index][0],TestCSV._found_bugs[itr_index][1],TestCSV._found_bugs[itr_index][2])

			TestCSV._logger._info("Failure Report creation is complated for column.")
			return failed_tests;
		except Exception as e:
			TestCSV._logger._error("Error occurred! in '_report_failed' -> "+str(e))
			return "1"
		pass


	@classmethod
	def _html_report_generation(cls) -> str:
		"""-"""
		try:
			part1 = """<!---->
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
* {box-sizing: border-box}
body {font-family: "Lato", sans-serif;}

/* Style the tab */
.tab {
  float: left;
  border: 1px solid #ccc;
  background-color: #f1f1f1;
  width: 10%;
  height: 500px;
}

/* Style the buttons inside the tab */
.tab button {
  display: block;
  background-color: inherit;
  color: black;
  padding: 22px 16px;
  width: 100%;
  border: none;
  outline: none;
  text-align: left;
  cursor: pointer;
  transition: 0.3s;
  font-size: 17px;
}

/* Change background color of buttons on hover */
.tab button:hover {
  background-color: #ddd;
}

/* Create an active/current "tab button" class */
.tab button.active {
  background-color: #ccc;
}

/* Style the tab content */
.tabcontent {
  float: left;
  padding: 0px 12px;
  border: 1px solid #ccc;
  width: 90%;
  border-left: none;
  height: 500px;
}
/*overview style*/


table#t01, th#t01, td#t01 {
  border: 1px solid black;
  border-collapse: collapse;
  width:100%;
}
th#t01, td#t01 {
  padding: 15px;
  text-align: left;
}
table#t01 tr:nth-child(even) {
  background-color: #eee;
}
table#t01 th#t01 {
  background-color: black;
  color: white;
}

/*columns detail*/


/* Style the tab */
.tabi {
  overflow: hidden;
  border: 1px solid #ccc;
  background-color: #f1f1f1;
}

/* Style the buttons inside the tab */
.tabi button {
  background-color: inherit;
  float: left;
  border: none;
  outline: none;
  cursor: pointer;
  padding: 14px 16px;
  transition: 0.3s;
  font-size: 17px;
}

/* Change background color of buttons on hover */
.tabi button:hover {
  background-color: #ddd;
}

/* Create an active/current tablink class */
.tabi button.active {
  background-color: #ccc;
}

/* Style the tab content */
.tabcontenti {
  display: none;
  padding: 6px 12px;
  border: 1px solid #ccc;
  border-top: none;
}
</style>
</head>
<body bgcolor="#d1ccbe">

          
<table>
  <tr>
    <th><img style='display:block; width:100px;height:100px;' id='base64image'                 
       src='data:image/png;base64,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'/></th>
    <th><h1>&nbsp Data Quality Test</h1></th>
  </tr>
</table>

<!--Main menu -->
<div class="tab">
  <button class="tablinks" onclick="openCity(event, 'Overview')" id="defaultOpen" style="color:rgb(255, 153, 0);"><b>Overview</b></button>
  <button class="tablinks" onclick="openCity(event, 'Failures')" style="color:rgb(255, 0, 0);"><b>Failures</b></button>
  <button class="tablinks" onclick="openCity(event, 'Test Cases')" style="color:rgb(12, 85, 201);"><b>Test Cases</b></button>
  
</div>

<!--Overview-->
<div id="Overview" class="tabcontent">
  <h3>Overview</h3>

  <div style="width:50%; float:left;">
  <center>
  <table id="t01">
  <tr id="t01">
    <th id="t01">Statistics</th>
    <th id="t01">Result</th> 
  </tr>





<!---->"""
			
			part2 = TestCSV._report_overview_table();
			part3 = """<!---->






</table>
</center>
</div>

<div style="width:50%; float:right;"><center><div id="chart"><canvas id="test_canvas" width="500" height="500"></canvas></center></div>
</div>




<div id="Failures" class="tabcontent">

    <center>
      <table id="t01">
      <tr id="t01"><th id="t01">Column Name</th><th id="t01">Row Number</th><th id="t01">Failed Data</th></tr>


<!---->"""
			part4 = TestCSV._report_failed();
			part5 = """<!---->
    </table>
    </center>

</div>

<div id="Test Cases" class="tabcontent">
  <center><table id="t01"><tr id="t01"><th id="t01">Column</th><th id="t01">Type</th><th id="t01">Arg1</th><th id="t01">Arg2</th></tr>


<!---->"""
			part6 = TestCSV._report_testcases();
			part7 = """<!---->




</table></center>

</div>


<script>
function openCityi(evt, cityName) {
  var i, tabcontent, tablinks;
  tabcontent = document.getElementsByClassName("tabcontenti");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }
  tablinks = document.getElementsByClassName("tablinksi");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }
  document.getElementById(cityName).style.display = "block";
  evt.currentTarget.className += " active";
}
</script>
   

<script>
function openCity(evt, cityName) {
  var i, tabcontent, tablinks;
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }
  document.getElementById(cityName).style.display = "block";
  evt.currentTarget.className += " active";
}

// Get the element with id="defaultOpen" and click on it
document.getElementById("defaultOpen").click();
</script>


  <script>

function drawPieChart( data, colors, title ){     
var canvas = document.getElementById( "test_canvas" );    
var context = canvas.getContext( "2d" ); 

var dataLength = data.length; 

var total = 0; 

for( var i = 0; i < dataLength; i++ ){        
    total += data[ i ][ 1 ];     
} 
var x = 150;     
var y = 160;     
var radius = 150; 
var startingPoint = 0; 

for( var i = 0; i < dataLength; i++ ){ 
  var percent = data[ i ][ 1 ] * 100 / total; 
  var endPoint = startingPoint + ( 2 / 100 * percent );
context.beginPath();
        context.fillStyle = colors[ i ];       
        context.moveTo( x, y );       
        context.arc( x, y, radius, startingPoint * Math.PI, endPoint * Math.PI );        
        context.fill(); 
        
        
   startingPoint = endPoint; 
   
   
        context.rect( 320, 25 * i+81, 15, 15 ); 
        context.fill();        
        context.fillStyle = "black";  
    context.fillText( data[ i ][ 0 ] + " (" + data[ i ][ 1 ] + ")", 350, 25 * i + 90);    
        }  

    context.font = "35px Arial";     
    context.textAlign = "center";     
    context.fillText( title, 150, 360 );  }"""
			part8 = TestCSV._report_overview_chart();
			part9 = """</body>
</html>"""
			file_name = TestCSV._csv_file_name+str(time.strftime("%Y%m%d%H%M%S", time.localtime()))+".html"
			f = open(file_name,"w")
			f.write(part1+part2+part3+part4+part5+part6+part7+part8+part9)
			f.close()

			TestCSV._logger._info("Report has been generated")
			return "0";
		except Exception as e:
			TestCSV._logger._error("Error occurred! in '_html_report_generation' -> "+str(e))
			return "1"
		pass



	@classmethod
	def class_starter(cls, csv_file_name, json_file_name) -> str:
		"""-"""
		try:

			TestCSV._csv_file_name = csv_file_name;
			TestCSV._read_csv();
			TestCSV._json_file_name = json_file_name;
			TestCSV._read_json();
			TestCSV._case_iteration();
			TestCSV._html_report_generation();

			TestCSV._logger._info("class_starter method is finished")
			return "0"
		except Exception as e:
			TestCSV._logger._error("Error occurred! in 'main' -> "+str(e))
			return "1"
		pass








def main():
	my_parser = argparse.ArgumentParser()

	my_parser.add_argument('--report', type=str, help="Provide your report file, Example: '--report report.csv'")

	my_parser.add_argument('--testcase', type=str, help="Provide your testcase file, Example: '--testcase testcase.json'")

	my_parser.add_argument('--extract', type=str, help="You can extract example testcase or report file, Example: '--extract testcase' or '--extract report'")

	args = my_parser.parse_args()

	run(args)


def run(args):
	if args.extract == "testcase":
		f = open("testcase.json","w")
		f.write("""[{"case":"1","column": "Region","type": "IsNotNull","arg1": null,"arg2": null},{"case":"2","column": "Order Priority","type": "IsValueRange","arg1": "(M|C)","arg2": null}]""")
		f.close()
	elif args.extract == "report":
		f = open("report.csv","w")
		f.write("Region,Country,Item Type,Sales Channel,Order Priority\nAsia,Singapore,Snacks,Online,C\nSub-Saharan Africa,Ethiopia,Cosmetics,Online,M\nAfrica,Tanzania,Cosmetics,Offline,M")
		f.close()
	else:
		test_agent = pyFork.TestCSV()
		test_agent.class_starter(args.report, args.testcase)

if __name__ == '__main__':
	main()