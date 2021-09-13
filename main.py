from adder import join_group
from time import sleep
from join import enter
group = input("send link to the froup to scrape")
link = input("where you want to add them")
user_phones = ['639381545561',  '639566736010', '639650635604',
               '639438769086',  '639754052600', '639356069153', '639218821356', '639701793314', '639360395458']
n = 0
rule = input(
    "0: all, 1: recently, 2: online,\n3: exact day, 4: since day + online + recently")

need = int(input("Number of users"))
enter(user_phones, group, link)
print("done entering")
sleep(3)
n = 0


while n != need:
    for i in range(len(user_phones)):
        try:
            n += join_group(user_phones[i], group,
                            link, n, rule)
            sleep(10*60)
        except Exception as e:
            print(e)
