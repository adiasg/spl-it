from flask import Flask, render_template, request
import pandas
from spl_it import getSplit

app = Flask(__name__)

@app.route('/')
def serve_index():
    return render_template('index.html')

@app.route('/split', methods=['GET','POST'])
def serve_split():
    if request.method == 'GET':
        return render_template('split_input_1.html')
    else:
        return render_template('split_input_2.html', num_people=int(request.form['people']), num_items=int(request.form['items']), people=[ i for i in range(1,int(request.form['people'])+1) ], items=[ i for i in range(1,int(request.form['items'])+1) ])

@app.route('/processing', methods=['POST'])
def serve_processing():
        print('Processing')
        print(request.form)
        data = request.form
        num_people = int(data['people'])
        num_items = int(data['items'])
        items = [ data['item'+str(i)] for i in range(1,num_items+1) ]
        people = [ data['person'+str(i)] for i in range(1,num_people+1) ]
        print('No. of people', num_people)
        print('No. of items', num_items)

        rate = pandas.DataFrame(columns=['Item','Rate'])
        rate.set_index('Item', inplace=True)
        for i in range(1,num_items+1):
            #d = {'Item': data['item'+str(i)], 'Rate': data['item'+str(i)+'-rate']}
            s = pandas.Series( {'Rate': data['item'+str(i)+'-rate']}, name=data['item'+str(i)])
            rate = rate.append(s,verify_integrity=True)
        rate['Rate'] = rate['Rate'].astype(int)
        print(rate)

        paid = pandas.DataFrame(columns=['Person','Paid'])
        paid.set_index('Person', inplace=True)
        for i in range(1,num_people+1):
            d = {'Person': data['person'+str(i)], 'Paid': data['person'+str(i)+'-paid']}
            # print(d)
            s = pandas.Series( {'Paid': int(data['person'+str(i)+'-paid'])}, name=data['person'+str(i)])
            paid = paid.append(s,verify_integrity=True)
        #paid['Paid'] = paid['Paid'].astype(int)
        print(paid)

        print(rate.index)
        print(paid.index)

        eaten = pandas.DataFrame(columns=rate.index.copy(), index=paid.index.copy())
        print(eaten)

        for p in range(1,num_people+1):
            for i in range(1,num_items+1):
                person = data['person'+str(p)]
                item = data['item'+str(i)]
                #print(person)
                #print(item)
                s = 'person'+str(p)+'-'+'item'+str(i)
                #print(s)
                eaten.loc[person][item] = float(data['person'+str(p)+'-'+'item'+str(i)])
        print(eaten)

        return render_template('display_split.html', split=getSplit(rate,eaten,paid))

if __name__ == '__main__':
    app.run(debug=True)
