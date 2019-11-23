#!/usr/bin/python
import os
import argparse

src_path = os.path.join(os.path.abspath(
    os.path.dirname(__file__) + '/../Database/gsoc_records.db'))
dest_path = os.path.join(os.path.abspath(
    os.path.dirname(__file__) + '/../stats/{}{}'))

arg_parser = argparse.ArgumentParser(
    description='Transform Database records to csv for specific year')
arg_parser.add_argument('Year',
                        type=int,
                        help='retrieve records for this year')
arg_parser.add_argument('--src', '-s',
                        type=str,
                        default=src_path,
                        help='existing database file path(Default: {})'.format(src_path))
arg_parser.add_argument('--dest', '-d',
                        type=str,
                        default=dest_path,
                        help='generated csv file path(Default: {})'.format(dest_path))
args = arg_parser.parse_args()

year = args.Year
csv_file_path = args.dest
database_path = args.src
output_path = csv_file_path.format(year, '.csv')
sql_query = "SELECT name,tagline,technologies,slots,year FROM records WHERE year = {} order by slots desc".format(
    year)
command = 'sqlite3 -header -csv {} "{}" > {}'.format(
    database_path, sql_query, output_path)

ret_code = os.system(command)

if ret_code == 0:
    print('Success')
    exit(0)
else:
    print('Something Went wrong! -_-')
    exit(1)
