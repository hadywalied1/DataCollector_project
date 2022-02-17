import os
import socket
import sys
from flask import Flask
from flask import Flask, send_file
from flask import request
from flask import Response
import json
from entities import *
from flask_sqlalchemy import SQLAlchemy
from flask import render_template
import pandas as pd
from flask import send_file

if getattr(sys, 'frozen', False):
    template_folder = os.path.join(sys._MEIPASS, 'templates')
    static_folder = os.path.join(sys._MEIPASS, 'static')
    app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
else:
    app = Flask(__name__)
    
# determine if application is a script file or frozen exe
if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
elif __file__:
    application_path = os.path.dirname(__file__)

config_path = os.path.join(application_path, ".\\res\\database.db")

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+ config_path
db = SQLAlchemy(app)

class Data (db.Model):
    id = db.Column("id", db.Integer, primary_key = True)
    name = db.Column("name",db.String(100), unique = False, nullable = True)
    # weight and length data
    weight = db.Column("weight", db.Numeric(precision=2), unique = False, nullable  = True)
    height = db.Column("height", db.Numeric(precision=2), unique = False, nullable = True)
    #hand power data
    leftHandGripData =  db.Column("leftHandGripData", db.Numeric(precision=2), unique = False, nullable  = True)
    rightHandGripData =  db.Column("rightHandGripData", db.Numeric(precision=2), unique = False, nullable  = True)
    legsAndBackData =  db.Column("legsAndBackData", db.Numeric(precision=2), unique = False, nullable  = True)
    #effort data 
    effortMarkData =  db.Column("effortMarkData", db.Numeric(precision=2), unique = False, nullable  = True)
    effortTimeData =  db.Column("effortTimeData", db.Numeric(precision=2), unique = False, nullable  = True)
    # hand stability data
    firstWrongCount = db.Column("firstWrongCount", db.Numeric(precision=2), unique = False, nullable = True)
    firstTotalTime = db.Column("firstTotalTime", db.Numeric(precision=2), unique = False, nullable = True)
    firstAvg = db.Column("firstAvg", db.Numeric(precision=2), unique = False, nullable = True)
    secondWrongCount = db.Column("secondWrongCount", db.Numeric(precision=2), unique = False, nullable = True)
    secondTotalTime = db.Column("secondTotalTime", db.Numeric(precision=2), unique = False, nullable = True)
    secondAvg = db.Column("secondAvg", db.Numeric(precision=2), unique = False, nullable = True)
    thirdWrongCount = db.Column("thirdWrongCount", db.Numeric(precision=2), unique = False, nullable = True)
    thirdTotalTime = db.Column("thirdTotalTime", db.Numeric(precision=2), unique = False, nullable = True)
    thirdAvg = db.Column("thirdAvg", db.Numeric(precision=2), unique = False, nullable = True)
    handStabilityDegree =  db.Column("handStabilityDegree", db.Numeric(precision=2), unique = False, nullable  = True)
    # depth data 
    depthTrialTrain = db.Column("depthTrialTrain", db.Numeric(precision=2), unique = False, nullable  = True)
    depthTrial1 = db.Column("depthTrial1", db.Numeric(precision=2), unique = False, nullable  = True)
    depthTrial2 = db.Column("depthTrial2", db.Numeric(precision=2), unique = False, nullable  = True)
    depthData = db.Column("depthData", db.Numeric(precision=2), unique = False, nullable  = True)
    #hearing data
    leftEarDegree = db.Column("leftEarDegree", db.String(100), unique = False, nullable  = True)
    leftEarTones = db.Column("leftEarTones", db.Numeric(precision=2), unique = False, nullable  = True)
    rightEarDegree =  db.Column("rightEarDegree", db.String(100), unique = False, nullable  = True)
    rightEarTones =  db.Column("rightEarTones", db.Numeric(precision=2), unique = False, nullable  = True)
    #arms data
    firstArmsErrors= db.Column("firstArmsErrors", db.Numeric(precision=2), unique = False, nullable = True)
    firstArmsTime= db.Column("firstArmsTime", db.Numeric(precision=2), unique = False, nullable = True)
    firstArmsAverage= db.Column("firstArmsAverage", db.Numeric(precision=2), unique = False, nullable = True)
    secondArmsErrors= db.Column("secondArmsErrors", db.Numeric(precision=2), unique = False, nullable = True)
    secondArmsTime= db.Column("secondArmsTime", db.Numeric(precision=2), unique = False, nullable = True)
    secondArmsAverage= db.Column("secondArmsAverage", db.Numeric(precision=2), unique = False, nullable = True)
    thirdArmsErrors= db.Column("thirdArmsErrors", db.Numeric(precision=2), unique = False, nullable = True)
    thirdArmsTime= db.Column("thirdArmsTime", db.Numeric(precision=2), unique = False, nullable = True)
    thirdArmsAverage= db.Column("thirdArmsAverage", db.Numeric(precision=2), unique = False, nullable = True)
    armsData = db.Column("armsData", db.Numeric(precision=2), unique = False, nullable  = True)
    
    def as_dict(self):
        return {'id':self.id,
                'name': self.name,
                
                'height': self.height,
                'weight': self.weight,
                
                'effortMarkData':self.effortMarkData,
                'effortTimeData':self.effortTimeData, 
                
                'rightHandGripData':self.rightHandGripData,
                'leftHandGripData':self.leftHandGripData, 
                'legsAndBackData':self.legsAndBackData ,
                
                'firstWrongCount':self.firstWrongCount,
                'firstTotalTime':self.firstTotalTime,
                'firstAvg':self.firstAvg,
                'secondWrongCount':self.secondWrongCount,
                'secondTotalTime':self.secondTotalTime,
                'secondAvg':self.secondAvg,
                'thirdWrongCount':self.thirdWrongCount,
                'thirdTotalTime':self.thirdTotalTime,
                'thirdAvg':self.thirdAvg,
                'handStabilityDegree':self.handStabilityDegree,
                
                'rightEarDegree':self.rightEarDegree,
                'rightEarTones':self.rightEarTones,
                'leftEarDegree':self.leftEarDegree,
                'leftEarTones':self.leftEarTones,
                
                'depthTrialTrain':self.depthTrialTrain, 
                'depthTrial1':self.depthTrial1, 
                'depthTrial2':self.depthTrial2, 
                'depthData':self.depthData, 
                
                'firstArmsErrors':self.firstArmsErrors, 
                'firstArmsTime':self.firstArmsTime, 
                'firstArmsAverage':self.firstArmsAverage,
                'secondArmsErrors':self.secondArmsErrors, 
                'secondArmsTime':self.secondArmsTime, 
                'secondArmsAverage':self.secondArmsAverage,
                'thirdArmsErrors':self.thirdArmsErrors, 
                'thirdArmsTime':self.thirdArmsTime, 
                'thirdArmsAverage':self.thirdArmsAverage,
                'armsData':self.armsData
                }
    def as_list(self):
        return [self.id,
                self.name,
                
                self.height,
                self.weight,
                
                self.effortMarkData,
                self.effortTimeData, 
                
                self.rightHandGripData,
                self.leftHandGripData, 
                self.legsAndBackData ,
                
                self.firstWrongCount,
                self.firstTotalTime,
                self.firstAvg,
                self.secondWrongCount,
                self.secondTotalTime,
                self.secondAvg,
                self.thirdWrongCount,
                self.thirdTotalTime,
                self.thirdAvg,
                self.handStabilityDegree,
                
                self.rightEarDegree,
                self.rightEarTones,
                self.leftEarDegree,
                self.leftEarTones,
                
                self.depthTrialTrain, 
                self.depthTrial1, 
                self.depthTrial2, 
                self.depthData, 
                
                self.firstArmsErrors, 
                self.firstArmsTime, 
                self.firstArmsAverage,
                self.secondArmsErrors, 
                self.secondArmsTime, 
                self.secondArmsAverage,
                self.thirdArmsErrors, 
                self.thirdArmsTime, 
                self.thirdArmsAverage,
                self.armsData
                ]
    
    
    
@app.route("/handPower", methods = ["POST"])
def handPower():
    print(request.get_json())
    print(type(request.json))
    data = request.json
    try:
        obj = Data.query.filter_by(id= data["id"]).first()
        if(obj == None):
            user = Data(id = data["id"],name = data["name"],
                        leftHandGripData = data["leftHandGripData"],
                        rightHandGripData = data["rightHandGripData"],
                        legsAndBackData = data["legsAndBackData"]
                        )
            db.session.add(user)
            db.session.commit()
        else :
            obj.leftHandGripData = data["leftHandGripData"]
            obj.rightHandGripData = data["rightHandGripData"]
            obj.legsAndBackData = data["legsAndBackData"]
            db.session.commit()
        
        resp =json.dumps({"status":True, "message":"Successful"})
        response = Response(status=200,content_type= "application/json; charset=utf-8")
        response.set_data(resp)
        return response
    except Exception as e:
        err = "Error: "+ str(e)
        resp =json.dumps({"status":False, "message":err})
        response = Response(status=400,content_type= "application/json; charset=utf-8")
        response.set_data(resp)
        return response


@app.route("/weightHeight", methods = ["POST"])
def weightHeight():
    print(request.get_json())
    print(type(request.json))
    data = request.json
    try:
        obj = Data.query.filter_by(id= data["id"]).first()
        if(obj == None):
            user = Data(id = data["id"],
                        name = data["name"],
                        weight = data["weight"],
                        height= data["height"])
            db.session.add(user)
            db.session.commit()
        else :
            obj.weight = data["weight"]
            obj.height = data["height"]
            db.session.commit()
        
        resp =json.dumps({"status":True, "message":"Successful"})
        response = Response(status=200,content_type= "application/json; charset=utf-8")
        response.set_data(resp)
        return response
    except Exception as e:
        err = "Error: "+ str(e)
        resp =json.dumps({"status":False, "message":err})
        response = Response(status=400,content_type= "application/json; charset=utf-8")
        response.set_data(resp)
        return response

@app.route("/effortMeasure", methods = ["POST"])
def EffortMeasure():
    print(request.get_json())
    print(type(request.json))
    data = request.json
    try:
        obj = Data.query.filter_by(id= data["id"]).first()
        if(obj == None):
            user = Data(id = data["id"],name = data["name"],
                        effortMarkData = data["effortMarkData"],
                        effortTimeData=60)
            db.session.add(user)
            db.session.commit()
        else :
            obj.effortMarkData = data["effortMarkData"]
            obj.effortTimeData = 60
            db.session.commit()
        
        resp =json.dumps({"status":True, "message":"Successful"})
        response = Response(status=200,content_type= "application/json; charset=utf-8")
        response.set_data(resp)
        return response
    except Exception as e:
         err = "Error: "+ str(e)
         resp =json.dumps({"status":False, "message":err})
         response = Response(status=400,content_type= "application/json; charset=utf-8")
         response.set_data(resp)
         return response


@app.route("/handStability", methods = ["POST"])
def HandStability():
    print(request.get_json())
    print(type(request.json))
    data = request.json
    try:
        obj = Data.query.filter_by(id= data["id"]).first()
        if(obj == None):
            user = Data(id = data["id"],name = data["name"],
                        firstWrongCount=data["firstWrongCount"],
                        firstTotalTime=data["firstTotalTime"],
                        firstAvg=data["firstAvg"],
                        secondWrongCount=data["secondWrongCount"],
                        secondTotalTime=data["secondTotalTime"],
                        secondAvg=data["secondAvg"],
                        thirdWrongCount=["thirdWrongCount"],
                        thirdTotalTime=["thirdTotalTime"],
                        thirdAvg=["thirdAvg"],
                        handStabilityDegree = data["handStabilityDegree"]
                        )
            db.session.add(user)
            db.session.commit()
        else :
            obj.firstWrongCount = data["firstWrongCount"]
            obj.firstTotalTime = data["firstTotalTime"]
            obj.firstAvg = data["firstAvg"]
            obj.secondWrongCount = data["secondWrongCount"]
            obj.secondTotalTime = data["secondTotalTime"]
            obj.secondAvg = data["secondAvg"]
            obj.thirdWrongCount = data["thirdWrongCount"]
            obj.thirdTotalTime = data["thirdTotalTime"]
            obj.thirdAvg = data["thirdAvg"]
            obj.handStabilityDegree = data["handStabilityDegree"]
        
            db.session.commit()
        
        resp =json.dumps({"status":True, "message":"Successful"})
        response = Response(status=200,content_type= "application/json; charset=utf-8")
        response.set_data(resp)
        return response
    except Exception as e:
          err = "Error: "+ str(e)
          resp =json.dumps({"status":False, "message":err})
          response = Response(status=200,content_type= "application/json; charset=utf-8")
          response.set_data(resp)
          return response    

@app.route("/depth", methods = ["POST"])
def depth():
    print(request.get_json())
    print(type(request.json))
    data = request.json
    try:
        obj = Data.query.filter_by(id= data["id"]).first()
        if(obj == None):
            user = Data(id = data["id"],name = data["name"],
                        depthTrialTrain=data["depthTrialTrain"],
                        depthTrial1=data["depthTrial1"],
                        depthTrial2=data["depthTrial2"],
                        depthData = data["depthData"])

            db.session.add(user)
            db.session.commit()
        else :
            obj.depthTrialTrain=data["depthTrialTrain"]
            obj.depthTrial1=data["depthTrial1"]
            obj.depthTrial2=data["depthTrial2"]
            obj.depthData = data["depthData"]
            db.session.commit()
        
        resp =json.dumps({"status":True, "message":"Successful"})
        response = Response(status=200,content_type= "application/json; charset=utf-8")
        response.set_data(resp)
        return response
    except Exception as e:
          err = "Error: "+ str(e)
          print(err)
          resp =json.dumps({"status":False, "message":err})
          response = Response(status=400,content_type= "application/json; charset=utf-8")
          response.set_data(resp)
          return response
        

@app.route("/hearing", methods = ["POST"])
def hearing():
    print(request.get_json())
    print(type(request.json))
    data = request.json
    try:
        obj = Data.query.filter_by(id= data["id"]).first()
        if(obj == None):
            user = Data(id = data["id"],name = data["name"],
                        leftEarDegree = data["leftEarDegree"],
                        leftEarTones = data["leftEarTones"],
                        rightEarDegree = data["rightEarDegree"],
                        rightEarTones = data["rightEarTones"]
                        )
            db.session.add(user)
            db.session.commit()
        else :
            obj.leftEarDegree = data["leftEarDegree"]
            obj.leftEarTones = data["leftEarTones"]
            obj.rightEarDegree = data["rightEarDegree"]
            obj.rightEarTones = data["rightEarTones"]
            db.session.commit()
        
        resp =json.dumps({"status":True, "message":"Successful"})
        response = Response(status=200,content_type= "application/json; charset=utf-8")
        response.set_data(resp)
        return response
    except Exception as e:
         err = "Error: "+ str(e)
         resp =json.dumps({"status":False, "message":err})
         response = Response(status=400,content_type= "application/json; charset=utf-8")
         response.set_data(resp)
         return response

@app.route("/arms", methods = ["POST"])
def arms():
    print(request.get_json())
    print(type(request.json))
    data = request.json
    try:
        obj = Data.query.filter_by(id= data["id"]).first()
        if(obj == None):
            user = Data(id = data["id"],name = data["name"],
                            firstArmsErrors=data["firstArmsErrors"],
                            firstArmsTime=data["firstArmsTime"],
                            firstArmsAverage=data["firstArmsAverage"],
                            secondArmsErrors=data["secondArmsErrors"],
                            secondArmsTime=data["secondArmsTime"],
                            secondArmsAverage=data["secondArmsAverage"],
                            thirdArmsErrors=data["thirdArmsErrors"],
                            thirdArmsTime=data["thirdArmsTime"],
                            thirdArmsAverage=data["thirdArmsAverage"],
                            armsData = data["armsData"])
            db.session.add(user)
            db.session.commit()
        else :
            obj.firstArmsErrors = data["firstArmsErrors"]
            obj.firstArmsTime = data["firstArmsTime"]
            obj.firstArmsAverage = data["firstArmsAverage"]
            obj.secondArmsErrors = data["secondArmsErrors"]
            obj.secondArmsTime = data["secondArmsTime"]
            obj.secondArmsAverage = data["secondArmsAverage"]
            obj.thirdArmsErrors = data["thirdArmsErrors"]
            obj.thirdArmsTime = data["thirdArmsTime"]
            obj.thirdArmsAverage = data["thirdArmsAverage"]
            obj.armsData = data["armsData"]
            db.session.commit()
        
        resp =json.dumps({"status":True, "message":"Successful"})
        response = Response(status=200,content_type= "application/json; charset=utf-8")
        response.set_data(resp)
        return response
    except Exception as e:
        err = "Error: "+ str(e)
        print(err)
        resp =json.dumps({"status":False, "message":err})
        response = Response(status=400,content_type= "application/json; charset=utf-8")
        response.set_data(resp)
        return response
            
@app.route("/gettingData", methods = ["GET"])
def gettingData():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    print(request.remote_addr, local_ip)
    if(request.environ.get('HTTP_X_REAL_IP', request.remote_addr) == local_ip
       or request.environ.get('HTTP_X_REAL_IP', request.remote_addr) == '127.0.0.1'):          
        data = Data.query.all()
        return render_template('getData.html', len = len(data) ,Data=data)
    return render_template('index.html')

@app.route("/download_excel", methods = ["GET"])
def download_excel():
    data = Data.query.all()
    print([(x.id, x.name) for x in data])
    column1 = ["بيانات المختبرين", "الإختبارات البدنية", "الإختبارات العملية"]
    column2 = ["جهاز التناسق", "جهاز بذل الجهد	", "جهاز قياس قوة القبضة والظهر والقدمين	"
               , "جهاز ثبات اليد	", "جهاز قياس شدة السمع	", "جهاز ادراك العمق	", "تآزر الذراعين"]
    column3 = ["الإختبار الأول	", "الإختبار الثاني	", "الإختبار الثالث	", "الدرجة", "الأذن اليمني	", "الأذن اليسري	", 
               "الإختبار الأول ","الإختبار الثاني ","الإختبار الثالث "," الدرجة",]
    column4 = ["الرقم العسكري"
               , "الاسم"
               
               , "الطول"
               , "الوزن"
               
               , "زمن"
               , "درجة"
               
               , "قبضة اليد اليمني	"
               , "قبضة اليد اليسري	"
               , "الظهر والقدمين"
               
               , "عدد الأخطاء	"
               , "الزمن الكلي للأخطاء"
               , "المتوسط"
               , "عدد الأخطاء"
               , "الزمن الكلي للأخطاء"
               , "المتوسط"
               , "عدد الأخطاء"
               , "الزمن الكلي للأخطاء"
               ,"المتوسط"
               , " "
               
               , "عدد النغمات المسموعة"
               , "الدرجة"
               , "عدد النغمات المسموعة"
               , "الدرجة"
               
               , "المحاولة التدريبية"
               ,"المحاولة الأختبارية"
               ,"2المحاولة الأختبارية"
               , "الدرجة المعيارية"
               
               , "عدد الأخطاء"
               , "الزمن الكلي للأخطاء"
               , "المتوسط"
               , "عدد الأخطاء"
               , "الزمن الكلي للأخطاء"
               , "المتوسط"
               ,"عدد الأخطاء	"
               , "الزمن الكلي للأخطاء"
               , "المتوسط"
               , " "]
    
    columns = ['الرقم العسكري', 'الاسم', 'الوزن', 'الطول','قبضة اليد اليمني','قبضة اليد اليسري','الظهر والقدمين'
               ,'درجة بذل الجهد','زمن بذل الجهد','ثبات اليد','إدراك العمق',
               '(درجة)الأذن اليمني', '(عدد)الأذن اليمني	', '(درجة)الأذن اليسري	', '(عدد)الأذن اليسري	', 'تآزر الذراعين']
    dataDict = [x.as_list() for x in data]
    print(dataDict)
    df = pd.DataFrame(dataDict,columns=column4)
    print(df)
    file =  os.path.join(application_path,'.\\res\\data.xlsx')
    excelWriter = pd.ExcelWriter(file, engine='xlsxwriter')
    df.to_excel(excelWriter, sheet_name='Sheet1', startrow=4, header=False)
    workbook  = excelWriter.book
    worksheet = excelWriter.sheets['Sheet1']
    format1 = workbook.add_format({'num_format': '0'})
    # Add a header format.
    header_format = workbook.add_format({
    'bold': True,
    'text_wrap': True,
    'reading_order': 1,
    'valign': 'top',
    'align':'right',
    'fg_color': '#D7E4BC',
    'border': 1})
    
    for col_num, value in enumerate(df.columns.values):
        worksheet.write(3, col_num + 1, value, header_format)
    
    center_format = workbook.add_format({
    'bold': True,
    'text_wrap': True,
    'reading_order': 1,
    'align': 'center',
    'border': 1,
    'fg_color': '#D7E4BC',
    'valign': 'vcenter'})                
    worksheet.merge_range("B1:C1", column1[0], center_format)
    worksheet.merge_range("D1:J1" ,column1[1], center_format)
    worksheet.merge_range("K1:AL1" ,column1[2], center_format)
    
    worksheet.merge_range("D2:E2" ,column2[0], center_format)
    worksheet.merge_range("F2:G2" ,column2[1], center_format)
    worksheet.merge_range("H2:J2" ,column2[2], center_format)
    worksheet.merge_range("K2:T2" ,column2[3], center_format)
    worksheet.merge_range("U2:X2" ,column2[4], center_format)
    worksheet.merge_range("Y2:AB2" ,column2[5], center_format)
    worksheet.merge_range("AC2:AL2" ,column2[6], center_format)
    
    worksheet.merge_range("K3:M3" ,column3[0], center_format)
    worksheet.merge_range("N3:P3" ,column3[1], center_format)
    worksheet.merge_range("Q3:S3" ,column3[2], center_format)
    worksheet.write("T3" ,column3[3], center_format)
    worksheet.merge_range("U3:V3" ,column3[4], center_format)
    worksheet.merge_range("W3:X3" ,column3[5], center_format)
    worksheet.merge_range("AC3:AE3" ,column3[6], center_format)
    worksheet.merge_range("AF3:AH3" ,column3[7], center_format)
    worksheet.merge_range("AI3:AK3" ,column3[8], center_format)
    worksheet.write("AL3" ,column3[9], center_format)
    
    worksheet.set_column('B1:AN1', 18, format1)
    excelWriter.save()
    return send_file(file, as_attachment=True)

@app.route("/upload", methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        print(request.files['file'])
        f = request.files['file']
        data_xls = pd.read_excel(f)
        importData(data_xls)    
        return '''
    <!doctype html>
    <link rel="stylesheet" href="static/css/bootstrap.min.css">
    <div class="row " dir="rtl">
    <div class="col-lg-3 ">
    </div>
     <div class="col-lg-6 text-center">
        <title>Upload an excel file</title>
        <h1 >تم رفع الملف بنجاح</h1>
        <button class="btn btn-success" style="margin-top:20px;" onclick='location.href = "/gettingData"' type="button">
                            <span>عرض البيانات</span>
        </button>
    </div>
    </div>

    '''
    return '''
    <!doctype html>
    <link rel="stylesheet" href="static/css/bootstrap.min.css">
    <div class="row " dir="rtl">
    <div class="col-lg-3 ">
    </div>
    <div class="col-lg-6 text-center">
        <title>Upload an excel file</title>
        <h1 >رفع ملف الاكسل </h1>
        <form action="" method=post enctype=multipart/form-data>
        <div class="form-group">
        <p><input class="form-control" accept="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" style="margin-top:20px;"  type=file class="form-control" name=file>
        <input  class="btn btn-primary" style="margin-top:20px;" type=submit value=رفع>
        </div>
        </div>
        
    </div>
     </form>
    '''
def importData(df):
    Data.query.delete()
    
    df.drop([0,1,2], inplace = True)
    df.columns = [
                '#',
                'id',
                'name',
                'height',
                'weight',
                'effortMarkData',
                'effortTimeData', 
                'rightHandGripData',
                'leftHandGripData', 
                'legsAndBackData' ,
                'firstWrongCount',
                'firstTotalTime',
                'firstAvg',
                'secondWrongCount',
                'secondTotalTime',
                'secondAvg',
                'thirdWrongCount',
                'thirdTotalTime',
                'thirdAvg',
                'handStabilityDegree',
                'rightEarDegree',
                'rightEarTones',
                'leftEarDegree',
                'leftEarTones',
                'depthTrialTrain', 
                'depthTrial1', 
                'depthTrial2', 
                'depthData', 
                'firstArmsErrors', 
                'firstArmsTime', 
                'firstArmsAverage',
                'secondArmsErrors', 
                'secondArmsTime', 
                'secondArmsAverage',
                'thirdArmsErrors', 
                'thirdArmsTime', 
                'thirdArmsAverage',
                'armsData'
    ]
    for index, row in df.iterrows():
        data = Data(
            id = row["id"], name = row["name"],
            height = row["height"], weight = row["weight"],
            effortMarkData = row["effortMarkData"], effortTimeData = row["effortTimeData"],
            rightHandGripData = row["rightHandGripData"], leftHandGripData = row["leftHandGripData"],
            legsAndBackData = row["legsAndBackData"], firstWrongCount = row["firstWrongCount"],
            firstTotalTime = row["firstTotalTime"], firstAvg = row["firstAvg"],
            secondWrongCount = row["secondWrongCount"], secondTotalTime = row["secondTotalTime"],
            secondAvg = row["secondAvg"], thirdWrongCount = row["thirdWrongCount"],
            thirdTotalTime = row["thirdTotalTime"], thirdAvg = row["thirdAvg"],
            handStabilityDegree = row["handStabilityDegree"], rightEarDegree = row["rightEarDegree"],
            rightEarTones = row["rightEarTones"], leftEarDegree = row["leftEarDegree"],
            leftEarTones = row["leftEarTones"], depthTrialTrain = row["depthTrialTrain"],
            depthTrial1 = row["depthTrial1"], depthTrial2 = row["depthTrial2"],
            depthData = row["depthData"], firstArmsErrors = row["firstArmsErrors"],
            firstArmsTime = row["firstArmsTime"], firstArmsAverage = row["firstArmsAverage"],
            secondArmsErrors = row["secondArmsErrors"], secondArmsTime = row["secondArmsTime"],
            secondArmsAverage = row["secondArmsAverage"], thirdArmsErrors = row["thirdArmsErrors"],
            thirdArmsTime = row["thirdArmsTime"], thirdArmsAverage = row["thirdArmsAverage"],
            armsData = row["armsData"]
                    )
        db.session.add(data)
        print(type(row))
    db.session.commit()

@app.route("/delete", methods=['GET', 'POST'])
def delete_all():    
    Data.query.delete()
    db.session.commit()
    return    '''
     <!doctype html>
    <link rel="stylesheet" href="static/css/bootstrap.min.css">
    <div class="row " dir="rtl">
    <div class="col-lg-3 ">
    </div>
     <div class="col-lg-6 text-center">
        <title>Deleted Successfully </title>
        <h1 >تم مسح البيانات بنجاح</h1>
        <button class="btn btn-success" style="margin-top:20px;" onclick='location.href = "/gettingData"' type="button">
                            <span>عرض البيانات</span>
        </button>
    </div>
    </div>
    '''

if __name__ == "__main__":
    # ensure the instance folder exists
    try:
        os.makedirs(application_path+"\\res")
    except OSError:
        pass

    db.create_all()
    app.run(debug = False, host="0.0.0.0", use_reloader = False)
    