from phone import Phone

phone_num = '13300592449'
p = Phone()
ok = p.find(phone_num)
with open('province_ch.txt', 'r', encoding="utf-8") as f:
    province_list = f.read().splitlines()
    print(province_list)
index = province_list.index(ok.get('province'))
print(index)
print(ok)
