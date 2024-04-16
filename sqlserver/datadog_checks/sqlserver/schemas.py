from datadog_checks.sqlserver.const import (
    TABLES_IN_SCHEMA_QUERY,
    COLUMN_QUERY,
    PARTITIONS_QUERY,
    INDEX_QUERY,
    FOREIGN_KEY_QUERY,
    SCHEMA_QUERY,
)

from datadog_checks.sqlserver.utils import (
    execute_query_output_result_as_a_dict, get_list_chunks
)

import pdb

import time
import json
from datadog_checks.base.utils.db.utils import DBMAsyncJob, default_json_event_encoding

class Schemas:
    
    MAX_COLUMN_COUNT  = 100_000
    def __init__(self, check):
        self._check = check 
        self._log = check.log
        self.schemas_per_db = {} 

        # These are fields related to the work to do while doing the initial intake
        # for diffs there should eb a self._done_db_list which will be used to see if new dbs have appeared/disappeared.
        self._databases_to_query = []
        self._current_table_list = None
        self._current_schema_list = None
        self._number_of_collected_tables = 0 #TODO later switch to columns

    def reset_data_collection(self):
        self._current_table_list = None  
        self._current_schema_list = None
        self._number_of_collected_tables = 0
       
    def _init_schema_collection(self):
        currently_known_databases = self._check.get_databases()
        if len(self._databases_to_query) == 0:
            self._databases_to_query = self._check.get_databases()
            return  
        else:
            if self._databases_to_query[0] not in currently_known_databases:
                #TODO if db dissapeared we invalidate indexes should be done in exception treatment of use DB ?
                #if DB is not there the first use db will throw and we continue until we find an existing db or exaust the list
                # the idea is always finish the existing DB list and then run "diff" logic which will create a new list of "tasks"
                self.reset_data_collection()

   #TODO update this at the very end as it constantly changing
    """schemas data struct is a dictionnary with key being a schema name the value is
    schema
    dict:
        "name": str
        "schema_id": str
        "principal_id": str
        "tables" : []
            object_id : str
            name : str
            columns: list of columns                  
                "columns": dict
                    name: str
                    data_type: str
                    default: str
                    is_nullable : str
            indexes : list of indexes - important
            foreign_keys : list of foreign keys
            partitions useful to know the number 
    """
    def collect_schemas_data2(self):
        #schemas per db
        # flush previous collection
        pdb.set_trace()
        self.schemas_per_db = {} 
        self.dbs_metadata = []
        # init the index
        self._init_schema_collection()
        if len(self._databases_to_query) == 0:
            return
        
        # dont need an index just always safe the last one.
        def fetch_schema_data(cursor, db_name):
            # check if we start from scratch or not 
            pdb.set_trace()
            if self._current_schema_list is None:
                # find new schemas:
                schemas = self._query_schema_information(cursor)
            else:
                schemas = self._current_schema_list  

            if self._current_table_list is None:
                schemas[0]["tables"] = self._get_tables(schemas[0], cursor)
            else:
                schemas[0]["tables"] = self._current_table_list

            for index_sh, schema in enumerate(schemas):  
                if schema["tables"] is None or len(schema["tables"]) == 0:
                    schema["tables"] = self._get_tables(schema, cursor)
                for index_t,table in enumerate(schema["tables"]):
                    
                    #TODO later can stop after a certain amount of columns
                    # thus stop
                    self._number_of_collected_tables+=1
                    column_amount = self._get_table_data(table, schema, cursor)
                    pdb.set_trace()
                    if column_amount > 100_000 or self._number_of_collected_tables == 2:
                        self._number_of_collected_tables = 0
                        self._current_table_list = schema["tables"][index_t+1:]
                        self._current_schema_list = schemas[index_sh:]
                        # TODO this will send not only schemas with tables filled but schemas that are yet empty, not that bad but can be fixed
                        self.schemas_per_db[db_name] = schemas
                        self._databases_to_query = self._databases_to_query[self._databases_to_query.index(db_name):]
                        pdb.set_trace()
                        return False
            self.schemas_per_db[db_name] = schemas
            # if we reached this point means we went through all the list thus we can reset :
            self.reset_data_collection()
            self._databases_to_query = []
            return True
        self._check.do_for_databases(fetch_schema_data, self._databases_to_query)
        pdb.set_trace()
        print(self.schemas_per_db)
    
    #sends all the data in one go but split in chunks (like Seth's solution)
    def collect_schemas_data(self):
        pdb.set_trace()
        base_event = {
                "host": self._check.resolved_hostname,
                #"agent_version": datadog_agent.get_version(),
                "dbms": "sqlserver", #TODO ?
                "kind": "", # TODO ? 
                #"collection_interval": self.schemas_collection_interval,
                #"dbms_version": self._payload_pg_version(),
                #"tags": self._tags_no_db,
                #"cloud_metadata": self._config.cloud_metadata,
            }

        def fetch_schema_data(cursor, db_name):
            schemas = self._query_schema_information(cursor)

            coulmn_count  = 0
            for schema in schemas:
                tables = self._get_tables(schema, cursor)

                # tables_chunk = list(get_list_chunks(tables, chunk_size)) - may be will need to switch to chunks and change queries ... ask Justin
                start_table_index = 0
                if len(tables) > 0:
                    pdb.set_trace()
                    numer_columns,my_tables = self._get_tables_data(tables, schema, cursor)
                    pdb.set_trace()
                    print(my_tables, numer_columns)

                for index_t, table in enumerate(tables):
                    
                    before = time.time() * 1000
                    coulmn_count += self._get_table_data(table, schema, cursor)
                    after = time.time() * 1000
                    total = after - before
                    pdb.set_trace()
                    print(total)

                    if coulmn_count > self.MAX_COLUMN_COUNT or index_t == len(tables) -1:   # we flush if the last table or columns threshold
                        #flush data ...                         
                        print(total)
                        self._flush_schema(base_event, db_name, schema, tables[start_table_index:index_t+1])
                        start_table_index = index_t+1 if index_t+1 < len(tables) else 0 # 0 if we ve finished the tables anyway
                        coulmn_count = 0
                        # reset column coutnt
                    #if last  

            return True
        self._check.do_for_databases(fetch_schema_data, self._check.get_databases())

    # TODO this can be a separate class, we could stack in data on each loop iteration and it decides when to flush 

    def _flush_schema(self, base_event, database, schema, tables):
        event = {
            **base_event, 
            "metadata": [{"db_name":database, "schemas": [{**schema, "tables": tables}]}],
            "timestamp": time.time() * 1000,
        }
        json_event = json.dumps(event, default=default_json_event_encoding)
        self._log.debug("Reporting the following payload for schema collection: {}".format(json_event))
        self._check.database_monitoring_metadata(json_event)
        
    # TODO how often ?

    #TODOTODO do we need this map/list format if we are not dumping in json ??? May be we need to send query results as they are ? 

    #TODO Looks fine similar to Postgres, do we need to do someting with prinicipal_id
    # or reporting principal_id is ok
    def _query_schema_information(self, cursor):

        # principal_id is kind of like an owner not sure if need it.
        self._log.debug("collecting db schemas")
        self._log.debug("Running query [%s]", SCHEMA_QUERY)
        cursor.execute(SCHEMA_QUERY)
        schemas = []
        columns = [i[0] for i in cursor.description]
        schemas = [dict(zip(columns, row)) for row in cursor.fetchall()]
        for schema in schemas:
            schema["tables"] = []
        self._log.debug("fetched schemas len(rows)=%s", len(schemas))
        return schemas
        
    #TODO collect diffs : we need to take care of new DB / removed DB . schemas new removed
    # will nedd a separate query for changed indexes
    def _get_tables_data(self, table_list, schema, cursor):
        if len(table_list) == 0:
            return
        name_to_id = {}
        id_to_all = {}
        table_names = ",".join(["'{}'".format(t.get("name")) for t in table_list])
        table_ids = ",".join(["{}".format(t.get("object_id")) for t in table_list])
        for t in table_list:
            name_to_id[t["name"]] = t["object_id"] 
            id_to_all[t["object_id"]] = t
        total_columns_number  = self._populate_with_columns_data(table_names, name_to_id, id_to_all, schema, cursor)
        self._populate_with_partitions_data(table_ids, id_to_all, cursor)
        self._populate_with_foreign_keys_data(table_ids, id_to_all, cursor)
        pdb.set_trace()
        self._populate_with_index_data(table_ids, id_to_all, cursor)
        # unwrap id_to_all
        return total_columns_number, list(id_to_all.values())

    def _populate_with_columns_data(self, table_names, name_to_id, id_to_all, schema, cursor):
        # get columns if we dont have a dict here unlike postgres
        cursor.execute(COLUMN_QUERY.format(table_names, schema["name"]))
        data = cursor.fetchall()
        columns = [str(i[0]).lower() for i in cursor.description]
        rows = [dict(zip(columns, row)) for row in data]       
        for row in rows:
            table_id = name_to_id.get(str(row.get("table_name")))
            if table_id is not None:
                # exclude "table_name" from the row dict
                row.pop("table_name", None)
                id_to_all.get(table_id)["columns"] = id_to_all.get(table_id).get("columns",[]) + [row]
        return len(data)
    
    def _populate_with_partitions_data(self, table_ids, id_to_all, cursor):
        cursor.execute(PARTITIONS_QUERY.format(table_ids))
        columns = [str(i[0]).lower() for i in cursor.description] 
        rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
        for row in rows:
            id  = row.pop("object_id", None)
            if id is not None:
                #TODO what happens if not found ? 
                id_to_all.get(id)["partitions"] = row
            else:
                print("todo error")
            row.pop("object_id", None)
        print("end")

    def _populate_with_index_data(self, table_ids, id_to_all, cursor):
        cursor.execute(INDEX_QUERY.format(table_ids))
        pdb.set_trace()
        columns = [str(i[0]).lower() for i in cursor.description] 
        rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
        for row in rows:
            id  = row.pop("object_id", None)
            if id is not None:
                id_to_all.get(id)["indexes"] = row
            else:
                print("todo error")
            row.pop("object_id", None)
            pdb.set_trace()
        pdb.set_trace()
        print("end")

    def _populate_with_foreign_keys_data(self, table_ids, id_to_all, cursor):
            pdb.set_trace()
            cursor.execute(FOREIGN_KEY_QUERY.format(table_ids))
            columns = [str(i[0]).lower() for i in cursor.description] 
            rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
            for row in rows:
                id  = row.pop("object_id", None)
                if id is not None:
                    id_to_all.get(id)["foreign_keys"] = row
                else:
                    print("todo error")  
            pdb.set_trace()
            print("end")
        #return execute_query_output_result_as_a_dict(COLUMN_QUERY.format(table_name, schema_name), cursor)
    

    def _get_table_data(self, table, schema, cursor):
        table["columns"] = self._get_columns_data_per_table(table["name"], schema["name"], cursor)
        table["partitions"] = self._get_partitions_data_per_table(table["object_id"], cursor)
        if str(table["object_id"]) == "1803153469":
            pdb.set_trace()
            print("should have index")
        table["indexes"] = self._get_index_data_per_table(table["object_id"], cursor)
        table["foreign_keys"] = self._get_foreign_key_data_per_table(table["object_id"], cursor)
        #TODO probably here decide based on the columns amount
        return len(table["columns"])
        
    #TODO in SQLServer partitioned child tables should have the same object_id might be worth checking with a test.

    #TODOTODO do we need this map/list format if we are not dumping in json ??? May be we need to send query results as they are ? 
    def _get_tables(self, schema, cursor):
        cursor.execute(TABLES_IN_SCHEMA_QUERY.format(schema["schema_id"]))
        columns = [str(i[0]).lower() for i in cursor.description]
        rows = [dict(zip(columns, row)) for row in cursor.fetchall()] #TODO may be more optimal to patch columns with index etc 
        # rows = [dict(zip(columns + ["columns", "indexes", "partitions", "foreign_keys"], row + [[], [], [], []])) for row in cursor.fetchall()] #TODO may be this works
        return [ {"object_id" : row["object_id"], "name" : row['name'], "columns" : [], "indexes" : [], "partitions" : [], "foreign_keys" : []} for row in rows ]                  

    def _get_columns_data_per_table(self, table_name, schema_name, cursor):
        return execute_query_output_result_as_a_dict(COLUMN_QUERY.format(table_name, schema_name), cursor)

    #TODO table 1803153469 is in  sys.indexes but not in sys.index_columns ... shell we do something about it ?
    def _get_index_data_per_table(self, table_object_id, cursor):           
        return execute_query_output_result_as_a_dict(INDEX_QUERY.format(table_object_id), cursor)

    #TODO its hard to get the partition key - for later ? 
    def _get_partitions_data_per_table(self, table_object_id, cursor):
        # TODO check out sys.partitions in postgres we deliver some data about patitions
        # "partition_key": str (if has partitions) - equiv ? 
        # may be use this  https://littlekendra.com/2016/03/15/find-the-partitioning-key-on-an-existing-table-with-partition_ordinal/
        # for more in depth search, it's not trivial to determine partition key like in Postgres
        return execute_query_output_result_as_a_dict(PARTITIONS_QUERY.format(table_object_id), cursor, "partition_count")

    def _get_foreign_key_data_per_table(self, table_object_id, cursor):  
        return execute_query_output_result_as_a_dict(FOREIGN_KEY_QUERY.format(table_object_id), cursor, "foreign_key_count")         
