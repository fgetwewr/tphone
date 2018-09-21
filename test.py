from phone import Phone


def test():
    phone_num = '13300001251'
    p = Phone()
    with open('province.txt', 'r') as f:
        province_list = f.read().splitlines()

    with open('province_ch.txt', 'r', encoding="utf-8") as f:
        province_ch_list = f.read().splitlines()

    try:

        desc = p.find(phone_num)
        # print(desc)
        # 返回归属的列表下标
        index = province_ch_list.index(desc.get('province'))
        # print(desc.get('province'), index)
        if index is not None:
            # 如果下标存在，找到对应数据库的表名
            use_table = province_list[index]
            insert_value(use_table, desc)


        else:
            with open('errorlog/descerror.txt', 'a', encoding='utf-8') as f:
                f.write(phone_num + '\n')
    # 无用手机号
    except Exception as e:
        with open('errorlog/NoneType.txt', 'a', encoding='utf-8') as f:
            f.write(phone_num + '\n')

def insert_value(use_table, desc):
    string = "('%s', '%s', '%s', 0, 0, '%s')" % (
    desc.get('phone'), desc.get('province'), desc.get('city'), desc.get('phone_type'))
    a = {}.fromkeys([use_table], [string])
    d = a.get(use_table)
    b = ('13300001251', '广西', '南宁', 0, 0, '电信')
    d.append(b)
    print(a)
    print(d)
    e = (i for i in d)
    print(e)


def insertdb(self, use_table, desc, count):
    """向数据库中插入手机号码"""
    value_list = []

    sql = "INSERT INTO %s (phone, pro, city, mark, checked, company) values ('%s', '%s', '%s', 0, 0, '%s')" % \
          (use_table, desc.get('phone'), desc.get('province'), desc.get('city'), desc.get('phone_type'))
    try:
        print('第%s个' % count + sql)
        self.cursor.execute(sql)
        if count % 1000 == 0:
            self.db.commit()
    # 写入数据库错误
    except Exception as e:
        with open('errorlog/sqlerrorlog.txt', 'a', encoding='utf8') as f:
            f.write(str(e) + '\n')
        self.db.rollback()

test()