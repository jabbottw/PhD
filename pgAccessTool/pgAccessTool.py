"""
/***************************************************************************
Name		     : DB_Processor
Description          : Database query tool set
Date                 : 5/9/2014
copyright            : (C) 2014 by Julian Abbott-Whitley - PhD WFS
email                : jwhitley@phdwellfile.com 
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program has been developed for use by PhD well file services.    *
 *                                                                         *
 ***************************************************************************/
 """
# Import necessary libraries
import psycopg2
import sys

# PostGreSQL data processor class
# Establishes a connection to a specified PG database so information can be queried as needed
class DB_Processor:

        # Class initiation
        #Requires the following parameters: DB name, DB username, DB password, Host location, port number
        def __init__(self, db, uName, pWord, host, port):
            self.__db = db            # DB name
            self.__uName = uName      # User name
            self.__pWord = pWord      # Password
            self.__host = host        # DB Host location
            self.__port = port        # Port Number
            # Set the DB connection using the provided parameters
            self.__con = psycopg2.connect(database="%s" % (self.db),user="%s" % (self.uName),password="%s" % (self.pWord),host="%s" % (self.host),port="%s" % (self.port))

        #### Getters Setters and Delete methods ####
        def get_db(self):
            return self.__db

        def get_u_name(self):
            return self.__uName

        def get_p_word(self):
            return self.__pWord

        def get_host(self):
            return self.__host

        def get_port(self):
            return self.__port

        def get_con(self):
            return self.__con

        def set_db(self, value):
            self.__db = value

        def set_u_name(self, value):
            self.__uName = value

        def set_p_word(self, value):
            self.__pWord = value

        def set_host(self, value):
            self.__host = value

        def set_port(self, value):
            self.__port = value

        def set_con(self, value):
            self.__con = value

        def del_db(self):
            del self.__db

        def del_u_name(self):
            del self.__uName

        def del_p_word(self):
            del self.__pWord

        def del_host(self):
            del self.__host

        def del_port(self):
            del self.__port

        def del_con(self):
            del self.__con

        db = property(get_db, set_db, del_db, "db's docstring")
        uName = property(get_u_name, set_u_name, del_u_name, "uName's docstring")
        pWord = property(get_p_word, set_p_word, del_p_word, "pWord's docstring")
        host = property(get_host, set_host, del_host, "host's docstring")
        port = property(get_port, set_port, del_port, "port's docstring")
        con = property(get_con, set_con, del_con, "con's docstring")


################  Utility Methods  ################


        # Set new DB connection parameters
        def setNewConnections(self, db, uName, pWord, host, port):
                self.__db = db
                self.__uName = uName
                self.__pWord = pWord
                self.__host = host
                self.__port = port
                self.__con = psycopg2.connect(database="%s" % (self.db),user="%s" % (self.uName),password="%s" % (self.pWord),host="%s" % (self.host),port="%s" % (self.port))
        
        # Establishes a new connection with the database using the settings stored in the objects variables
        def makeConnection(self):
                # Try block to make db connection
                try:
                        # Make connection
                        self.__con = psycopg2.connect(database="%s" % (self.db),user="%s" % (self.uName),password="%s" % (self.pWord),host="%s" % (self.host),port="%s" % (self.port))
                # Exception error
                except psycopg2.DatabaseError, e:
                        sys.exit(1)
        # Close the DB Connection
        def closeDBConnection(self):
                # Close  the connection
                        if self.__con:
                                self.__con.close()
                                
        # Sends an SQL query to the database and returns the results in the form of a list    
        def getDBData(self, sqlString):
            # List object to store the results
            dbList = []
            try:
                # Cursor object to execute and analyze the query results
                cur = self.__con.cursor()
                cur.execute(sqlString)
                    
                # Collect the column names from the query
                # col_names = [cn[0] for cn in cur.description]
                # Add the columns names to the zero row of the dbList
                #dbList.append(col_names)
                    
                # Collect all rows from the cursor
                rows = cur.fetchall()
                # Cycle through and collect all of the rows in the result list into the dbList
                for row in rows:
                    dbList.append(row)
                return dbList
                    
            except psycopg2.DatabaseError, e:
                return dbList
                
                
        
        # Extracts a select column from a 2-dim list into a single list object
        
        # Input data using a basic sql statement
        # This process will simply take the provided statement, execute the statement, and commit the results
        def inputDBData(self, sqlInput):
            #  try except block
            try:
                cur = self.__con.cursor()
                cur.execute(sqlInput)
                self.__con.commit()
                return True
                
            except psycopg2.DatabaseError, e:
                return False
                
                
        
        def extractListCol(self, listA, col):
            colList = []
            for i in listA:
                colList.append(i[int(col)])
            return colList
        
        
        # Clean the default COGCC API provided by the state. This should be in the form of 05-xxx-xxxxx
        # This function will remove the dashes and tack on the last four zeros. 
        def cleanCO_API(self,api):
            # Split the provided api into a list using the dashes
            apiSplit = api.split("-")
            # Create the final variable to be returned
            apiConcat = ""
            # Concate the list into a single variable
            for i in apiSplit:
                apiConcat = "%s%s" % (apiConcat, i)
            # Add the final four zeros if len of the current api = 10
            if (len(apiConcat) == 10):
                apiConcat = "%s%s" % (apiConcat, "0000")
            if (len(apiConcat) == 12):
                apiConcat = "%s%s" % (apiConcat, "00")
            return apiConcat

