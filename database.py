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

    def data_slice(self, attribute, att_range):
        print attribute
        print att_range

        slices = {} 
        s = []
        for i in range(int(att_range)):
            index = i+1
            statment = "SELECT * FROM election_data_num WHERE party = " + str(index)        
            self.cursor.execute(statment)        
            rows = self.cursor.fetchall()
            slices[index] = rows
            print "dictionary: ", slices
            return slices
            #s.append()
            #s.append(rows)
            #print "dictionary: ", slices
        
