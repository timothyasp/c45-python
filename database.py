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

    def insert_row_string(self, data_tuple):
        self.cursor.execute("INSERT INTO election_data_string(id, party, ideology, race, gender, religion, income, education, age, region, bush_approval, vote)  values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                             data_tuple)      

    def insert_row_num(self, data_tuple):
        self.cursor.execute("INSERT INTO election_data_num(id, party, ideology, race, gender, religion, income, education, age, region, bush_approval, vote)  values(%d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d)",
                             data_tuple)      

    def data_slice(self, attribute, att_range):
        print attribute
        print att_range

 
        for i in range(int(att_range)):
            statment = "SELECT * FROM election_data WHERE party='" + str(i) + "'"      
                    
            print statment 
#   self.cursor.execute("SELECT * FROM election_data_string WHERE political_party %s", (str(i)));   
            rows = self.cursor.fetchall()
            print "Group:"
            for row in rows:
                print row 
        
