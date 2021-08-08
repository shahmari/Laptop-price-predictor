import mysql.connector
from mine_data import miner

Prior_keys = ['Price', 'Mass', 'PanalSize', 'PanalResolution', 'GPUBrand', 'GPUCapacity', 'DiskType', 'RAMType', 'RAMCapacity',
              'CPUSerie', 'CacheCapacity', 'Battery', 'OS', 'Touch', 'Thunderbolt', 'USB4', 'TypeC', 'KeyboardLight', 'Fingerprint', 'DVD']

def check_database(host_, user_, pass_):
    database = mysql.connector.connect(
        host=host_,
        user=user_,
        password=pass_
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
    mycursor.execute("CREATE DATABASE laptop_data")


def create_table(host_, user_, pass_):
    database = mysql.connector.connect(
        host=host_,
        user=user_,
        password=pass_,
        database="laptop_data"
    )
    mycursor = database.cursor()
    execute = 'create table selected_data (Price int, Mass float, PanalSize float, PanalResolution int, GPUBrand int, GPUCapacity int, DiskType int, RAMType int, RAMCapacity int, CPUSerie int, CacheCapacity int, Battery float, OS int, Touch int, Thunderbolt int, USB4 int, TypeC int, KeyboardLight int, Fingerprint int, DVD int)'
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
    sql = "INSERT INTO selected_data (" + \
        string + ") VALUES (" + 19*"%s, " + "%s)"
    for data in fdata:
        if data == None:
            continue
        mined_data = miner(data)
        data_value = []
        for i in Prior_keys:
            data_value.append(mined_data[i])
        val = data_value
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


def get_SQL_data(host_, user_, pass_):
    database = mysql.connector.connect(
        host=host_,
        user=user_,
        password=pass_,
        database="laptop_data"
    )
    mycursor = database.cursor()
    mycursor.execute("SELECT * FROM selected_data")
    myresult = mycursor.fetchall()
    return myresult

def normal_method(data):
    fdata = []
    for d in data:
        if d == None:
            continue
        mined_data = miner(d)
        data_value = []
        for i in Prior_keys:
            data_value.append(mined_data[i])
        fdata.append(data_value)
    return fdata
