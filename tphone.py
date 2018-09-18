from phone import Phone
import pymysql


class PhoneData:
    """按照运营商批量生成手机号，并根据归属地存储到数据库"""

    def __init__(self, host, port, user, database, password):
        self.p = Phone()
        self.db = pymysql.connect(host=host, port=port, user=user, database=database, password=password)
        self.cursor = self.db.cursor()

    def __def__(self):
        self.db.close()

    def create_phone(self, prefix_list, province_list, province_cn_list):
        """ 判断手机号归属地，并插入到对应表中 """

        for prefix in prefix_list:
            i = 0
            count = 1
            while i < 100000000:
                # 生成手机号
                phone_num = str(int(prefix) * 100000000 + i)
                i += 1
                # 查找每个手机号的归属地信息
                desc = self.p.find(phone_num)
                # 返回归属的列表下标
                index = province_cn_list.index(desc.get('province'))
                if index:
                    # 如果下标存在，找到对应数据库的表名
                    use_table = province_list[index]
                    # 调入函数，插入到数据库中
                    self.insertdb(use_table, desc, count)
                    count += 1
                else:
                    with open('error.txt', 'w', encoding='utf-8') as f:
                        f.write(phone_num + '\n')

    def insertdb(self, use_table, desc, count):
        """向数据库中插入手机号码"""
        sql = "INSERT INTO %s (phone, pro, city, mark, checked, company) value ('%s', '%s', '%s', 0, 0, '%s')" % \
              (use_table, desc.get('phone'), desc.get('province'), desc.get('city'), desc.get('phone_type'))
        try:
            print(sql)
            self.cursor.execute(sql)
            if count % 1000 == 0:
                self.db.commit()

        except Exception as e:
            print(e)
            self.db.rollback()


def main():

    # 移动号段
    mobile = ['134', '135', '136', '137', '138', '139', '147', '150', '151', '152', '157', '158', '159', '172', '178',
              '182', '183', '184', '187', '188', '198']
    # 联通号段
    unicom = ['130', '131', '132', '145', '155', '156', '166', '171', '175', '176', '185', '186']

    # 电信号段
    telecom = ['133', '149', '153', '173', '177', '180', '181', '189', '199']

    # 数据库省列表
    with open('province.txt', 'r') as f:
        province_list = f.read().splitlines()

    # 中文省列表
    with open('province_ch.txt', 'r', encoding='utf8') as f:
        province_ch_list = f.read().splitlines()

    ph = PhoneData(
        host="192.168.52.110",
        port=3306,
        user="superboy",
        password="123456",
        database="tg"
    )

    ph.create_phone(telecom, province_list, province_ch_list)


if __name__ == '__main__':
    main()