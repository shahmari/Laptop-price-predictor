import os
from get_raw_modules import get_raw_data as grd
import mysql.connector
from mine_data import miner


url = 'https://www.digikala.com/search/category-notebook-netbook-ultrabook/?has_selling_stock=1&pageno={}&sortby=4'

print('welcome to laptop price predictor!')

setting_check = os.path.isfile('./setting')

if setting_check == True:
    with open('setting', 'r') as setting:
        settext = setting.read().split('\n')
    if settext[0] == 'y':
        choice = settext[0]
        host = settext[1]
        user = settext[2]
        password = settext[3]
    else:
        choice = 'n'

else:
    print('we use normal file saving method by default. do you want to change it to SQL? ([y]/[n])')
    choice = input('>> ')
    while True:
        if choice in ['y', 'n']:
            break
        else:
            print('Please respond correctly. try again:')
            choice = input('>> ')
    host = user = password = ""
    if choice == 'y':
        print('Please enter your server information:')
        host = input('Enter your host name (for example localhost): ')
        user = input('Enter your username (for example root): ')
        password = input('Enter your password: ')
    print('Do you want to save changes and your information? [y]/[n]')
    dosave = input('>> ')
    while True:
        if dosave in ['y', 'n']:
            break
        else:
            print('Please respond correctly. try again:')
            dosave = input('>> ')
    if dosave == 'y':
        with open('setting', 'w') as setting:
            setting.write(choice+'\n'+host+'\n'+user+'\n'+password)


def check_database(host_, user_, pass_):
    database = mysql.connector.connect(
        host = host_ ,
        user = user_ ,
        password = pass_
    )
    mycursor = database.cursor()
    mycursor.execute("SHOW DATABASES")
    if ("laptop_data",) in mycursor:
        return True
    else:
        return False

def check_table(host_, user_, pass_):
    database = mysql.connector.connect(
        host=host_,
        user=user_,
        password=pass_,
        database="laptop_data"
    )
    mycursor = database.cursor()
    mycursor.execute("SHOW TABLES")
    if ("selected_data",) in mycursor:
        return True
    else:
        return False

def create_database(host_, user_, pass_):
    database = mysql.connector.connect(
        host=host_,
        user=user_,
        password=pass_
    )
    mycursor = database.cursor()
    mycursor.execute("CREATE DATABASES laptop_data")

def create_table(host_, user_, pass_):
    database = mysql.connector.connect(
        host=host_,
        user=user_,
        password=pass_,
        database="laptop_data"
    )
    mycursor = database.cursor()
    execute = 'create table selected_data (Price int, Mass float, PanalSize float, PanalResolution int, GPUBrand varchar(255), GPUCapacity int, DiskType int, RAMType int, RAMCapacity int, CPUSerie varchar(255), CacheCapacity int, Battery float, OS int, Touch int, Thunderbolt int, USB4 int, TypeC int, KeyboardLight int, Fingerprint int, DVD int)'
    mycursor.execute(execute)

def check_data(host_, user_, pass_):
    database = mysql.connector.connect(
        host=host_,
        user=user_,
        password=pass_,
        database="laptop_data"
    )
    mycursor = database.cursor()
    mycursor.execute("SELECT * FROM selected_data")
    myresult = mycursor.fetchall()
    if myresult == []:
        return False
    else:
        return True

def add_data(host_, user_, pass_, fdata):
    database = mysql.connector.connect(
        host=host_,
        user=user_,
        password=pass_,
        database="laptop_data"
    )

    mycursor = database.cursor()
    string = 'Price, Mass, PanalSize, PanalResolution, GPUBrand, GPUCapacity, DiskType, RAMType, RAMCapacity, CPUSerie, CacheCapacity, Battery, OS, Touch, Thunderbolt, USB4, TypeC, KeyboardLight, Fingerprint, DVD'
    sql = "INSERT INTO selected_data (" + string + ") VALUES (" + 19*"%s, " + "%s)"
    for data in fdata:
        if data == None:
            continue
        val = list(miner(data).values())
        mycursor.execute(sql, val)
        database.commit()

def delete_data(host_, user_, pass_):
    database = mysql.connector.connect(
        host=host_,
        user=user_,
        password=pass_,
        database="laptop_data"
    )

    mycursor = database.cursor()
    sql = "DROP TABLE selected_data"
    mycursor.execute(sql)


if choice == 'y':
    if check_database(host, user, password) == True:
        if check_table(host, user, password) == False:
            create_table(host, user, password)
    else:
        create_database(host, user, password)
        create_table(host, user, password)
    if check_data(host, user, password) == False:
        print('Getting data from the source...', end='')
        data = grd(url)
        print('\rData received!')
        print('adding data to the server...',end='')
        add_data(host, user, password, data)
        print('\rData added!')
    else:
        print('do you want to update data? [y]/[n]')
        doUpdate = input('>> ')
        while True:
            if doUpdate in ['y', 'n']:
                break
            else:
                print('Please respond correctly. try again:')
                doUpdate = input('>> ')
        if doUpdate == 'y':
            print('Updating...', end='')
            delete_data(host, user, password)
            create_table(host, user, password)
            data = grd(url)
            add_data(host, user, password, data)
            print('\rUpdating Completed!')
