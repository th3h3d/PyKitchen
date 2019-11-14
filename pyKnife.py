"""pyFork is for testing data in CSV format"""

import pandas
import time
import argparse
import pyKnife
import logger
import csv
import io
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

	_source_data = pandas.DataFrame();
	_target_data = pandas.DataFrame();

	_result_of_comparison = list();
	_header_of_result_of_comparison = list();



	_found_bugs = list()

	def __init__(self):
		"""Set mandatory input.
		"""
		pass

	@classmethod
	def _read_json_connection(cls) -> str:
		"""reads mapping file file and keeps in dataframe"""
		try:
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
			Testdb2db._set_mapping_file_name();
			return "0";
		except Exception as e:
			Testdb2db._logger._error("Error occurred! in '_validation_of_connection' -> "+str(e))
			return "1";
		pass

	@classmethod
	def _set_mapping_file_name(cls) -> str:
		"""sets file name for mapping file"""
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
			mapping_header = ['case','source_table','source_query','source_primary_keys','target_table','target_query','target_primary_keys']
			mapping_header_from_file = list(Testdb2db._data_frame_mapping.columns)

			for itr_index in range(len(mapping_header)):
				if mapping_header[itr_index] in mapping_header:
					pass
				else:
					Testdb2db._logger._error("Connection info {} is missing in the {} file.".format(mapping_header[itr_index],Testdb2db._mapping_file_name));
					Testdb2db._logger._error("File headers: '{}'".format(mapping_header_from_file));
					return "1";

			
			Testdb2db._logger._info("Validation of mapping is successfully finised.");
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
			for itr_index in range(len(Testdb2db._data_frame_mapping)):
				Testdb2db._case = Testdb2db._data_frame_mapping['case'][itr_index];
				Testdb2db._source_table = Testdb2db._data_frame_mapping['source_table'][itr_index];
				Testdb2db._source_query = Testdb2db._data_frame_mapping['source_query'][itr_index];
				Testdb2db._source_primary_keys = Testdb2db._data_frame_mapping['source_primary_keys'][itr_index];
				Testdb2db._target_table = Testdb2db._data_frame_mapping['target_table'][itr_index];
				Testdb2db._target_query = Testdb2db._data_frame_mapping['target_query'][itr_index];
				Testdb2db._target_primary_keys = Testdb2db._data_frame_mapping['target_primary_keys'][itr_index];
				Testdb2db._logger._info("Variable setting is successfully finished for case {}".format(itr_index))
				


			Testdb2db._logger._info("Variable setting and iteration is successfully finised for mapping data.");
			Testdb2db._query_data_for_source()	
			return "0";
		except Exception as e:
			Testdb2db._logger._error("Error occurred! in '_set_data_with_iteration' -> "+str(e))
			return "1";
		pass

	@classmethod
	def _query_data_for_source(cls) -> str:
		"""_"""
		try:
			db_engine = create_engine(Testdb2db._source_connection_string)
			db_connection = db_engine.connect()
			output_data_from_db = db_connection.execute(Testdb2db._source_query)
			Testdb2db._source_sql_statement = "";
			Testdb2db._source_data = pandas.DataFrame(output_data_from_db.fetchall())
			db_connection.close()

			Testdb2db._logger._info(Testdb2db._source_data.columns)
			Testdb2db._logger._info(Testdb2db._source_data.head())
			
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
			db_engine = create_engine(Testdb2db._target_connection_string)
			db_connection = db_engine.connect()
			output_data_from_db = db_connection.execute(Testdb2db._target_query)
			Testdb2db._target_data = pandas.DataFrame(output_data_from_db.fetchall())
			db_connection.close()

			Testdb2db._logger._info(Testdb2db._target_data.columns)
			Testdb2db._logger._info(Testdb2db._target_data.head())
			

			Testdb2db._logger._info("Data is fetched from target database.");
			Testdb2db._prepare_data_comparasion_result()
			return "0";
		except Exception as e:
			Testdb2db._logger._error("Error occurred! in '_query_data_for_target' -> "+str(e))
			return "1";
		pass


	@classmethod
	def _prepare_data_comparasion_result(cls) -> str:
		"""_"""
		try:
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

			#set source header
			header.append("System")
			for i in range(len(Testdb2db._source_data.columns)):
				header.append('column_'+str(i))
			#set target header
			header.append("System")
			for i in range(len(Testdb2db._target_data.columns)):
				header.append('column_'+str(i))		


			Testdb2db._header_of_result_of_comparison = str(header);
			Testdb2db._logger._info("Data header: {}".format(Testdb2db._header_of_result_of_comparison));

			Testdb2db._result_of_comparison = str(result);
			Testdb2db._logger._info("Data unmatched data: {}".format(Testdb2db._result_of_comparison));


			Testdb2db._logger._info("Data comparasion result is prepared.");
			return "0";
		except Exception as e:
			Testdb2db._logger._error("Error occurred! in '_prepare_data_comparasion_result' -> "+str(e))
			return "1";
		pass


	@classmethod
	def _reporting_javascript(cls) -> str:
		"""_"""
		try:
			source_sql_statement = '';
			for i in range(len(Testdb2db._source_query)):
				if i % 60 == 0 and i != 0:
					source_sql_statement = source_sql_statement + str(Testdb2db._source_query[i]) + "\\n";
				else:
					source_sql_statement = source_sql_statement + str(Testdb2db._source_query[i])

			target_sql_statement = '';
			for i in range(len(Testdb2db._source_query)):
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
			

			Testdb2db._logger._info("Report {} has been created.".format(html_report_name));
			return "0";
		except Exception as e:
			Testdb2db._logger._error("Error occurred! in '_reporting_javascript' -> "+str(e))
			return "1";
		pass

	@classmethod
	def _reporting_csv(cls) -> str:
		"""Generate CSV report""" #buggy
		try:
			csv_report_name = str(Testdb2db._source_table)+str("_")+str(Testdb2db._target_table)+str("__report_")+str(time.strftime("%Y%m%d%H%M%S", time.localtime()))+str(".csv")
			header = Testdb2db._header_of_result_of_comparison
			file_object = open(csv_report_name, mode="w", newline="")
			csv_writer = csv.writer(file_object, quoting=csv.QUOTE_ALL)
			csv_writer.writerow(header)
			for itr_index in range(len(Testdb2db._result_of_comparison)):
				csv_writer.writerow(Testdb2db._result_of_comparison[itr_index])
			file_object.close()
			Testdb2db._logger._info("'{}' report generated.".format(csv_report_name))
			return "0"
		except Exception as e:
			Testdb2db._logger._error("Error occurred! in '_reporting_csv' -> "+str(e))
			return "1"
		pass


	@classmethod
	def master_method(cls, json_connection_file_name, output_type) -> str:
		"""Master method, where class methods are called"""
		try:

			Testdb2db._connection_file_name = json_connection_file_name;
			Testdb2db._read_json_connection();

			if output_type == "javascript":
				Testdb2db._reporting_javascript();
			elif output_type == "csv":
				Testdb2db._reporting_csv()
			else:
				Testdb2db._logger._error("Output type '{}' is not chosen!".format(output_type))

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
		f.write("""[{"source_database_type":"sqlite","source_connection_string":"sqlite:////Users/th3h3d/Desktop/pyKnife/testdb.db","target_database_type":"oracle","target_connection_string":"sqlite:////Users/th3h3d/Desktop/pyKnife/testdb.db","mapped_tables":"mapping1.json"}]""")
		f.close()
		print("connection.json is created")
	elif args.example == "mapping":
		f = open("mapping.json","w")
		f.write("""[{"case":"1","source_table":"source","source_query":"SELECT Region AS Rg, Country AS Ctr, ItemType AS ItmTyp, SalesChannel AS Slcl, OrderPriority AS Odpr, OrderDate AS Ordt, OrderID AS Orid , ShipDate AS Shpdt, UnitsSold AS Untsl, UnitPrice AS Untpr, UnitCost AS Untcst, TotalRevenue AS Ttlrv, TotalCost AS Ttlcs, TotalProfit AS Ttlprf, id as ID FROM source","source_primary_keys":"id","target_table":"target","target_query":"SELECT Region_T AS Rg, Country_T AS Ctr, ItemType_T AS ItmTyp, SalesChannel_T AS Slcl, OrderPriority_T AS Odpr, OrderDate_T AS Ordt, OrderID_T AS Orid , ShipDate_T AS Shpdt, UnitsSold_T AS Untsl, UnitPrice_T AS Untpr, UnitCost_T AS Untcst, TotalRevenue_T AS Ttlrv, TotalCost_T AS Ttlcs, TotalProfit_T AS Ttlprf, id_T as ID FROM target","target_primary_keys":"id_T",}]""")
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