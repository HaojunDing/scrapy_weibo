import pymysql

class MysqlIns(object):
    def __init__(self):
        self.db = pymysql.connect(host='117.61.130.177', port=3306, user='root', password='123456', database='scrapy', charset='utf8')
        self.cursor = self.db.cursor()

    def execute_ins(self, sql, data):
        try:
            self.cursor.execute(sql, data)
            self.db.commit()
        except Exception as e:
            print(e)
            self.db.rollback()

    def __del__(self):
        self.cursor.close()
        self.db.close()

if __name__ == '__main__':
    sql = 'insert into test (title, zan) VALUES (%s, %s)'
    data = ('贴了', 2)
    myhelper = MysqlIns()
    myhelper.execute_ins(sql, data)