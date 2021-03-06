
import sqlite3
import json

def _get_table(cursor, table):
	try:
		cursor.execute('SELECT * FROM %s' % table)
	except sqlite3.OperationalError:
		print('warning: one history database is locked\n\
  exit the browser and kill its background processes\n\
  if you want the most recent data to be included\n')

	return cursor.fetchall()

def _combine(tables):
	tables = map(lambda x: map(lambda y: list(y), x), tables)

	for table in tables[1:]:
		for i in xrange(len(tables[0])):
			for el in table[i]:
				tables[0][i].append(el)

	return tables[0]

def _add_keys(keys, values):
	return map(lambda x: dict(zip(keys, x[:len(keys)])), values)

def sqlite_to_json(db_name, tables, keys):
	if type(tables) != list:
		tables = [tables]

	conn = sqlite3.connect(db_name)
	c = conn.cursor()
	tables = map(lambda x: _get_table(c, x), tables)
	conn.close()

	data = _combine(tables)
	data = _add_keys(keys, data)

	return data
