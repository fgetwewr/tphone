import pymysql
from phone import Phone


class Handle_mysql:

    def __init__(self, host, port, user, database, password):
        self.p = Phone()
        self.db = pymysql.connect(host=host, port=port, user=user, database=database, password=password)
        self.cursor = self.db.cursor()

    def __del__(self):
        self.db.close()

    def count_table(self, province_list):
        sum = 0
        for province in province_list:
            print(province)
            sql = 'select count(phone) from %s' % (province)
            self.cursor.execute(sql)
            count = self.cursor.fetchone()[0]
            sum += count
        print(sum)

    def truncate_table(self, province_list):
        for province in province_list:
            sql = 'truncate table %s;' % (province)
            self.cursor.execute(sql)
        print('总数为%s数据清除成功')


if __name__ == '__main__':
    # 数据库省列表
    with open('province.txt', 'r') as f:
        province_list = f.read().splitlines()

    # 中文省列表
    with open('province_ch.txt', 'r', encoding='utf8') as f:
        province_ch_list = f.read().splitlines()

    handle = Handle_mysql(
        host="192.168.52.110",
        port=3306,
        user="superboy",
        password="Wang123#",
        database="tg"
    )

    handle.count_table(province_list)
    # handle.truncate_table(province_list)


