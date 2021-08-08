from sklearn import tree
import os
from get_raw_modules import get_raw_data as grd
from SQL_modules import *

url = 'https://www.digikala.com/search/category-notebook-netbook-ultrabook/?has_selling_stock=1&pageno={}&sortby=4'

print('welcome to laptop price predictor!')

setting_check = os.path.isfile('./setting')

if setting_check == True:
    print('Setting file found. do you want to change the setting? [y]/[n]')
    change_setting = input(' >>  ')
    while True:
        if change_setting in ['y', 'n']:
            break
        else:
            print('Please respond correctly. try again:')
            change_setting = input(' >>  ')
    if change_setting == 'y':
        print(
            'do you want to use SQL? ([y]/[n])')
        choice = input(' >>  ')
        while True:
            if choice in ['y', 'n']:
                break
            else:
                print('Please respond correctly. try again:')
                choice = input(' >>  ')
        host = user = password = ""
        if choice == 'y':
            print('Please enter your server information:')
            host = input('Enter your host name (for example localhost): ')
            user = input('Enter your username (for example root): ')
            password = input('Enter your password: ')
        with open('setting', 'w') as setting:
            setting.write(choice+'\n'+host+'\n'+user+'\n'+password)

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
    print(
        'do you want to use SQL for saving and reading data? ([y]/[n])')
    choice = input(' >>  ')
    while True:
        if choice in ['y', 'n']:
            break
        else:
            print('Please respond correctly. try again:')
            choice = input(' >>  ')
    host = user = password = ""
    if choice == 'y':
        print('Please enter your server information:')
        host = input('Enter your host name (for example localhost): ')
        user = input('Enter your username (for example root): ')
        password = input('Enter your password: ')
    print('Do you want to save changes and your information? [y]/[n]')
    dosave = input(' >>  ')
    while True:
        if dosave in ['y', 'n']:
            break
        else:
            print('Please respond correctly. try again:')
            dosave = input(' >>  ')
    if dosave == 'y':
        with open('setting', 'w') as setting:
            setting.write(choice+'\n'+host+'\n'+user+'\n'+password)


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
        print('adding data to the server...', end='')
        add_data(host, user, password, data)
        print('\rData added!')
    else:
        print('do you want to update data? [y]/[n]')
        doUpdate = input(' >>  ')
        while True:
            if doUpdate in ['y', 'n']:
                break
            else:
                print('Please respond correctly. try again:')
                doUpdate = input(' >>  ')
        if doUpdate == 'y':
            print('Updating...', end='')
            delete_data(host, user, password)
            create_table(host, user, password)
            data = grd(url)
            add_data(host, user, password, data)
            print('\rUpdating Completed!')

x = []
y = []
if choice == 'y':
    data = get_SQL_data(host, user, password)
else:
    data = normal_method(grd(url))
for line in data:
    x.append(list(line[1:]))
    y.append(line[0])

clf = tree.DecisionTreeClassifier()
clf = clf.fit(x, y)

while True:
    sample = []
    print('Enter properties of the desired laptop:')
    sample.append(
        float(input('Enter the desired weight in kilograms (for example: 2.1):  >> ')))
    sample.append(
        float(input('Enter the desired panel size in inches (for example: 15.5):  >> ')))
    s = input('Enter the desired panel resolution (for example: 1366*768):  >> ')
    sample.append(int(s[0]) * int(s[1]))
    print("Select the desired GPU manufacturer (enter the number only):")
    sample.append(
        int(input('1_AMD, 2_ATI, 3_Apple, 4_Intel, 5_NVIDIA  >> '))-1)
    sample.append(int(input(
        'Enter the desired GPU capacity in MB (for example: 4000 or if you dont want this part enter 0):  >> ')))
    print("Select the desired disk type (enter the number only):")
    sample.append(int(input('1_SSD, 2_eMMC, 3_hybrid, 4_HDD  >> '))-1)
    print("Select the desired RAM type (enter the number only):")
    sample.append(int(input('1_DDR3, 2_DDR4  >> '))+2)
    sample.append(
        int(input('Enter the desired RAM capacity in GB (for example: 16):  >> ')))
    print("Select the desired CPU serie (enter the number only):")
    sample.append(int(input('1_Core i7, 2_Pentium, 3_M1, 4_Ryzen 3, 5_Bristol Ridge, 6_A6, 7_Core i5, 8_Core i9, 9_Celeron, 10_Ryzen 5, 11_Core i3, 12_ATHLON, 13_Ryzen 7, 14_Quad Core  >> '))-1)
    sample.append(
        int(input('Enter the desired Cache capacity in MB (for example: 4):  >> ')))
    sample.append(
        float(input('Enter the desired Battery charging in Whr (for example: 45):  >> ')))
    print("Select the desired options (enter the number only):")
    sample.append(int(input('Have OS: 1_no 2_yes:  >> '))-1)
    sample.append(int(input('Have Touch screen: 1_no 2_yes:  >> '))-1)
    sample.append(int(input('Have Thunderbolt: 1_no 2_yes:  >> '))-1)
    sample.append(int(input('Have USB4: 1_no 2_yes:  >> '))-1)
    sample.append(int(input('Have Type-C: 1_no 2_yes:  >> '))-1)
    sample.append(int(input('Have Keyboard Light: 1_no 2_yes:  >> '))-1)
    sample.append(int(input('Have Fingerprint sensor: 1_no 2_yes:  >> '))-1)
    sample.append(int(input('Have DVD-R: 1_no 2_yes:  '))-1)
    print("your desired price is about", clf.predict([sample])[0], 'Tooman')
    print('do you want to continue? [y]/[n]')
    doContinue = input(' >>  ')
    while True:
        if doContinue in ['y', 'n']:
            break
        else:
            print('Please respond correctly. try again:')
            doContinue = input(' >>  ')
    if doContinue == 'n':
        break
