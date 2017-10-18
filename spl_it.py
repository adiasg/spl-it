import pandas
import numpy as np
from flask import jsonify

def checkAllClear(data):
    for d in data:
        if(d!=0):
            return False
    return True

def getSplit(rate, eaten, paid):
    eaten = eaten[rate.index]
    eaten = eaten.fillna(0)

    print('###################### Rate ######################')
    print(rate)
    print('---------------------------------------------------')
    print('###################### Eaten ######################')
    print(eaten)
    print('---------------------------------------------------')

    amount = pandas.DataFrame()
    amount['Total'] = eaten.apply(lambda row: np.dot(row,rate).sum(), axis=1)

    paid = paid.fillna(0)
    print('###################### Paid ######################')
    print(paid)
    print('---------------------------------------------------')
    amount = amount.join(paid)
    amount['Debt'] = amount.apply(lambda row: (row['Total']-row['Paid']).round(1), axis=1)
    amount['Debt'] = amount['Debt'].astype(int)

    print('###################### Amount ######################')
    print(amount)
    print('---------------------------------------------------')
    print('Total Amount:', amount['Total'].sum())
    print('Total Paid:', amount['Paid'].sum())
    print('Total Debt:', amount['Debt'].sum())
    print('')

    pos = amount['Debt'][amount['Debt']>0]
    neg = amount['Debt'][amount['Debt']<0]

    settle = {}
    for person in amount.index:
        settle[person] = []

    while not checkAllClear(neg):
        pos = pos.sort_values()
        neg = neg.sort_values()
        print('###################### Debt ######################')
        print(pos)
        print(neg)
        print('---------------------------------------------------')
        if pos[-1] < -neg[0]:
            settle[pos.index[-1]].append( {neg.index[0]: pos[-1]} )
            settle[neg.index[0]].append( {pos.index[-1]: -pos[-1]} )
            neg[0] += pos[-1]
            pos[-1] = 0
        else:
            settle[pos.index[-1]].append( {neg.index[0]: -neg[0]} )
            settle[neg.index[0]].append( {pos.index[-1]: neg[0]} )
            pos[-1] -= -neg[0]
            neg[0] = 0

    print('###################### Final Debt ######################')
    print(pos)
    print(neg)
    print('---------------------------------------------------')

    print(settle)
    return settle


if __name__ == '__main__':
    rate = pandas.read_csv('item-rates.csv', index_col=0)
    eaten = pandas.read_csv('item-person-split.csv', index_col=0)
    paid = pandas.read_csv('paid.csv', index_col=0)
    getSplit(rate, eaten, paid)
