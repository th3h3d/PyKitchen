"""pyKnife is for running database to database comparison"""

import pandas
import time
import argparse
import pyKnife
import logger
import csv
import io
import sqlite3
from sqlalchemy import create_engine

#Magic Methods
__version__ = '1.0'

__author__ = ("Haci Emre Dasgin <haci.dasgin@gmail.com>")

__all__ = []



class Testdb2db():
	"""-"""
	_passed = 0
	_failed = 0

	_logger = logger.Logger();

	_connection_file_name = "";
	_data_frame_connection = pandas.DataFrame();
	_data_frame_mapping = pandas.DataFrame();
	_file_connection_headers = list();

	_source_database_type = "";
	_source_connection_string = "";
	_target_database_type = "";
	_target_connection_string = "";
	_mapped_tables = "";

	_case = "";
	_source_table = "";
	_source_query = "";
	_source_primary_keys = "";
	_target_table = "";
	_target_query = "";
	_target_primary_keys = "";
	_common_header = "";

	_source_data = list()
	_target_data = list()

	_comparison_source_to_target = list()
	_comparison_target_to_source = list()

	_result_of_comparison = list();
	_header_of_result_of_comparison = list();

	_report_output_type = "";

	_sqlite_connection = None

	_found_bugs = list()

	def __init__(self):
		"""Set mandatory input.
		"""
		pass

	@classmethod
	def _read_json_connection(cls) -> str:
		"""reads mapping file file and keeps in dataframe"""
		try:
			Testdb2db._printerim("Connection info is being read.")
			Testdb2db._data_frame_connection = pandas.read_json(Testdb2db._connection_file_name);
			Testdb2db._logger._info("JSON file '{}' is successfully loaded.".format(Testdb2db._connection_file_name));
			Testdb2db._data_frame_connection = Testdb2db._data_frame_connection.applymap(str); #changes all data type of dataframe to string
			Testdb2db._logger._info("All data type is converted to 'string' data type.");

			Testdb2db._validation_of_connection()
			return "0";
		except Exception as e:
			Testdb2db._logger._error("Error occurred! in '_read_json_connection' -> "+str(e))
			return "1";
		pass

	@classmethod
	def _validation_of_connection(cls) -> str:
		"""_"""
		try:
			connection_header = ['source_database_type','source_connection_string','target_database_type','target_connection_string','mapped_tables']
			connection_header_from_file = list(Testdb2db._data_frame_connection.columns)

			for itr_index in range(len(connection_header_from_file)):
				if connection_header_from_file[itr_index] in connection_header:
					pass
				else:
					Testdb2db._logger._error("Connection info {} is missing in the {} file.".format(connection_header_from_file[itr_index],Testdb2db._connection_file_name));
					Testdb2db._logger._error("File headers: '{}'".format(connection_header_from_file));
					return "1";
			
			
			Testdb2db._logger._info("Validation of connection info is successfully finised.");
			Testdb2db._printerim("Connection validation is passed.")
			Testdb2db._set_mapping_file_name();
			return "0";
		except Exception as e:
			Testdb2db._logger._error("Error occurred! in '_validation_of_connection' -> "+str(e))
			return "1";
		pass

	@classmethod
	def _set_mapping_file_name(cls) -> str:
		"""sets file name for mapping file, connection between 'connection.json' and 'mapping*.json'"""
		try:
			Testdb2db._mapping_file_name = Testdb2db._data_frame_connection['mapped_tables'][0]
			Testdb2db._logger._info("File name '{}' is set for reading mapping file.".format(Testdb2db._mapping_file_name));

			Testdb2db._read_json_mapping();
			return "0";
		except Exception as e:
			Testdb2db._logger._error("Error occurred! in '_set_mapping_file_name' -> "+str(e))
			return "1";
		pass


	@classmethod
	def _read_json_mapping(cls) -> str:
		"""reads mapping file file and keeps in dataframe"""
		try:
			Testdb2db._printerim("Mapping info is being read.")
			Testdb2db._data_frame_mapping = pandas.read_json(Testdb2db._mapping_file_name);
			Testdb2db._logger._info("JSON file '{}' is successfully loaded.".format(Testdb2db._data_frame_mapping));
			Testdb2db._data_frame_mapping = Testdb2db._data_frame_mapping.applymap(str); #changes all data type of dataframe to string
			Testdb2db._logger._info("All data type is converted to 'string' data type.");

			Testdb2db._validation_of_mapping()
			return "0";
		except Exception as e:
			Testdb2db._logger._error("Error occurred! in '_read_json_mapping' -> "+str(e))
			return "1";
		pass

	@classmethod
	def _validation_of_mapping(cls) -> str:
		"""_"""
		try:
			mapping_header = ['case','source_table','source_query','source_primary_keys','target_table','target_query','target_primary_keys','common_header']
			mapping_header_from_file = list(Testdb2db._data_frame_mapping.columns)

			for itr_index in range(len(mapping_header)):
				if mapping_header[itr_index] in mapping_header:
					pass
				else:
					Testdb2db._logger._error("Connection info {} is missing in the {} file.".format(mapping_header[itr_index],Testdb2db._mapping_file_name));
					Testdb2db._logger._error("File headers: '{}'".format(mapping_header_from_file));
					return "1";
			
			Testdb2db._logger._info("Validation of mapping is successfully finised.");
			Testdb2db._printerim("Mapping validation is passed.")
			Testdb2db._variable_setting_connection();
			return "0";
		except Exception as e:
			Testdb2db._logger._error("Error occurred! in '_validation_of_mapping' -> "+str(e))
			return "1";
		pass

	@classmethod
	def _variable_setting_connection(cls) -> str:
		"""_"""
		try:
			Testdb2db._source_database_type = Testdb2db._data_frame_connection['source_database_type'][0];
			Testdb2db._source_connection_string = Testdb2db._data_frame_connection['source_connection_string'][0];
			Testdb2db._target_database_type = Testdb2db._data_frame_connection['target_database_type'][0];
			Testdb2db._target_connection_string = Testdb2db._data_frame_connection['target_connection_string'][0];
			Testdb2db._mapped_tables = Testdb2db._data_frame_connection['mapped_tables'][0];

			
			Testdb2db._logger._info("Variable setting is successfully finised for connection data.");
			Testdb2db._set_data_with_iteration();
			return "0";
		except Exception as e:
			Testdb2db._logger._error("Error occurred! in '_variable_setting_connection' -> "+str(e))
			return "1";
		pass

	@classmethod
	def _set_data_with_iteration(cls) -> str:
		"""_"""
		try:
			Testdb2db._printerim("{} iteration(s) are detected.".format(len(Testdb2db._data_frame_mapping)))
			for itr_index in range(len(Testdb2db._data_frame_mapping)):
				Testdb2db._case = Testdb2db._data_frame_mapping['case'][itr_index];
				Testdb2db._printerim("Case {} is being iterated.".format(Testdb2db._case))
				Testdb2db._source_table = Testdb2db._data_frame_mapping['source_table'][itr_index];
				Testdb2db._source_query = Testdb2db._data_frame_mapping['source_query'][itr_index];
				Testdb2db._source_primary_keys = Testdb2db._data_frame_mapping['source_primary_keys'][itr_index];
				Testdb2db._target_table = Testdb2db._data_frame_mapping['target_table'][itr_index];
				Testdb2db._target_query = Testdb2db._data_frame_mapping['target_query'][itr_index];
				Testdb2db._target_primary_keys = Testdb2db._data_frame_mapping['target_primary_keys'][itr_index];
				Testdb2db._common_header = Testdb2db._data_frame_mapping['common_header'][itr_index];
				Testdb2db._logger._info("Variable setting is successfully finished for case {}".format(itr_index))
				Testdb2db._logger._info("Variable setting and iteration is successfully finised for mapping data.");
				Testdb2db._query_data_for_source();
				Testdb2db._printerim("Case {} is completed.\n".format(Testdb2db._case))

			return "0";
		except Exception as e:
			Testdb2db._logger._error("Error occurred! in '_set_data_with_iteration' -> "+str(e))
			return "1";
		pass

	@classmethod
	def _query_data_for_source(cls) -> str:
		"""_"""
		try:
			Testdb2db._printerim("Source data is being read.")
			db_engine = create_engine(Testdb2db._source_connection_string)
			db_connection = db_engine.connect()
			output_data_from_db = db_connection.execute(Testdb2db._source_query)
			Testdb2db._source_sql_statement = "";
			Testdb2db._source_data = output_data_from_db.fetchall()
			db_connection.close()
			
			Testdb2db._logger._info("Data is fetched from source database.");
			Testdb2db._query_data_for_target()

			return "0";
		except Exception as e:
			Testdb2db._logger._error("Error occurred! in '_variable_setting_connection' -> "+str(e))
			return "1";
		pass

	@classmethod
	def _query_data_for_target(cls) -> str:
		"""_"""
		try:
			Testdb2db._printerim("Target data is being read.")
			db_engine = create_engine(Testdb2db._target_connection_string)
			db_connection = db_engine.connect()
			output_data_from_db = db_connection.execute(Testdb2db._target_query)
			Testdb2db._target_data = output_data_from_db.fetchall()
			db_connection.close()
			
			Testdb2db._logger._info("Data is fetched from target database.");
			Testdb2db._data_loading_to_sqlite_memory()
			return "0";
		except Exception as e:
			Testdb2db._logger._error("Error occurred! in '_query_data_for_target' -> "+str(e))
			return "1";
		pass


	@classmethod
	def _data_loading_to_sqlite_memory(cls) -> str:
		"""_"""
		try:
			#set connection nothing
			Testdb2db._sqlite_connection = None

			#connect memory db
			Testdb2db._sqlite_connection = sqlite3.connect(':memory:')
			#Testdb2db._sqlite_connection = sqlite3.connect('/Users/th3h3d/Desktop/pyKnife/testdb.db')
			
			#Mr cursor
			the_cursor = Testdb2db._sqlite_connection.cursor()

			#create source table
			source_table_string = Testdb2db._create_source_table()
			Testdb2db._logger._info("Source table string is created: '{}'".format(source_table_string));
			Testdb2db._sqlite_connection.execute(source_table_string)
			Testdb2db._printerim("Source table is created in cache.")

			#insert source data to memory
			for itr_index1 in range(len(Testdb2db._source_data)):
				Testdb2db._sqlite_connection.execute("INSERT INTO source_table VALUES {};".format(str(Testdb2db._source_data[itr_index1])))
			Testdb2db._sqlite_connection.commit()
			Testdb2db._printerim("Source data is loaded to cache.")



			#create target table
			target_table_string = Testdb2db._create_target_table()
			Testdb2db._logger._info("Target table string is created: '{}'".format(target_table_string));
			Testdb2db._sqlite_connection.execute(target_table_string)
			Testdb2db._printerim("Target table is created in cache.")
			
			#insert target data to memory
			for itr_index1 in range(len(Testdb2db._target_data)):
				Testdb2db._sqlite_connection.execute("INSERT INTO target_table VALUES {};".format(str(Testdb2db._target_data[itr_index1])))
			Testdb2db._sqlite_connection.commit()
			Testdb2db._printerim("Target data is loaded to cache.")


			#create comparesion queries
			header = Testdb2db._common_header.split(",")

			SQL_start = "SELECT ";
			SQL_body = "";
			SQL_end_source = " FROM source_table"
			SQL_end_target = " FROM target_table"


			for itr_index in range(len(header)):
				SQL_body = SQL_body + header[itr_index] + ", "
			SQL_body = SQL_body[:-2]
			SQL_without_table = SQL_start+SQL_body

			SQL_difference_from_source_to_target = SQL_without_table+SQL_end_source+" EXCEPT "+SQL_without_table+SQL_end_target
			Testdb2db._logger._info("Comparesion query for source: '{}'".format(SQL_difference_from_source_to_target));

			SQL_difference_from_target_to_source = SQL_without_table+SQL_end_target+" EXCEPT "+SQL_without_table+SQL_end_source
			Testdb2db._logger._info("Comparesion query for target: '{}'".format(SQL_difference_from_target_to_source));


			#fetch comparison results
			the_cursor.execute(SQL_difference_from_source_to_target)
			Testdb2db._comparison_source_to_target = the_cursor.fetchall()
			Testdb2db._logger._info("Source to Target result: '{}'".format(Testdb2db._comparison_source_to_target));


			the_cursor.execute(SQL_difference_from_target_to_source)
			Testdb2db._comparison_target_to_source = the_cursor.fetchall()
			Testdb2db._logger._info("Target to Source result: '{}'".format(Testdb2db._comparison_target_to_source));


			Testdb2db._sqlite_connection.close()
			return "0";
		except Exception as e:
			Testdb2db._logger._error("Error occurred! in '_data_loading_to_sqlite_memory' -> "+str(e))
			return "1";
		pass



	@classmethod
	def _create_source_table(cls,) -> str:
		"""_"""
		try:
			header = Testdb2db._common_header.split(",")

			SQL_start = """CREATE TABLE "source_table" (""";
			SQL_body = "";
			SQL_end = """);"""
			for itr_index in range(len(header)):
				SQL_body = SQL_body + header[itr_index] + " TEXT, "
			SQL_body = SQL_body[:-2]

			source_table_string = SQL_start+SQL_body+SQL_end

			return source_table_string;

		except Exception as e:
			Testdb2db._logger._error("Error occurred! in '_create_source_table' -> "+str(e))
			return "1";
		pass

	@classmethod
	def _create_target_table(cls,) -> str:
		"""_"""
		try:
			header = Testdb2db._common_header.split(",")

			SQL_start = """CREATE TABLE "target_table" (""";
			SQL_body = "";
			SQL_end = """);"""
			for itr_index in range(len(header)):
				SQL_body = SQL_body + header[itr_index] + " TEXT, "
			SQL_body = SQL_body[:-2]

			target_table_string = SQL_start+SQL_body+SQL_end

			return target_table_string;
		except Exception as e:
			Testdb2db._logger._error("Error occurred! in '_create_target_table' -> "+str(e))
			return "1";
		pass

	@classmethod
	def _prepare_data_comparasion_result(cls) -> str:
		"""_"""
		try:
			Testdb2db._printerim("Data is being compared.")
			result = list()
			header = list()
			make_dict = {"source":Testdb2db._source_data, "target":Testdb2db._target_data}
			make_concat = pandas.concat(make_dict)
			make_concat.drop_duplicates(keep=False)

			df_gpby = make_concat.groupby(list(make_concat.columns))
			new_index = [x[0] for x in df_gpby.groups.values() if len(x) == 1]
			new_dataframe = make_concat.reindex(new_index)

			source = list()
			target = list()

			for i in range(len(new_index)):
				if new_index[i][0] == 'source':
					source.append(new_index[i])
				else:
					target.append(new_index[i])

			for i in range(len(target)):
				flag = 0;
				for j in range(len(source)):
					if target[i][1] == source[j][1]:
						flag = 1;
						source_and_target = list()
						all_target = new_dataframe.loc[target[i][0]]
						target_row = list(all_target.loc[ target[i][1] , : ])
						target_row.insert(0,"Target")
						source_and_target = list()
						all_source = new_dataframe.loc[source[j][0]]
						source_row = list(all_source.loc[ source[j][1] , : ])
						source_row.insert(0,"Source")
						source_and_target.extend(source_row)                
						source_and_target.extend(target_row)
						result.append(source_and_target)
					else:
						pass
				if flag == 0:
					source_and_target = list()
					all_target = new_dataframe.loc[target[i][0]]
					target_row = list(all_target.loc[ target[i][1] , : ])
					target_row.insert(0,"Target")
					source_row = list()
					source_row.insert(0,"Source")
					for walk in range(len(target_row)-1):
						source_row.append("Not Found")
					source_and_target.extend(source_row)
					source_and_target.extend(target_row)
					result.append(source_and_target)
					
			#set all data to string type
			for i in range(len(result)):
				for j in range(len(result[i])):
					result[i][j] = str(result[i][j])

			#set headers
			Testdb2db._common_header = Testdb2db._common_header.replace(" ","") #no space in the header!
			common_header_for_both = Testdb2db._common_header.split(",")
			if len(common_header_for_both) == len(Testdb2db._source_data.columns) and len(common_header_for_both) == len(Testdb2db._target_data.columns):
				#set source header
				header.append("System")
				for itr_index in range(len(common_header_for_both)):
					header.append(common_header_for_both[itr_index])
				#set target header
				header.append("System")
				for itr_index in range(len(common_header_for_both)):
					header.append(common_header_for_both[itr_index])
			else:
				Testdb2db._logger._error("Error occurred! Either source or target column length (source: {}, target: {}) does not match with defined common headers (common header: {})".format(len(Testdb2db._source_data.columns),len(Testdb2db._target_data.columns),len(common_header_for_both)))
				return "1";

			Testdb2db._header_of_result_of_comparison = str(header);
			Testdb2db._logger._info("Data header: {}".format(Testdb2db._header_of_result_of_comparison));

			Testdb2db._result_of_comparison = str(result);
			Testdb2db._logger._info("Data unmatched data: {}".format(Testdb2db._result_of_comparison));

			Testdb2db._logger._info("Data comparasion result is prepared.");

			#if there is no unmatched data, stop right here
			if len(result) == 0:
				Testdb2db._printerim("All data is matched!")
				Testdb2db._printerim("Report is NOT printed!")
				return "0";				


			#output file method calls happen here.
			if Testdb2db._report_output_type == "javascript":
				Testdb2db._reporting_javascript();
			elif Testdb2db._report_output_type == "csv":
				Testdb2db._reporting_csv()
			else:
				Testdb2db._logger._error("Output type '{}' is not chosen!".format(Testdb2db._report_output_type))
				return "1";

			return "0";
		except Exception as e:
			Testdb2db._logger._error("Error occurred! in '_prepare_data_comparasion_result' -> "+str(e))
			return "1";
		pass


	@classmethod
	def _reporting_javascript(cls) -> str:
		"""_"""
		try:
			Testdb2db._printerim("HTML report is being generated.")
			source_sql_statement = '';
			for i in range(len(Testdb2db._source_query)):
				if i % 60 == 0 and i != 0:
					source_sql_statement = source_sql_statement + str(Testdb2db._source_query[i]) + "\\n";
				else:
					source_sql_statement = source_sql_statement + str(Testdb2db._source_query[i])

			target_sql_statement = '';
			for i in range(len(Testdb2db._target_query)):
				if i % 60 == 0 and i != 0:
					target_sql_statement = target_sql_statement + str(Testdb2db._target_query[i]) + "\\n";
				else:
					target_sql_statement = target_sql_statement + str(Testdb2db._target_query[i])

			#read raw html code
			file_object_read = io.open("rawreportcode.txt", mode="r", encoding="utf-8")
			raw_html_code = file_object_read.read()

			#replace some part of raw data
			raw_html_code=raw_html_code.replace("@4055586c28f35be98535a1728a4248a9@",Testdb2db._header_of_result_of_comparison)
			raw_html_code=raw_html_code.replace("@7906899a18b96a3f8142fa93a0da4e74@",Testdb2db._result_of_comparison)
			raw_html_code=raw_html_code.replace("@595aa739fc58403c7c62cc2840d0b7fb@",source_sql_statement)
			raw_html_code=raw_html_code.replace("@69e396acbd4d981461374b77cabc07ff@",target_sql_statement)

			#write data into report
			html_report_name = str(Testdb2db._source_table)+str("_")+str(Testdb2db._target_table)+str("__report_")+str(time.strftime("%Y%m%d%H%M%S", time.localtime()))+str(".html")
			file_object_write = io.open(html_report_name, mode="w", encoding="utf-8")
			file_object_write.write(raw_html_code)
			
			Testdb2db._printerim("Report {} has been created.".format(html_report_name))
			return "0";
		except Exception as e:
			Testdb2db._logger._error("Error occurred! in '_reporting_javascript' -> "+str(e))
			return "1";
		pass

	@classmethod
	def _reporting_csv(cls) -> str:
		"""Generate CSV report""" #buggy
		try:
			Testdb2db._printerim("CSV report is being generated.")
			csv_report_name = str(Testdb2db._source_table)+str("_")+str(Testdb2db._target_table)+str("__report_")+str(time.strftime("%Y%m%d%H%M%S", time.localtime()))+str(".csv")
			header = Testdb2db._header_of_result_of_comparison
			file_object = open(csv_report_name, mode="w", newline="")
			csv_writer = csv.writer(file_object, quoting=csv.QUOTE_ALL)
			csv_writer.writerow(header)
			for itr_index in range(len(Testdb2db._result_of_comparison)):
				csv_writer.writerow(Testdb2db._result_of_comparison[itr_index])
			file_object.close()
			Testdb2db._printerim("'{}' report generated.".format(csv_report_name))
			return "0"
		except Exception as e:
			Testdb2db._logger._error("Error occurred! in '_reporting_csv' -> "+str(e))
			return "1"
		pass

	@classmethod
	def _printerim(cls, message_to_print_on_console) -> str:
		"""Master method, where class methods are called"""
		try:
			print("-- "+message_to_print_on_console)
			Testdb2db._logger._info("'{}' message is printed to user!".format(message_to_print_on_console))
			return "0"
		except Exception as e:
			Testdb2db._logger._error("Error occurred! in 'main' -> "+str(e))
			return "1"
		pass

	@classmethod
	def master_method(cls, json_connection_file_name, output_type) -> str:
		"""Master method, where class methods are called"""
		try:
			Testdb2db._connection_file_name = json_connection_file_name;
			Testdb2db._report_output_type = output_type;
			Testdb2db._printerim("Script started.")
			if Testdb2db._connection_file_name != "" and Testdb2db._report_output_type != "":
				Testdb2db._read_json_connection();
			else:
				Testdb2db._logger._error("Error occurred! Either connection or output is not provided")
				return "1"

			Testdb2db._logger._info("master_method method is finished")
			return "0"
		except Exception as e:
			Testdb2db._logger._error("Error occurred! in 'main' -> "+str(e))
			return "1"
		pass


def runner(args):
	"""runner stays in between master method and main method"""
	if args.example == "connection":
		f = open("connection.json","w")
		f.write("""[{\n"source_database_type":"sqlite",\n"source_connection_string":"sqlite:////Users/th3h3d/Desktop/pyKnife/testdb.db",\n"target_database_type":"oracle",\n"target_connection_string":"sqlite:////Users/th3h3d/Desktop/pyKnife/testdb.db",\n"mapped_tables":"mapping1.json"\n}]""")
		f.close()
		print("connection.json is created")
	elif args.example == "mapping":
		f = open("mapping1.json","w")
		f.write("""[{\n"case":"1",\n"source_table":"source",\n"source_query":"SELECT Region AS Rg, Country AS Ctr, ItemType AS ItmTyp, SalesChannel AS Slcl, OrderPriority AS Odpr, OrderDate AS Ordt, OrderID AS Orid , ShipDate AS Shpdt, UnitsSold AS Untsl, UnitPrice AS Untpr, UnitCost AS Untcst, TotalRevenue AS Ttlrv, TotalCost AS Ttlcs, TotalProfit AS Ttlprf, id as ID FROM source ORDER BY id",\n"source_primary_keys":"id",\n"target_table":"target",\n"target_query":"SELECT Region_T AS Rg, Country_T AS Ctr, ItemType_T AS ItmTyp, SalesChannel_T AS Slcl, OrderPriority_T AS Odpr, OrderDate_T AS Ordt, OrderID_T AS Orid , ShipDate_T AS Shpdt, UnitsSold_T AS Untsl, UnitPrice_T AS Untpr, UnitCost_T AS Untcst, TotalRevenue_T AS Ttlrv, TotalCost_T AS Ttlcs, TotalProfit_T AS Ttlprf, id_T as ID FROM target ORDER BY",\n"target_primary_keys":"id_T",\n"common_header":"Region, Country, ItemType, SalesChannel, OrderPriority, OrderDate, OrderID, ShipDate, UnitsSold, UnitPrice, UnitCost, TotalRevenue, TotalCost, TotalProfit, ID"\n}]""")
		f.close()
		print("mapping.json is created")
	elif args.example == "jsrawreportcode":
		f = open("rawreportcode.txt","w")
		f.write("<script>\n$.reportInfo.dataHeaderDiff = @4055586c28f35be98535a1728a4248a9@;\n$.reportInfo.diffData = @7906899a18b96a3f8142fa93a0da4e74@;\n$.reportInfo.source.sql = \"@595aa739fc58403c7c62cc2840d0b7fb@\";\n$.reportInfo.target.sql = \"@69e396acbd4d981461374b77cabc07ff@\";\n<\\script>")
		f.close()
		print("rawreportcode.txt is created")
	else:
		test_agent = pyKnife.Testdb2db()
		test_agent.master_method(args.connection, args.output)


def main():
	"""User Interface for console"""
	my_parser = argparse.ArgumentParser()

	my_parser.add_argument('--connection', type=str, help="Provide your mapping file, Example: 'connection.json'")

	my_parser.add_argument('--example', type=str, help="Provide your example opetion, Example: 'connection' or 'mapping' or 'rawreportcode'")

	my_parser.add_argument('--output', type=str, help="Provide your output file type (p.s. csv is buggy currently), Example 'javascript' or 'csv'")


	args = my_parser.parse_args()

	runner(args)


if __name__ == '__main__':
	"""main method where the script starts running"""
	main()