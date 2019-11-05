#!/usr/bin/python
import os
import argparse

arg_parser = argparse.ArgumentParser(description='Transform Database records to csv for specific year')
arg_parser.add_argument('Year',
                        type=int,
                        help='retrieve records for this year')
arg_parser.add_argument('--src', '-s',
                        type=str,
                        default='../Database/gsoc_records.db',
                        help='existing database file path(Default:../Database/gsoc_records.db)')
arg_parser.add_argument('--dest', '-d',
                        type=str,
                        default='../stats/',
                        help='generated csv file path(Default:../stats)')
args = arg_parser.parse_args()

year = args.Year
csv_file_path = args.dest
database_path = args.src
file_name = csv_file_path + str(year) + '.csv'
sql_query = "SELECT name,tagline,technologies,slots,year FROM records WHERE year = {} order by slots desc".format(year)
command = 'sqlite3 -header -csv {} "{}" > {}'.format(database_path, sql_query, file_name)

ret_code = os.system(command)

if ret_code == 0:
    print('Success')
    exit(0)
else:
    print('Something Went wrong! -_-')
    exit(1)
