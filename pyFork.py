"""pyFork is for testing data in CSV format"""
#a git connection test

import pandas
import re
import time
import argparse
import pyFork
import logger
import csv
import sqlite3

#Magic Methods
__version__ = '1.0'

__author__ = ("Haci Emre Dasgin <haci.dasgin@gmail.com>")

__all__ = []

class TestCSV():
	"""-"""
	_passed = 0
	_failed = 0

	_logger = logger.Logger();

	_memory_database_creation_flag = 0;
	_file_database_creation_flag = 0;
	_generic_cursor = 0;

	_csv_file_name = "";
	_json_file_name = "";
	_data_frame = pandas.DataFrame();
	_mapping_frame = pandas.DataFrame();
	_csv_header = list()

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
		"""reads csv file and keeps in dataframe"""
		try:
			TestCSV._data_frame = pandas.read_csv(TestCSV._csv_file_name);
			TestCSV._logger._info("CSV file '{}' is successfully loaded.".format(TestCSV._csv_file_name));
			TestCSV._data_frame = TestCSV._data_frame.applymap(str);#changes all data type of dataframe to string
			TestCSV._csv_header = list(TestCSV._data_frame.columns); #get csv header
			TestCSV._data_frame = TestCSV._data_frame.replace(to_replace = "nan", value ="");#converts nan to ""
			TestCSV._logger._info("All data type is converted to 'string' data type.");
			return "0";
		except Exception as e:
			TestCSV._logger._error("Error occurred! in '_read_csv' -> "+str(e))
			return "1";
		pass

	@classmethod
	def _read_json(cls) -> str:
		"""reads json file and keeps in dataframe"""
		try:
			TestCSV._mapping_frame = pandas.read_json(TestCSV._json_file_name);
			TestCSV._logger._info("JSON file '{}' is successfully loaded.".format(TestCSV._json_file_name));
			return "0";
		except Exception as e:
			TestCSV._logger._error("Error occurred! in '_read_json' -> "+str(e))
			return "1";
		pass

	@classmethod
	def _csv_header_check(cls) -> str:
		"""This method checks csv header"""
		try:
			for itr_index in range(len(TestCSV._mapping_frame["case"])):
				if TestCSV._csv_header.count(TestCSV._mapping_frame["column"][itr_index]) == 1:
					pass
				else:
					TestCSV._logger._error("Column '{}' could not be found in '{}' file.".format(TestCSV._mapping_frame["column"][itr_index],TestCSV._csv_file_name));
					print("--File check is failed, Please check the log.")
					return "1";

			TestCSV._logger._info("Header check is finished.");
			return "0";
		except Exception as e:
			TestCSV._logger._error("Error occurred! in '_csv_header_check' -> "+str(e))
			return "1";
		pass


	@classmethod
	def _case_iteration(cls) -> str:
		"""itrates dataframe from json file and parse argument to corresponding function"""
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
				elif TestCSV._mapping_frame["type"][itr_index].upper() == "ISDEPENDENCY":
					TestCSV._isdependency(TestCSV._mapping_frame["column"][itr_index],TestCSV._mapping_frame["arg1"][itr_index],TestCSV._mapping_frame["arg2"][itr_index])
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
	def _collect_failure(cls, colum_name, row_number, test_type, arg1, arg2, data) -> str:
		"""collects failed data in a array"""
		try:
			bug_report_line = list()
			#generates array structure
			bug_report_line.append(colum_name)
			bug_report_line.append(row_number)
			bug_report_line.append(test_type)
			bug_report_line.append(arg1)
			bug_report_line.append(arg2)
			bug_report_line.append(data)
			#keeps in global array
			TestCSV._found_bugs.append(bug_report_line)

			return "0";
		except Exception as e:
			TestCSV._logger._error("Error occurred! in '_collect_failure' -> "+str(e))
			return "1";
		pass

	@classmethod
	def _isinteger(cls, column_name) -> str:
		"""executes _isinteger method"""
		try:
			test_type = "IsInteger";
			for itr_index in range(len(TestCSV._data_frame)):
				bug_store = [];
				if len(re.findall(TestCSV._isinteger_regex, TestCSV._data_frame[column_name][itr_index])) == 1:
					TestCSV._passed += 1; 
				else:
					TestCSV._failed += 1; 
					TestCSV._collect_failure(column_name,itr_index,test_type,TestCSV._isinteger_regex,"null",TestCSV._data_frame[column_name][itr_index])

			TestCSV._logger._info("IsInteger check is completed for column '{}'".format(column_name))
			return "0"
		except Exception as e:
			TestCSV._logger._error("Error occurred! in '_isinteger' -> "+str(e))
			return "1"
		pass

	@classmethod
	def _isnegativeinteger(cls, column_name) -> str:
		"""executes _isnegativeinteger method"""
		try:
			test_type = "IsNegativeInteger";
			for itr_index in range(len(TestCSV._data_frame)):
				bug_store = [];
				if len(re.findall(TestCSV._isnegativeinteger_regex, TestCSV._data_frame[column_name][itr_index])) == 1:
					TestCSV._passed += 1; 
				else:
					TestCSV._failed += 1; 
					TestCSV._collect_failure(column_name,itr_index,test_type,TestCSV._isnegativeinteger_regex,"null",TestCSV._data_frame[column_name][itr_index])

			TestCSV._logger._info("IsNegativeInteger check is completed for column '{}'".format(column_name))
			return "0"
		except Exception as e:
			TestCSV._logger._error("Error occurred! in '_isnegativeinteger' -> "+str(e))
			return "1"
		pass

	@classmethod
	def _isdouble(cls, column_name) -> str:
		"""executes _isdouble method"""
		try:
			test_type = "IsDouble";
			for itr_index in range(len(TestCSV._data_frame)):
				bug_store = [];
				if len(re.findall(TestCSV._isdouble_regex, TestCSV._data_frame[column_name][itr_index])) == 1:
					TestCSV._passed += 1; 
				else:
					TestCSV._failed += 1; 
					TestCSV._collect_failure(column_name,itr_index,test_type,TestCSV._isdouble_regex,"null",TestCSV._data_frame[column_name][itr_index])

			TestCSV._logger._info("IsDouble check is completed for column '{}'".format(column_name))
			return "0"
		except Exception as e:
			TestCSV._logger._error("Error occurred! in '_isdouble' -> "+str(e))
			return "1"
		pass

	@classmethod
	def _isnegativedouble(cls, column_name) -> str:
		"""executes _isnegativedouble method"""
		try:
			test_type = "IsNegativeDouble";
			for itr_index in range(len(TestCSV._data_frame)):
				bug_store = [];
				if len(re.findall(TestCSV._isnegativedouble_regex, TestCSV._data_frame[column_name][itr_index])) == 1:
					TestCSV._passed += 1; 
				else:
					TestCSV._failed += 1; 
					TestCSV._collect_failure(column_name,itr_index,test_type,TestCSV._isnegativedouble_regex,"null",TestCSV._data_frame[column_name][itr_index])

			TestCSV._logger._info("IsNegativeDouble check is completed for column '{}'".format(column_name))
			return "0"
		except Exception as e:
			TestCSV._logger._error("Error occurred! in '_isnegativedouble' -> "+str(e))
			return "1"
		pass

	@classmethod
	def _isnull(cls, column_name) -> str:
		"""executes _isnull method"""
		try:
			test_type = "IsNull";
			for itr_index in range(len(TestCSV._data_frame)):
				bug_store = [];
				if TestCSV._data_frame[column_name][itr_index] == "":
					TestCSV._passed += 1; 
				else:
					TestCSV._failed += 1; 
					TestCSV._collect_failure(column_name,itr_index,test_type,"null","null",TestCSV._data_frame[column_name][itr_index])

			TestCSV._logger._info("IsNull check is completed for column '{}'".format(column_name))
			return "0"
		except Exception as e:
			TestCSV._logger._error("Error occurred! in '_isnull' -> "+str(e))
			return "1"
		pass

	@classmethod
	def _isnotnull(cls, column_name) -> str:
		"""executes _isnotnull method"""
		try:
			test_type = "IsNotNull";
			for itr_index in range(len(TestCSV._data_frame)):
				bug_store = [];
				if TestCSV._data_frame[column_name][itr_index] != "":
					TestCSV._passed += 1; 
				else:
					TestCSV._failed += 1; 
					TestCSV._collect_failure(column_name,itr_index,test_type,"null","null","<null>")

			TestCSV._logger._info("IsNotNull check is completed for column '{}'".format(column_name))
			return "0"
		except Exception as e:
			TestCSV._logger._error("Error occurred! in '_isnotnull' -> "+str(e))
			return "1"
		pass

	@classmethod
	def _isalphanumeric(cls, column_name) -> str:
		"""executes _isalphanumeric method"""
		try:
			test_type = "IsAlphaNumeric";
			for itr_index in range(len(TestCSV._data_frame)):
				bug_store = [];
				if len(re.findall(TestCSV._isalphanumeric_regex, TestCSV._data_frame[column_name][itr_index])) == 1:
					TestCSV._passed += 1; 
				else:
					TestCSV._failed += 1; 
					TestCSV._collect_failure(column_name,itr_index,test_type,TestCSV._isalphanumeric_regex,"null",TestCSV._data_frame[column_name][itr_index])

			TestCSV._logger._info("IsAlphaNumeric check is completed for column '{}'".format(column_name))
			return "0"
		except Exception as e:
			TestCSV._logger._error("Error occurred! in '_isalphanumeric' -> "+str(e))
			return "1"
		pass

	@classmethod
	def _isalphabetic(cls, column_name) -> str:
		"""executes _isalphabetic method"""
		try:
			test_type = "IsAlphabetic";
			for itr_index in range(len(TestCSV._data_frame)):
				bug_store = [];
				if len(re.findall(TestCSV._isalphabetic_regex, TestCSV._data_frame[column_name][itr_index])) == 1:
					TestCSV._passed += 1; 
				else:
					TestCSV._failed += 1; 
					TestCSV._collect_failure(column_name,itr_index,test_type,TestCSV._isalphabetic_regex,"null",TestCSV._data_frame[column_name][itr_index])

			TestCSV._logger._info("IsAlphabetic check is completed for column '{}'".format(column_name))
			return "0"
		except Exception as e:
			TestCSV._logger._error("Error occurred! in '_isalphabetic' -> "+str(e))
			return "1"
		pass

	@classmethod
	def _isspace(cls, column_name) -> str:
		"""executes _isspace method"""
		try:
			test_type = "IsSpace";
			for itr_index in range(len(TestCSV._data_frame)):
				bug_store = [];
				if len(re.findall(TestCSV._isspace_regex, TestCSV._data_frame[column_name][itr_index])) == 1:
					TestCSV._passed += 1; 
				else:
					TestCSV._failed += 1; 
					TestCSV._collect_failure(column_name,itr_index,test_type,TestCSV._isspace_regex,"null",TestCSV._data_frame[column_name][itr_index])

			TestCSV._logger._info("IsSpace check is completed for column '{}'".format(column_name))
			return "0"
		except Exception as e:
			TestCSV._logger._error("Error occurred! in '_isspace' -> "+str(e))
			return "1"
		pass

	@classmethod
	def _isregex(cls, column_name, arg1) -> str:
		"""executes _isregex method"""
		try:
			test_type = "IsRegex";
			for itr_index in range(len(TestCSV._data_frame)):
				bug_store = [];
				if len(re.findall(arg1, TestCSV._data_frame[column_name][itr_index])) == 1:
					TestCSV._passed += 1; 
				else:
					TestCSV._failed += 1; 
					TestCSV._collect_failure(column_name,itr_index,test_type,arg1,"null",TestCSV._data_frame[column_name][itr_index])

			TestCSV._logger._info("IsRegex check is completed for column '{}'".format(column_name))
			return "0"
		except Exception as e:
			TestCSV._logger._error("Error occurred! in '_isregex' -> "+str(e))
			return "1"
		pass

	@classmethod
	def is_value_numeric_at_all(cls, value):
		"""Specil method to check value that is it numeric or not"""
		try:
			int(value)
			return True
		except ValueError:
			return  False

	@classmethod
	def _islessthan(cls, column_name, arg1) -> str:
		"""executes _islessthan method"""
		try:
			test_type = "IsLessThan";
			for itr_index in range(len(TestCSV._data_frame)):
				bug_store = [];
				if TestCSV.is_value_numeric_at_all(TestCSV._data_frame[column_name][itr_index]):
					if int(TestCSV._data_frame[column_name][itr_index]) < int(arg1):
						TestCSV._passed += 1; 
					else:
						TestCSV._failed += 1; 
						TestCSV._collect_failure(column_name,itr_index,test_type,arg1,"null",TestCSV._data_frame[column_name][itr_index])
				else:
					TestCSV._failed += 1; 
					TestCSV._collect_failure(column_name,itr_index,test_type,arg1,"null",TestCSV._data_frame[column_name][itr_index])

			TestCSV._logger._info("IsLessThan check is completed for column '{}'".format(column_name))
			return "0"
		except Exception as e:
			TestCSV._logger._error("Error occurred! in '_islessthan' -> "+str(e))
			return "1"
		pass

	@classmethod
	def _isgreaterthan(cls, column_name, arg1) -> str:
		"""executes _isgreaterthan method"""
		try:
			test_type = "IsGreaterThan";
			for itr_index in range(len(TestCSV._data_frame)):
				bug_store = [];
				if TestCSV.is_value_numeric_at_all(TestCSV._data_frame[column_name][itr_index]):
					if int(TestCSV._data_frame[column_name][itr_index]) > int(arg1):
						TestCSV._passed += 1; 
					else:
						TestCSV._failed += 1; 
						TestCSV._collect_failure(column_name,itr_index,test_type,arg1,"null",TestCSV._data_frame[column_name][itr_index])
				else:
					TestCSV._failed += 1; 
					TestCSV._collect_failure(column_name,itr_index,test_type,arg1,"null",TestCSV._data_frame[column_name][itr_index])
			TestCSV._logger._info("IsGreaterThan check is completed for column '{}'".format(column_name))
			return "0"
		except Exception as e:
			TestCSV._logger._error("Error occurred! in '_isgreaterthan' -> "+str(e))
			return "1"
		pass

	@classmethod
	def _islessthanorequalsto(cls, column_name, arg1) -> str:
		"""executes _islessthanorequalsto method"""
		try:
			test_type = "IsLessThanOrEqualsTo";
			for itr_index in range(len(TestCSV._data_frame)):
				bug_store = [];
				if TestCSV.is_value_numeric_at_all(TestCSV._data_frame[column_name][itr_index]):
					if int(TestCSV._data_frame[column_name][itr_index]) <= int(arg1):
						TestCSV._passed += 1; 
					else:
						TestCSV._failed += 1; 
						TestCSV._collect_failure(column_name,itr_index,test_type,arg1,"null",TestCSV._data_frame[column_name][itr_index])
				else:
					TestCSV._failed += 1; 
					TestCSV._collect_failure(column_name,itr_index,test_type,arg1,"null",TestCSV._data_frame[column_name][itr_index])

			TestCSV._logger._info("IsLessThanOrEqualsTo check is completed for column '{}'".format(column_name))
			return "0"
		except Exception as e:
			TestCSV._logger._error("Error occurred! in '_islessthanorequalsto' -> "+str(e))
			return "1"
		pass

	@classmethod
	def _isgreaterthanorequalsto(cls, column_name, arg1) -> str:
		"""executes _isgreaterthanorequalsto method"""
		try:
			test_type = "IsGreaterThanOrEqualsTo";
			for itr_index in range(len(TestCSV._data_frame)):
				bug_store = [];
				if TestCSV.is_value_numeric_at_all(TestCSV._data_frame[column_name][itr_index]):
					if int(TestCSV._data_frame[column_name][itr_index]) >= int(arg1):
						TestCSV._passed += 1; 
					else:
						TestCSV._failed += 1; 
						TestCSV._collect_failure(column_name,itr_index,test_type,arg1,"null",TestCSV._data_frame[column_name][itr_index])
				else:
					TestCSV._failed += 1; 
					TestCSV._collect_failure(column_name,itr_index,test_type,arg1,"null",TestCSV._data_frame[column_name][itr_index])

			TestCSV._logger._info("IsGreaterThanOrEqualsTo check is completed for column '{}'".format(column_name))
			return "0"
		except Exception as e:
			TestCSV._logger._error("Error occurred! in '_isgreaterthanorequalsto' -> "+str(e))
			return "1"
		pass

	@classmethod
	def _isinbetween(cls, column_name, arg1, arg2) -> str:
		"""executes _isinbetween method"""
		try:
			test_type = "IsInBetween";
			for itr_index in range(len(TestCSV._data_frame)):
				bug_store = [];
				if TestCSV.is_value_numeric_at_all(TestCSV._data_frame[column_name][itr_index]):
					if int(TestCSV._data_frame[column_name][itr_index]) > int(arg1) and int(TestCSV._data_frame[column_name][itr_index]) < int(arg2) :
						TestCSV._passed += 1; 
					else:
						TestCSV._failed += 1; 
						TestCSV._collect_failure(column_name,itr_index,test_type,arg1,arg2,TestCSV._data_frame[column_name][itr_index])
				else:
					TestCSV._failed += 1; 
					TestCSV._collect_failure(column_name,itr_index,test_type,arg1,arg2,TestCSV._data_frame[column_name][itr_index])

			TestCSV._logger._info("IsInBetween check is completed for column '{}'".format(column_name))
			return "0"
		except Exception as e:
			TestCSV._logger._error("Error occurred! in '_isinbetween' -> "+str(e))
			return "1"
		pass

	@classmethod
	def _isinbetweenorequalsto(cls, column_name, arg1, arg2) -> str:
		"""executes _isinbetweenorequalsto method"""
		try:
			test_type = "IsInBetweenOrEqualsTo";
			for itr_index in range(len(TestCSV._data_frame)):
				bug_store = [];
				if TestCSV.is_value_numeric_at_all(TestCSV._data_frame[column_name][itr_index]):
					if int(TestCSV._data_frame[column_name][itr_index]) >= int(arg1) and int(TestCSV._data_frame[column_name][itr_index]) <= int(arg2) :
						TestCSV._passed += 1; 
					else:
						TestCSV._failed += 1; 
						TestCSV._collect_failure(column_name,itr_index,test_type,arg1,arg2,TestCSV._data_frame[column_name][itr_index])
				else:
					TestCSV._failed += 1; 
					TestCSV._collect_failure(column_name,itr_index,test_type,arg1,arg2,TestCSV._data_frame[column_name][itr_index])

			TestCSV._logger._info("IsInBetweenOrEqualsTo check is completed for column '{}'".format(column_name))
			return "0"
		except Exception as e:
			TestCSV._logger._error("Error occurred! in '_isinbetweenorequalsto' -> "+str(e))
			return "1"
		pass

	@classmethod
	def _ismaxlength(cls, column_name, arg1) -> str:
		"""executes _ismaxlength method"""
		try:
			test_type = "IsMaxLength";
			for itr_index in range(len(TestCSV._data_frame)):
				bug_store = [];
				if len(str(TestCSV._data_frame[column_name][itr_index])) < int(arg1):
					TestCSV._passed += 1; 
				else:
					TestCSV._failed += 1; 
					TestCSV._collect_failure(column_name,itr_index,test_type,arg1,"null",TestCSV._data_frame[column_name][itr_index])


			TestCSV._logger._info("IsMaxLength check is completed for column '{}'".format(column_name))
			return "0"
		except Exception as e:
			TestCSV._logger._error("Error occurred! in '_ismaxlength' -> "+str(e))
			return "1"
		pass


	@classmethod
	def _isminlenght(cls, column_name, arg1) -> str:
		"""executes _isminlenght method"""
		try:
			test_type = "IsMinLenght";
			for itr_index in range(len(TestCSV._data_frame)):
				bug_store = [];
				if len(str(TestCSV._data_frame[column_name][itr_index])) > int(arg1):
					TestCSV._passed += 1; 
				else:
					TestCSV._failed += 1; 
					TestCSV._collect_failure(column_name,itr_index,test_type,arg1,"null",TestCSV._data_frame[column_name][itr_index])

			TestCSV._logger._info("IsMinLenght check is completed for column '{}'".format(column_name))
			return "0"
		except Exception as e:
			TestCSV._logger._error("Error occurred! in '_isminlenght' -> "+str(e))
			return "1"
		pass

	@classmethod
	def _isexactlength(cls, column_name, arg1) -> str:
		"""executes _isexactlength method"""
		try:
			test_type = "IsExactLength";
			for itr_index in range(len(TestCSV._data_frame)):
				bug_store = [];
				if len(str(TestCSV._data_frame[column_name][itr_index])) == int(arg1):
					TestCSV._passed += 1; 
				else:
					TestCSV._failed += 1; 
					TestCSV._collect_failure(column_name,itr_index,test_type,arg1,"null",TestCSV._data_frame[column_name][itr_index])

			TestCSV._logger._info("IsExactLength check is completed for column '{}'".format(column_name))
			return "0"
		except Exception as e:
			TestCSV._logger._error("Error occurred! in '_isexactlength' -> "+str(e))
			return "1"
		pass


	@classmethod
	def _islenghtinbetween(cls, column_name, arg1, arg2) -> str:
		"""executes _islenghtinbetween method"""
		try:

			test_type = "IsLenghtInBetween";
			for itr_index in range(len(TestCSV._data_frame)):
				bug_store = [];
				if len(str(TestCSV._data_frame[column_name][itr_index])) > int(arg1) and len(str(TestCSV._data_frame[column_name][itr_index])) < int(arg2):
					TestCSV._passed += 1; 
				else:
					TestCSV._failed += 1; 
					TestCSV._collect_failure(column_name,itr_index,test_type,arg1,arg2,TestCSV._data_frame[column_name][itr_index])

			TestCSV._logger._info("IsLenghtInBetween check is completed for column '{}'".format(column_name))
			return "0"
		except Exception as e:
			TestCSV._logger._error("Error occurred! in '_isexactlength' -> "+str(e))
			return "1"
		pass

	@classmethod
	def _islenghtinbetweenorequalsto(cls, column_name, arg1, arg2) -> str:
		"""executes _islenghtinbetweenorequalsto method"""
		try:
			test_type = "IsLenghtInBetweenOrEqualsTo";
			for itr_index in range(len(TestCSV._data_frame)):
				bug_store = [];
				if len(str(TestCSV._data_frame[column_name][itr_index])) >= int(arg1) and len(str(TestCSV._data_frame[column_name][itr_index])) <= int(arg2):
					TestCSV._passed+= 1; 
				else:
					TestCSV._failed += 1; 
					TestCSV._collect_failure(column_name,itr_index,test_type,arg1,arg2,TestCSV._data_frame[column_name][itr_index])

			TestCSV._logger._info("IsLenghtInBetweenOrEqualsTo check is completed for column '{}'".format(column_name))
			return "0"
		except Exception as e:
			TestCSV._logger._error("Error occurred! in '_islenghtinbetweenorequalsto' -> "+str(e))
			return "1"
		pass


	@classmethod
	def _isvaluerange(cls, column_name, arg1) -> str:
		"""executes _isvaluerange method"""
		try:
			test_type = "IsValueRange";
			for itr_index in range(len(TestCSV._data_frame)):
				bug_store = [];
				if len(re.findall("^"+arg1+"$", TestCSV._data_frame[column_name][itr_index])) == 1:
					TestCSV._passed+= 1; 
				else:
					TestCSV._failed+= 1; 
					TestCSV._collect_failure(column_name,itr_index,test_type,arg1,"null",TestCSV._data_frame[column_name][itr_index])

			TestCSV._logger._info("IsValueRange check is completed for column '{}'".format(column_name))
			return "0"
		except Exception as e:
			TestCSV._logger._error("Error occurred! in '_isvaluerange' -> "+str(e))
			return "1"
		pass

	@classmethod
	def _isunique(cls, column_name) -> str:
		"""executes _isunique method"""
		try:
			test_type = "IsUnique";
			all_data = list(TestCSV._data_frame[column_name])
			for itr_index in range(len(all_data)):
				bug_store = [];
				if all_data.count(all_data[itr_index]) == 1:
					TestCSV._passed += 1; 
				else:
					TestCSV._failed += 1; 
					TestCSV._collect_failure(column_name,itr_index,test_type,arg1,"null",TestCSV._data_frame[column_name][itr_index])

			TestCSV._logger._info("IsUnique check is completed for column '{}'".format(column_name))
			return "0"
		except Exception as e:
			TestCSV._logger._error("Error occurred! in '_isunique' -> "+str(e))
			return "1"
		pass


	@classmethod
	def _create_table_in_memory(cls, table_name, cache_or_file) -> str:
		"""_"""
		try:
			header = TestCSV._csv_header;
			SQL_start = """CREATE TABLE "{}" (""".format(table_name);
			SQL_body = "";
			SQL_end = """);""";
			for itr_index in range(len(header)):
				SQL_body = SQL_body +"'"+ header[itr_index] + "' TEXT, ";
			SQL_body = SQL_body[:-2]

			table_creation_string = SQL_start+SQL_body+SQL_end

			if cache_or_file == 1:
				TestCSV._memory_database_creation_flag = 1
			elif cache_or_file == 2:
				TestCSV._file_database_creation_flag = 1
			else:
				pass

			return table_creation_string;

		except Exception as e:
			TestCSV._logger._error("Error occurred! in '_create_table_in_memory' -> "+str(e))
			return "1";
		pass


	@classmethod
	def _isdependency(cls, column_name, arg1, arg2) -> str:
		"""executes _isdependency method"""
		try:
			test_type = "IsDependency";

			#database creation process
			if TestCSV._memory_database_creation_flag == 0:
				#connect SQLite db
				TestCSV._sqlite_connection = sqlite3.connect(':memory:')
				TestCSV._logger._info("(cache)-Database is craeted in the memory.")

				#create Mr cursor
				TestCSV._generic_cursor = TestCSV._sqlite_connection.cursor()
				TestCSV._logger._info("(cache)-The cursor is created.")

				#create  table
				table_creation_string = TestCSV._create_table_in_memory("table_name",1)
				TestCSV._logger._info("(cache)-Table creation statement: {}".format(table_creation_string))
				TestCSV._sqlite_connection.execute(table_creation_string)
				TestCSV._logger._info("(cache)-Table is created in memory.")

				data_with_list_form = TestCSV._data_frame.values.tolist() #convert dataframe to python list (array)
				for itr_index in range(len(data_with_list_form)):
					TestCSV._sqlite_connection.execute("INSERT INTO table_name VALUES {};".format(str(data_with_list_form[itr_index]).replace("[","(").replace("]",")")))
				TestCSV._sqlite_connection.commit()
				TestCSV._logger._info("(cache)-Data is loaded to cache.")

			elif arg2.upper() == "TRUE" and TestCSV._file_database_creation_flag == 0:
				database_file_name = TestCSV._csv_file_name+"_Database"+time.strftime("%Y%m%d%H%M%S", time.localtime());
				file_object = open(str(database_file_name)+".db","w")
				file_object.close()
				sqlite_connection_for_file = sqlite3.connect(str(database_file_name)+".db")
				TestCSV._logger._info("(file)-Database file '{}' is craeted in the memory.".format(str(database_file_name)+".db"))

				#create Mr cursor
				cursor_for_file = sqlite_connection_for_file.cursor()
				TestCSV._logger._info("(file)-The cursor is created.")

				#create table
				table_creation_string = TestCSV._create_table_in_memory("table_name",2)
				TestCSV._logger._info("(file)-Table creation statement: {}".format(table_creation_string))
				sqlite_connection_for_file.execute(table_creation_string)
				TestCSV._logger._info("(file)-Table is created in memory.")

				data_with_list_form = TestCSV._data_frame.values.tolist() #convert dataframe to python list (array)
				for itr_index in range(len(data_with_list_form)):
					sqlite_connection_for_file.execute("INSERT INTO table_name VALUES {};".format(str(data_with_list_form[itr_index]).replace("[","(").replace("]",")")))
				sqlite_connection_for_file.commit()
				TestCSV._logger._info("(file)-Data is inserted to file.")

			else:
				pass

			TestCSV._generic_cursor.execute(arg1);
			query_rsult = TestCSV._generic_cursor.fetchall()
			TestCSV._logger._info("Executed query: {}".format(arg1))
			TestCSV._logger._info("Return of executed query: {}".format(query_rsult))

			bug_store = [];

			if query_rsult[0][0] == 0:
				TestCSV._passed += 1; 
			else:
				TestCSV._failed += 1;
				#colum_name, row_number, test_type, arg1, arg2, data
				TestCSV._collect_failure(column_name,"Row Number cannot be shown with dependency test.",test_type,arg1,arg2,str(query_rsult))

			TestCSV._logger._info("IsDependency check is completed for column '{}'".format(column_name))
			return "0"
		except Exception as e:
			TestCSV._logger._error("Error occurred! in '_isdependency' -> "+str(e))
			return "1"
		pass

	@classmethod
	def _reporting_result(cls, output_type) -> str:
		"""Generate result diffirent format"""
		try:
			file_name = TestCSV._csv_file_name+"_Report"+time.strftime("%Y%m%d%H%M%S", time.localtime());
			header = ["COLUMN_NAME","ROW_NUMER","TEST_TYPE","ARG_1","ARG_2","FAILED_DATA"]
			if output_type.upper() == "CSV":
				file = open(file_name+".csv", mode="w", newline="")
				csv_writer = csv.writer(file, quoting=csv.QUOTE_ALL)
				csv_writer.writerow(header)
				csv_writer.writerows(TestCSV._found_bugs)
				file.close()
				TestCSV._logger._info("'{}' report generated.".format(file_name))
			elif output_type.upper() == "HTML":
				file = open(file_name+".html", mode="w")
				html_header_start = """<table class="table table-bordered table-hover table-condensed"><thead><style>table {font-family: arial, sans-serif; border-collapse: collapse; width: 100%;}td, th {border: 1px solid #dddddd;text-align: left;padding: 8px;}tr:nth-child(even) {background-color: #dddddd;}</style><tr><th title="Field #1">COLUMN_NAME</th><th title="Field #2">ROW_NUMER</th><th title="Field #3">TEST_TYPE</th><th title="Field #4">ARG_1</th><th title="Field #5">ARG_2</th><th title="Field #6">FAILED_DATA</th></tr></thead><tbody>"""
				html_header_end = """</tbody></table>"""
				html_data = "";
				for itr_index in range(len(TestCSV._found_bugs)):
					html_data = html_data + "<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>".format(TestCSV._found_bugs[itr_index][0],TestCSV._found_bugs[itr_index][1],TestCSV._found_bugs[itr_index][2],TestCSV._found_bugs[itr_index][3].replace('"','&quot;'),TestCSV._found_bugs[itr_index][4],TestCSV._found_bugs[itr_index][5].replace("'","&#39;"))
				html_ready = html_header_start+html_data+html_header_end;
				file.write(html_ready)
				file.close()
				TestCSV._logger._info("'{}' report generated.".format(file_name))
			else:
				TestCSV._logger._error("Report could not be generated, format '{}' is not known".format(output_type))
			return "0"
		except Exception as e:
			TestCSV._logger._error("Error occurred! in '_reporting_result' -> "+str(e))
			return "1"
		pass


	@classmethod
	def master_method(cls, csv_file_name, json_file_name, output_type) -> str:
		"""Master method, where class methods are called"""
		try:

			TestCSV._csv_file_name = csv_file_name;
			TestCSV._read_csv();
			TestCSV._json_file_name = json_file_name;
			TestCSV._read_json();

			if TestCSV._csv_header_check() == '0':
				TestCSV._case_iteration();
				print("--Execution is started")
				TestCSV._reporting_result(output_type);
				print("--Execution is finished")

			TestCSV._logger._info("master_method method is finished")
			return "0"
		except Exception as e:
			TestCSV._logger._error("Error occurred! in 'main' -> "+str(e))
			return "1"
		pass


def runner(args):
	"""runner stays in between master method and main method"""
	if args.example == "testcase":
		f = open("testcase.json","w")
		f.write("""[{"case":"1","column": "Region","type": "IsNotNull","arg1": null,"arg2": null},{"case":"2","column": "Order Priority","type": "IsValueRange","arg1": "(M|C)","arg2": null}]""")
		f.close()
	elif args.example == "report":
		f = open("report.csv","w")
		f.write("Region,Country,Item Type,Sales Channel,Order Priority\nAsia,Singapore,Snacks,Online,C\nSub-Saharan Africa,Ethiopia,Cosmetics,Online,M\nAfrica,Tanzania,Cosmetics,Offline,M")
		f.close()
	else:
		test_agent = pyFork.TestCSV()
		test_agent.master_method(args.report, args.testcase, args.output)



def main():
	"""User Interface for console"""
	my_parser = argparse.ArgumentParser()

	my_parser.add_argument('--report', type=str, help="Provide your report file, Example: 'report.csv'")

	my_parser.add_argument('--testcase', type=str, help="Provide your testcase file, Example: 'testcase.json'")

	my_parser.add_argument('--example', type=str, help="Provide your testcase file, Example: 'report' or 'testcase'")

	my_parser.add_argument('--output', type=str, help="Provide your output file type, Example 'csv' or 'html'")

	args = my_parser.parse_args()

	runner(args)


if __name__ == '__main__':
	"""main method where the script starts running"""
	main()
