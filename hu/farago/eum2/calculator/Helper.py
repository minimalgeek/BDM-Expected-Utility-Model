import collections

def tablePrint(data):
    for i, row in enumerate(data):
        for j, value in enumerate(row):
            print('%-8s' % round(value,3), end = ' ')
        print('\n')
        
def dumpclean(obj):
    if type(obj) == dict or type(obj) == collections.OrderedDict:
        for k, v in obj.items():
            if hasattr(v, '__iter__'):
                print(k)
                dumpclean(v)
            else:
                print('%s : %-8s' % (k[:3], round(v,3)), end="")
        print('\n')
    elif type(obj) == list:
        for v in obj:
            if hasattr(v, '__iter__'):
                dumpclean(v)
            else:
                print(v)
        print('\n')
    else:
        print(round(obj,3))
        
def objectListPrint(data):
    for i, row in enumerate(data):
        print(row)
