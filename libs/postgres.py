import psycopg2

class connection():
    def __init__(self, host, dbname, user, password, conn, script, variable):

        # connection parameter
        self.host = host
        self.dbname = dbname
        self.user = user
        self.password = password

        # connection objects
        self.conn = conn

        # SQL script & variable
        self.script = script
        self.variable = variable
    
    def getConnectionObject(self):
        # judge if parameter is exist or not
        if self.host and self.dbname and self.user and self.password:
            # combine connection string
            conn_string = "host={0} user={1} dbname={2} password={3}".format(self.host, self.user, self.dbname, self.password)
            # establish connection to database
            conn = psycopg2.connect(conn_string)
            print("connection to postgres database successfully")

            return conn

    def query(self):
        # judge if connection object is exist or not
        if self.conn and self.script:
            # get cursor object (from current connection object)
            cursor = self.conn.cursor()

            # execute specified SQL script
            cursor.execute(self.script)
            # get all result and initialize variable as a list
            rows = cursor.fetchall()
            
            # commit SQL script
            self.conn.commit()

            return rows
    
    def createTable(self):
        # judge if SQL is exist or not
        if self.script:
            # get cursor object (from current connection object)
            cursor = self.conn.cursor()

            # execute specified SQL script
            cursor.execute(self.script)

            # commit SQL script
            self.conn.commit()

            return 'table created successfully'

    def insert(self):
        # judge if SQL is exist or not
        if self.script:
            # get cursor object (from current connection object)
            cursor = self.conn.cursor()

            if self.variable:
                # execute specified SQL script with variable
                cursor.execute(self.script, self.variable)
            elif self.variable == '':
                # execute specified SQL script with variable
                cursor.execute(self.script)


            # commit SQL script
            self.conn.commit()

            # calculate rows which insert into table successfully
            row = cursor.rowcount
            result = '{0} row(s) had been insert'.format(row)

            return result
    
    def update(self):
        #judge if SQL and its variable is exist or not
        if self.script and self.variable:
            # get cursor object (from current connection object)
            cursor = self.conn.cursor()

            # execute specified SQL script with variable
            cursor.execute(self.script, self.variable)
            
            # commit SQL script
            self.conn.commit()

            # calculate rows which update from table successfully
            row = cursor.rowcount
            result = '{0} row(s) had been affected'.format(row)

            return result

    def delete(self):
        #judge if SQL and its variable is exist or not
        if self.script and self.variable:
            # get cursor object (from current connection object)
            cursor = self.conn.cursor()

            # execute specified SQL script with variable
            cursor.execute(self.script, self.variable)
            
            # commit SQL script
            self.conn.commit()

            # calculate rows which delete from table successfully
            row = cursor.rowcount
            result = '{0} row(s) had been deleted'.format(row)

            return result

    def release(self):
        cursor = self.conn.cursor()
        # release cursor object
        cursor.close()
        # release connection object
        self.conn.close()