from turtle import color
from PyQt5 import QtCore,QtGui,QtWidgets,Qt
from PyQt5.QtWidgets import*
from PyQt5.QtCore import*
from PyQt5.QtGui import QIcon, QTextCharFormat, QTextCursor, QTextDocument,QPixmap,QFont
import sys
import ChiShenMeCai

class GUI_MainWindow(QtWidgets.QMainWindow):
    def __init__(self,arg=None):
        super(GUI_MainWindow,self).__init__(arg)
        self.setUp(self)
        self.retranslate(self)

    def setUp(self,MainWindow):
        MainWindow.setObjectName("Main Window")
        MainWindow.resize(480,720)
        MainWindow.setFixedSize(480,720) #本行为禁止窗口拉伸
        self.centralWidget = QtWidgets.QTabWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.retranslate(MainWindow)

        MainWindow.setCentralWidget(self.centralWidget)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

#**********************************************************************
        
        ###label###
        self.labelTitle = QtWidgets.QLabel(self.centralWidget)
        self.labelTitle.setGeometry(QtCore.QRect(0,5,480,35))#水平位置,垂直位置,长,高
        self.labelTitle.setText("<font color=%s>%s</font>" %('#FFFFFF',"我是标题🐎🐎🐎🐎🐎🐎🐎🐎🐎🐎🐎🐎🐎🐎🐎🐎🐎🐎🐎🐎🐎🐎: "))
        self.labelTitle.setMidLineWidth(1)
        self.labelTitle.setStyleSheet('background-color: rgb(49, 140, 155)')

        self.labelHeight = QtWidgets.QLabel(self.centralWidget)
        self.labelHeight.setGeometry(QtCore.QRect(20,55,137,15))#水平位置,垂直位置,长,高
        self.labelHeight.setText("<font color=%s>%s</font>" %('#000000',"请输入您的身高(cm):"))
        self.labelHeight.setMidLineWidth(1)
        
        self.labelWeight = QtWidgets.QLabel(self.centralWidget)
        self.labelWeight.setGeometry(QtCore.QRect(171,55,137,15))#水平位置,垂直位置,长,高
        self.labelWeight.setText("<font color=%s>%s</font>" %('#000000',"请输入您的体重(kg):"))
        self.labelWeight.setMidLineWidth(1)

        self.labelBMI = QtWidgets.QLabel(self.centralWidget)
        self.labelBMI.setGeometry(QtCore.QRect(323,55,137,15))#水平位置,垂直位置,长,高
        self.labelBMI.setText("<font color=%s>%s</font>" %('#000000',"您的BMI:"))
        self.labelBMI.setMidLineWidth(1)

        self.labelGoal = QtWidgets.QLabel(self.centralWidget)
        self.labelGoal.setGeometry(QtCore.QRect(20,115,250,15))#水平位置,垂直位置,长,高
        self.labelGoal.setText("<font color=%s>%s</font>" %('#000000',"请选择或者输入您的个人情况/健康目标:"))
        self.labelGoal.setMidLineWidth(1)

        self.labelOught = QtWidgets.QLabel(self.centralWidget)
        self.labelOught.setGeometry(QtCore.QRect(20,172,250,15))#水平位置,垂直位置,长,高
        self.labelOught.setText("<font color=%s>%s</font>" %('#000000',"您今天应该获取的目标营养量为:"))
        self.labelOught.setMidLineWidth(1)

        self.labelBreakfast1 = QtWidgets.QLabel(self.centralWidget)
        self.labelBreakfast1.setGeometry(QtCore.QRect(20,275,250,15))#水平位置,垂直位置,长,高
        self.labelBreakfast1.setText("<font color=%s>%s</font>" %('#000000',"您的早饭吃了些什么呢🥛:"))
        self.labelBreakfast1.setMidLineWidth(1)

        self.labelBreakfast2 = QtWidgets.QLabel(self.centralWidget)
        self.labelBreakfast2.setGeometry(QtCore.QRect(240,275,250,15))#水平位置,垂直位置,长,高
        self.labelBreakfast2.setText("<font color=%s>%s</font>" %('#000000',"您的早饭获取的营养是:"))
        self.labelBreakfast2.setMidLineWidth(1)

        self.labelLunch = QtWidgets.QLabel(self.centralWidget)
        self.labelLunch.setGeometry(QtCore.QRect(20,420,250,15))#水平位置,垂直位置,长,高
        self.labelLunch.setText("<font color=%s>%s</font>" %('#000000',"您的午饭吃了些什么呢🍔:"))
        self.labelLunch.setMidLineWidth(1)

        self.labelSupper = QtWidgets.QLabel(self.centralWidget)
        self.labelSupper.setGeometry(QtCore.QRect(20,560,250,15))#水平位置,垂直位置,长,高
        self.labelSupper.setText("<font color=%s>%s</font>" %('#000000',"晚饭的建议是🥣:"))
        self.labelSupper.setMidLineWidth(1)


        ###textEdit###
        self.textEditHeight = QtWidgets.QTextEdit(self.centralWidget)
        self.textEditHeight.setGeometry(QtCore.QRect(20,75,137,30))
        self.textEditHeight.setObjectName("textEdit")

        self.textEditWeight = QtWidgets.QTextEdit(self.centralWidget)
        self.textEditWeight.setGeometry(QtCore.QRect(171,75,137,30))
        self.textEditWeight.setObjectName("textEdit")

        self.textEditBMI = QtWidgets.QTextEdit(self.centralWidget)
        self.textEditBMI.setGeometry(QtCore.QRect(323,75,75,30))
        self.textEditBMI.setObjectName("textEdit")

        self.textEditAge = QtWidgets.QTextEdit(self.centralWidget)
        self.textEditAge.setGeometry(QtCore.QRect(20,135,50,25))
        self.textEditAge.setText('Age')
        self.textEditAge.setObjectName("textEdit")
        
        self.textEditOught = QtWidgets.QTextEdit(self.centralWidget)
        self.textEditOught.setGeometry(QtCore.QRect(20,190,440,70))
        self.textEditOught.setObjectName("textEdit")

        self.textEditBreakfast1 = QtWidgets.QTextEdit(self.centralWidget)
        self.textEditBreakfast1.setGeometry(QtCore.QRect(20,295,220,100))
        self.textEditBreakfast1.setObjectName("textEdit")

        self.textEditBreakfast2 = QtWidgets.QTextEdit(self.centralWidget)
        self.textEditBreakfast2.setGeometry(QtCore.QRect(240,295,220,100))
        self.textEditBreakfast2.setObjectName("textEdit")

        self.textEditLunch1 = QtWidgets.QTextEdit(self.centralWidget)
        self.textEditLunch1.setGeometry(QtCore.QRect(20,440,220,100))
        self.textEditLunch1.setObjectName("textEdit")

        self.textEditLunch2 = QtWidgets.QTextEdit(self.centralWidget)
        self.textEditLunch2.setGeometry(QtCore.QRect(240,440,220,100))
        self.textEditLunch2.setObjectName("textEdit")

        self.textEditSupper = QtWidgets.QTextEdit(self.centralWidget)
        self.textEditSupper.setGeometry(QtCore.QRect(20,580,440,130))
        self.textEditSupper.setObjectName("textEdit")
        

        ###button###
        self.buttonBMI = QtWidgets.QPushButton(self.centralWidget)
        self.buttonBMI.setGeometry(QtCore.QRect(400,75,75,30)) #水平位置,垂直位置,长,高
        self.buttonBMI.setObjectName("buttonOpen")
        self.buttonBMI.setText("计算BMI")
        self.buttonBMI.clicked.connect(self.calcuateBMI)

        self.buttonConfirm1 = QtWidgets.QPushButton(self.centralWidget)
        self.buttonConfirm1.setGeometry(QtCore.QRect(400,135,75,30)) #水平位置,垂直位置,长,高
        self.buttonConfirm1.setObjectName("buttonConfirm1")
        self.buttonConfirm1.setText("确定")
        self.buttonConfirm1.clicked.connect(self.getAge)

        self.buttonConfirm2 = QtWidgets.QPushButton(self.centralWidget)
        self.buttonConfirm2.setGeometry(QtCore.QRect(365,392,100,30)) #水平位置,垂直位置,长,高
        self.buttonConfirm2.setObjectName("buttonConfirm2")
        self.buttonConfirm2.setText("确定")
        self.buttonConfirm2.clicked.connect(self.fun)
        
        self.buttonConfirm3 = QtWidgets.QPushButton(self.centralWidget)
        self.buttonConfirm3.setGeometry(QtCore.QRect(365,537,100,30)) #水平位置,垂直位置,长,高
        self.buttonConfirm3.setObjectName("buttonConfirm3")
        self.buttonConfirm3.setText("确定")
        self.buttonConfirm3.clicked.connect(self.getLunch)

        ###combo###

        self.goal2 = QtWidgets.QComboBox(self.centralWidget)
        self.goal2.setGeometry(70,135,115,30)
        self.goal2.addItems(['  男性  ',' 女性  '])
        self.goal2.currentIndexChanged[str].connect(self.fun2)
        self.goal2.currentIndexChanged[int].connect(self.fun2)

        self.goal3 = QtWidgets.QComboBox(self.centralWidget)
        self.goal3.setGeometry(180,135,115,30)
        self.goal3.addItems(['  维持体重  ','  增重(全)  ','  增重(肌)  ',' 减重  '])
        self.goal3.currentIndexChanged[str].connect(self.fun3)
        self.goal3.currentIndexChanged[int].connect(self.fun3)

        self.goal4 = QtWidgets.QComboBox(self.centralWidget)
        self.goal4.setGeometry(290,135,115,30)
        self.goal4.addItems(['健康','  高血压  ','  高血脂  ',' 高血糖  '])
        self.goal4.currentIndexChanged[str].connect(self.fun4)
        self.goal4.currentIndexChanged[int].connect(self.fun4)




#**********************************************************************
    def retranslate(self,MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("Main Window","KG"))
    
    goal = {'age':'','gender':'','shape':'','health':''}

    def fun2(self,i):
        self.goal['gender'] = i
    
    def fun3(self,i):
        self.goal['shape'] = i

    def fun4(self,i):
        self.goal['health'] = i

    def getAge(self):
        #goal = {'age':'','gender':'','shape':'','health':''}
        age = self.textEditAge.toPlainText()
        """gender = self.fun1(i)
        shape = self.fun2(i)
        health = self.fun3(i)
        goal['age'] = age
        goal['gender'] = gender
        goal['shape'] = shape
        goal['health'] = health"""
        self.goal['age'] = age
        print(self.goal)
        return self.goal

    def getSupper(self):
        pass

    def fun(self):
        breakfast_nutrition = "蛋白质: "+str(20)+"\n脂肪: "+str(10)+"\n胆固醇: "+str(0.02)+"\n碳水化合物: "+str(100)
        self.textEditBreakfast2.setText(breakfast_nutrition)

    def fun1(self,i):
        print(i)


    def calcuateBMI(self):
        height = int(self.textEditHeight.toPlainText())
        weight = int(self.textEditWeight.toPlainText())
        bmi = weight/pow((height/100),2)
        self.textEditBMI.setText(str(bmi)[:4])
        print('returned bmi ',bmi)
        return float(bmi)


    def defaultGoal(self):
        bmi = float(self.textEditBMI.toPlainText())
        age = int(self.textEditAge.toPlainText())

        print("returned age ",age)
        return age,bmi

    def getLunch(self):
        age,bmi= self.defaultGoal()
        print(self.textEditLunch1.toPlainText())
        s = self.textEditLunch1.toPlainText()
        li = s.split()
        cai_name_li = []
        cai_weight_li = []
        for i in range(len(li)):
            if i % 2 == 0:
                cai_name_li.append(li[i])
            else:
                cai_weight_li.append(int(li[i]))
        print(li)
        print(cai_name_li)
        print(cai_weight_li)


        csm = ChiShenMeCai.ChiShenMe(age, bmi, cai_name_li, cai_weight_li)
        li1,li2,li3=  csm.getChiShenMe(4, [20, 10, 0, 100])
        
        supper = str('')
        lunch_nutrition = str('您摄入的营养是')
        
        for i in range(len(li1)):
            supper += str(li1[i])
            supper += ' '
            supper += str(li2[i])
            supper += '\n'
        self.textEditSupper.setText(supper)

        
        lunch_nutrition = "蛋白质: "+str(li3[0])[:4]+"\n脂肪: "+str(li3[1])[:4]+"\n胆固醇: "+str(li3[2])[:4]+"\n碳水化合物: "+str(li3[3])[:4]
        
    
            
        self.textEditSupper.setText(supper)
        self.textEditLunch2.setText(lunch_nutrition)


        #return cai_name_li, cai_weight_li

    
        
        


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    gui = GUI_MainWindow()
    gui.setUp(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())