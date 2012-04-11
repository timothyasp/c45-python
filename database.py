import MySQLdb

class ElectionDatabase:

    def __init__(self):
        self.db = 0;

    def connect(self):
        self.db = MySQLdb.connect(host="external-db.s123655.gridserver.com",
                                  port=3306, 
                                  user="db123655_cpe466", 
                                  passwd="466cpe466", 
                                  db="db123655_466")
        self.cursor = self.db.cursor()

    def insert_row_num(self, data_tuple):
        self.cursor.execute("INSERT INTO election_data_num(id, party, ideology, race, gender, religion, income, education, age, region, bush_approval, vote)  values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                             data_tuple)      

    def load_data(self):
        statment = "SELECT * FROM election_data_num"
        self.cursor.execute(statment)        
        rows = self.cursor.fetchall()

        return rows

    def slice_by(self, attribute, val, index_set):
        print "column: ", column
        statment = "SELECT * FROM election_data_num WHERE `" + column + "` = " + str(val) 
        print "mysql statement: ", statment
        self.cursor.execute(statment)        
        return self.cursor.fetchall()

    def is_homogenous(self, data):
        return False

    def clean_up_nums(self):
        statement = "truncate table election_data_num"  
        self.cursor.execute(statement)

