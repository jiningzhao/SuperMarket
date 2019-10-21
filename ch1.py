from pymongo import MongoClient
from flask import Flask,request,render_template
import time
conn=MongoClient('127.0.0.1',27017)
	#连接MongoDB，‘127.0.0.1’是本机的IP地址，27017是默认端口
db=conn.supermarket
	# 连接mydoc文档，没有则自动创建
my_enter=db.enter
my_takein=db.takein
my_takeout=db.takeout
my_takeout_true=db.takeout_true
linshi=db.linshi
my_DB=db.all_db
	# 使用test_set集合，没有则自动创建
app = Flask(__name__)

@app.route('/')
def Enter():
    return render_template('登录.html',data='')
@app.route('/signin')
def SIGNIN():
    username1=''
    password1 = request.args.get('password1')
    password2 = request.args.get('password2')
    username = request.args.get('username')
    for i in my_enter.find({'username':username}):
        username1=i.get('username')
    if password1!=password2:
        data='两次密码输入不同！'
        return render_template('注册.html', data=data)
    elif username1 != '':
        data='账号已经存在'
        return render_template('注册.html', data=data)
    elif username == None:
        data='账号不能为空'
        return render_template('注册.html', data=data)
    elif password1==password2 and  password1 != None and username1=='' and username !=None and username!='':
        my_enter.insert({'username': username, 'password': password1})
        return render_template('登录.html')
    else:
        return render_template('注册.html', data='')

@app.route('/login')
def hello_world():
    password1=''
    username=request.args.get('username')
    password=request.args.get('password')
    for i in my_enter.find({'username':username}):
        password1=i.get('password')
    if password == password1 and username != '' and password != '':
        my_takeout.remove()
        return render_template('首页.html')
    return render_template('登录.html',data='您输入的账号或密码错误！')


@app.route('/takein')
def IN():
    sum1=0
    for i in my_DB.find():
        sum1+=1
    date=time.strftime('%Y-%m-%d',time.localtime(time.time()))
    no=sum1+1
    code = request.args.get('code')
    name=request.args.get('name')
    price=request.args.get('price',type=float)
    value=request.args.get('value',type=float)
    number=request.args.get('number',type=int)
    vendor=request.args.get('vendor')
    gg=request.args.get('gg')
    if code != None and code != '':
        if no==1:
            my_DB.insert({'no': no, 'code': code, 'name': name, 'price': price,'value':value,'vendor':vendor,'gg':gg, 'number': number})
        i = my_DB.find({'code': code}).count()
        if i!= 0:
            for j in my_DB.find({'code': code}):
                sum = number + int(j.get('number'))
                my_DB.update({'code': code}, {'$set': {'number': sum}})
        else:
            my_DB.insert({'no': no, 'code': code, 'name': name, 'price': price, 'value': value, 'vendor': vendor, 'gg': gg,'number': number})
        my_takein.insert({'no': no, 'code': code, 'name': name, 'price': price,'value':value, 'vendor': vendor, 'gg': gg, 'number': number, 'time': date})
        sum1 = 0
        for i in my_DB.find():
            sum1 += 1
        no = sum1 + 1
        return render_template('进货.html', time=date,no=no)
    return render_template('进货.html',time=date,no=no)


@app.route('/takeout')
def OUT():
    data=[]
    sum1=0
    sum2=0
    A=request.args.get('A',type=float)
    code = request.args.get('code')
    number = request.args.get('number',type=int)
    date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    if code != None and code != '':
        for i in my_DB.find({'code':code}):
            all_pay = float(i['value']) * number
            my_takeout.insert({'code':i.get('code'),'name':i.get('name'),'value':i.get('value'),'number':number,'all_pay':all_pay,'time':date})
            my_takeout_true.insert({'code': i.get('code'), 'name': i.get('name'), 'value': i.get('value'), 'number': number,'all_pay': all_pay, 'time': date})
    for j in my_takeout.find():
        sum1+=j.get('all_pay')
        if type(A)==float:
            sum2=A-sum1
        data.append(dict(code=j.get('code'), name=j.get('name'), value=j.get('value'), number=j.get('number'), all_pay=j.get('all_pay'),time=j.get('time')))
    return render_template('售货.html',data=data,sum1=sum1,sum2=sum2)

@app.route('/select_takein')
def SIN():
    data=[]
    code=request.args.get('code')
    name=request.args.get('name')
    date1=request.args.get('date1')
    if code!=None and code != '':
        for i in my_takein.find({'code':code}):
            data.append(dict(no=i.get('no'), code=i.get('code'), name=i.get('name'), price=i.get('price'),number=i.get('number'),time=i.get('time')))
            if date1 != None and date1 != '':
                for j in range(len(data)):
                   if  data[j]['time'] != date1:
                       data.pop(j)
    elif name != None and name!='':
        for i in my_takein.find({'name':name}):
            data.append(dict(no=i.get('no'), code=i.get('code'), name=i.get('name'), price=i.get('price'),number=i.get('number'), time=i.get('time')))
            if date1 != None and date1 != '':
                for j in range(len(data)):
                   if  data[j]['time'] != date1:
                       data.pop(j)
    else:
        pass
    return render_template('进货查询.html',data=data)

@app.route('/select_takeout')
def SOUT():
    data = []
    code = request.args.get('code')
    name = request.args.get('name')
    date1 = request.args.get('date1')
    if code != None and code != '':
        for i in my_takeout_true.find({'code': code}):
            data.append(dict(no=i.get('no'), code=i.get('code'), name=i.get('name'), value=i.get('value'),number=i.get('number'),all_pay=i.get('all_pay'), time=i.get('time')))
            if date1 != None and date1 != '':
                for j in range(len(data)):
                    if data[j]['time'] != date1:
                        data.pop(j)
    elif name != None and name != '':
        for i in my_takeout_true.find({'name': name}):
            data.append(dict(no=i.get('no'), code=i.get('code'), name=i.get('name'), value=i.get('value'),number=i.get('number'),all_pay=i.get('all_pay'), time=i.get('time')))
            if date1 != None and date1 != '':
                for j in range(len(data)):
                    if data[j]['time'] != date1:
                        data.pop(j)
    else:
        pass
    return render_template('售货查询.html',data=data)
@app.route('/select_DB')
def SDB():
    data = []
    code = request.args.get('code')
    name = request.args.get('name')
    if code != None and code != '':
        for i in my_DB.find({'code': code}):
            data.append(dict(no=i.get('no'), code=i.get('code'), name=i.get('name'),price=i.get('price'), value=i.get('value'),number=i.get('number'),vendor=i.get('vendor'),gg=i.get('gg')))
    elif name != None and name != '':
        for i in my_DB.find({'code': code}):
            data.append(dict(no=i.get('no'), code=i.get('code'), name=i.get('name'),price=i.get('price'), value=i.get('value'),number=i.get('number'),vendor=i.get('vendor'),gg=i.get('gg')))
    else:
        pass
    return render_template('库存查询.html',data=data)
@app.route('/menu')
def MENU():
    maba=[]
    for i in my_takeout.find():
        maba.append(dict(code=i.get('code'),number=i.get('number')))
    for i in maba:
        for j in my_DB.find({'code':i['code']}):
         my_DB.update({'code': i['code']}, {'$set': {'number': j.get('number')-i['number']}})

    my_takeout.remove()
    return render_template('首页.html')

if __name__ == '__main__':
    app.run()


