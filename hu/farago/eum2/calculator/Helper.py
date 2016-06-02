def tablePrint(data):
    for i, row in enumerate(data):
        for j, value in enumerate(row):
            print('%-8s' % value, end = ' ')
        print('\n')
        
def objectListPrint(data):
    for i, row in enumerate(data):
        print(row)