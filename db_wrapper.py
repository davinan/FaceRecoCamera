import MySQLdb


class db_wrapper():
    def __init__(self):
        self.db = MySQLdb.connect("localhost", "test", "test", "faces")
        self.cursor = self.db.cursor()

    def total_count(self):
        self.cursor.execute("SELECT SUM(COUNT) FROM NAME")
        data = self.cursor.fetchone()
        return int(data[0])

    def age_average(self):
        self.cursor.execute("SELECT AVG(AGE) FROM WHOLE")
        data = self.cursor.fetchone()
        return data[0]

    def gender_ratio(self):
        self.cursor.execute("SELECT AVG(GENDER) FROM WHOLE")
        data = self.cursor.fetchone()
        return data[0]

    def glass_ratio(self):
        self.cursor.execute("SELECT AVG(GLASSES) FROM WHOLE")
        data = self.cursor.fetchone()
        return data[0]

    def add_person_full(self, name, namemod, age, gender, glasses):
        try:
            # Execute the SQL command
            self.cursor.execute("INSERT INTO WHOLE (Name, AGE, GENDER, GLASSES, VISIT) " +
                                "VALUES ('%s', '%d', '%d', '%d', 1)" % (namemod, age, gender, glasses))
            # Commit your changes in the database
            self.db.commit()
            if self.name_count(name) == 0:
                self.cursor.execute("INSERT INTO NAME (NAME, COUNT) VALUES ('%s', '%d')" % (name, 1))
            else:

                self.cursor.execute("UPDATE NAME SET COUNT = COUNT + 1 WHERE Name = '%s'" % name)
            self.db.commit()
        except:
            # Rollback in case there is any error
            self.db.rollback()

    def add_person(self, name, namemod):
        try:
            # Execute the SQL command
            self.cursor.execute("INSERT INTO WHOLE (Name, VISIT) " +
                                "VALUES ('%s', 1)" % namemod)
            # Commit your changes in the database
            self.db.commit()
            self.cursor.execute("UPDATE NAME SET COUNT = COUNT + 1 WHERE Name = '%s'" % name)
        except:
            # Rollback in case there is any error
            self.db.rollback()

    def name_count(self, name):
        self.cursor.execute("SELECT COUNT FROM NAME WHERE NAME = '%s'" % name)
        data = self.cursor.fetchone()
        if data is None:
            return 0
        else:
            return data[0]

    def visit_count(self, name):
        self.cursor.execute("SELECT VISIT FROM WHOLE WHERE NAME = '%s' "
                            "AND AGE = %d AND GENDER = %d" % name)
        data = self.cursor.fetchone()
        if data is None:
            return 0
        else:
            return data[0]

    def max_visit(self):
        self.cursor.execute("SELECT * FROM WHOLE WHERE VISIT = (SELECT MAX(VISIT) FROM WHOLE)")
        data = self.cursor.fetchone()
        return data

    def update_visit(self, name):
        try:
            self.cursor.execute("UPDATE WHOLE SET VISIT = VISIT + 1 WHERE Name = '%s'" % name)
            self.db.commit()
        except:
            self.db.rollback()


if __name__ == "__main__":
    s = db_wrapper()
    # s.add_person("TESTING", 3, 1, 1)
    print(s.update_visit("ALEX"))
