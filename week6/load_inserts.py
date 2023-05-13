# this program loads Census ACS data using basic, slow INSERTs 
# run it with -h to see the command line options

import time
import psycopg2
import argparse
import re
import csv

DBname = "postgres"
DBuser = "postgres"
DBpwd = "Ganeshgani24!"
TableName = 'CensusData4'
Datafile = "acs2015_census_tract_data_part1.csv"  # name of the data file to be loaded
CreateDB = False  # indicates whether the DB table should be (re)-created

def row2vals(row):
	for key in row:
		if not row[key]:
			row[key] = 0  # ENHANCE: handle the null vals
		row['County'] = row['County'].replace('\'','')  # TIDY: eliminate quotes within literals

	ret = f"""
	   {row['CensusTract']},            -- CensusTract
	   '{row['State']}',                -- State
	   '{row['County']}',               -- County
	   {row['TotalPop']},               -- TotalPop
	   {row['Men']},                    -- Men
	   {row['Women']},                  -- Women
	   {row['Hispanic']},               -- Hispanic
	   {row['White']},                  -- White
	   {row['Black']},                  -- Black
	   {row['Native']},                 -- Native
	   {row['Asian']},                  -- Asian
	   {row['Pacific']},                -- Pacific
	   {row['Citizen']},                -- Citizen
	   {row['Income']},                 -- Income
	   {row['IncomeErr']},              -- IncomeErr
	   {row['IncomePerCap']},           -- IncomePerCap
	   {row['IncomePerCapErr']},        -- IncomePerCapErr
	   {row['Poverty']},                -- Poverty
	   {row['ChildPoverty']},           -- ChildPoverty
	   {row['Professional']},           -- Professional
	   {row['Service']},                -- Service
	   {row['Office']},                 -- Office
	   {row['Construction']},           -- Construction
	   {row['Production']},             -- Production
	   {row['Drive']},                  -- Drive
	   {row['Carpool']},                -- Carpool
	   {row['Transit']},                -- Transit
	   {row['Walk']},                   -- Walk
	   {row['OtherTransp']},            -- OtherTransp
	   {row['WorkAtHome']},             -- WorkAtHome
	   {row['MeanCommute']},            -- MeanCommute
	   {row['Employed']},               -- Employed
	   {row['PrivateWork']},            -- PrivateWork
	   {row['PublicWork']},             -- PublicWork
	   {row['SelfEmployed']},           -- SelfEmployed
	   {row['FamilyWork']},             -- FamilyWork
	   {row['Unemployment']}            -- Unemployment
	"""

	return ret


def initialize():
  parser = argparse.ArgumentParser()
  parser.add_argument("-d", "--datafile", required=True)
  parser.add_argument("-c", "--createtable", action="store_true")
  args = parser.parse_args()

  global Datafile
  Datafile = args.datafile
  global CreateDB
  CreateDB = args.createtable

# read the input data file into a list of row strings
def readdata(fname):
	print(f"readdata: reading from File: {fname}")
	with open(fname, mode="r") as fil:
		dr = csv.DictReader(fil)
		
		rowlist = []
		for row in dr:
			rowlist.append(row)

	return rowlist

# convert list of data rows into list of SQL 'INSERT INTO ...' commands
def getSQLcmnds(rowlist):
	cmdlist = []
	for row in rowlist:
		valstr = row2vals(row)
		cmd = f"INSERT INTO {TableName} VALUES ({valstr});"
		cmdlist.append(cmd)
	return cmdlist

# connect to the database
def dbconnect():
	connection = psycopg2.connect(
		host="localhost",
		database=DBname,
		user=DBuser,
		password=DBpwd,
	)
	#connection.autocommit = True
	return connection

# create the target table 
# assumes that conn is a valid, open connection to a Postgres database
def createTable(conn):

	with conn.cursor() as cursor:
		cursor.execute(f"""
			DROP TABLE IF EXISTS {TableName};
			CREATE TEMP TABLE {TableName} (
				CensusTract         NUMERIC,
				State               TEXT,
				County              TEXT,
				TotalPop            INTEGER,
				Men                 INTEGER,
				Women               INTEGER,
				Hispanic            DECIMAL,
				White               DECIMAL,
				Black               DECIMAL,
				Native              DECIMAL,
				Asian               DECIMAL,
				Pacific             DECIMAL,
				Citizen             DECIMAL,
				Income              DECIMAL,
				IncomeErr           DECIMAL,
				IncomePerCap        DECIMAL,
				IncomePerCapErr     DECIMAL,
				Poverty             DECIMAL,
				ChildPoverty        DECIMAL,
				Professional        DECIMAL,
				Service             DECIMAL,
				Office              DECIMAL,
				Construction        DECIMAL,
				Production          DECIMAL,
				Drive               DECIMAL,
				Carpool             DECIMAL,
				Transit             DECIMAL,
				Walk                DECIMAL,
				OtherTransp         DECIMAL,
				WorkAtHome          DECIMAL,
				MeanCommute         DECIMAL,
				Employed            INTEGER,
				PrivateWork         DECIMAL,
				PublicWork          DECIMAL,
				SelfEmployed        DECIMAL,
				FamilyWork          DECIMAL,
				Unemployment        DECIMAL
			);	
		""")

		print(f"Created {TableName}")

def load(conn):

        with conn.cursor() as cursor:
#                print(f"Loading {len(icmdlist)} rows")
                start = time.perf_counter()

 #               for cmd in icmdlist:
 #                       cursor.execute(cmd)

                with open(Datafile, 'r') as f:
                    next(f)
                    for line in f:
                        columns = line.rstrip('\n').split(',')
                        modified_columns = [col if col != '' else 'NULL' for col in columns]
                        modified_line = ','.join(modified_columns)
                        modified_file_object = StringIO(modified_line)
                        cursor.copy_from(modified_file_object, 'censusdata1h',sep=',',null='NULL')

                cursor.execute(f"""
                        ALTER TABLE censusdata1h ADD PRIMARY KEY (CensusTract);
                        CREATE INDEX idx_censusdata1h_State ON censusdata1h(State);
                        COMMIT;
                """)

                elapsed = time.perf_counter() - start
                print(f'Finished Loading. Elapsed Time: {elapsed:0.4} seconds')

def keys(conn):
    with conn.cursor() as cursor:
        cursor.execute(f"""
                       INSERT INTO newtable SELECT * FROM {TableName};
                       ALTER TABLE newtable  ADD PRIMARY KEY (CensusTract);
                       CREATE INDEX idx_newtable_State ON newtable(State);""")
def load(cmdlist):
        try:
                conn = dbconnect()
                with conn.cursor() as cursor:
                        for cmd in cmdlist:
                                cursor.execute(cmd)
                                conn.commit() # commit after every transaction
        finally:
                conn.close()

def main():
	initialize()
	conn = dbconnect()
	rlis = readdata(Datafile)
	cmdlist = getSQLcmnds(rlis)

	if CreateDB:
		createTable(conn)

	load(conn, cmdlist)


if __name__ == "__main__":
	main()



