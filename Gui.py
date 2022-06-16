from turtle import color
from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from PyQt5.QtWidgets import*
from PyQt5.QtCore import*
from PyQt5.QtGui import QIcon, QTextCharFormat, QTextCursor, QTextDocument, QPixmap, QFont
import sys

from py2neo import Graph, NodeMatcher, RelationshipMatcher

import ChiShenMeCai


class GUI_MainWindow(QtWidgets.QMainWindow):
    def __init__(self, arg=None):
        super(GUI_MainWindow, self).__init__(arg)
        self.setUp(self)
        self.retranslate(self)

    def setUp(self, MainWindow):
        MainWindow.setObjectName("Main Window")
        MainWindow.resize(480, 720)
        MainWindow.setFixedSize(480, 720) #本行为禁止窗口拉伸
        self.centralWidget = QtWidgets.QTabWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.retranslate(MainWindow)

        MainWindow.setCentralWidget(self.centralWidget)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

# **********************************************************************
        
        # ##label###
        self.labelTitle = QtWidgets.QLabel(self.centralWidget)
        self.labelTitle.setGeometry(QtCore.QRect(0, 5, 480, 35))    # 水平位置,垂直位置,长,高
        self.labelTitle.setText("<font color=%s>%s</font>" % ('#FFFFFF',
                                                              "********************基于知识图谱的膳食推荐********************"))
        self.labelTitle.setMidLineWidth(1)
        self.labelTitle.setStyleSheet('background-color: rgb(49, 140, 155)')

        self.labelHeight = QtWidgets.QLabel(self.centralWidget)
        self.labelHeight.setGeometry(QtCore.QRect(20, 55, 137, 15))     # 水平位置,垂直位置,长,高
        self.labelHeight.setText("<font color=%s>%s</font>" % ('#000000', "请输入您的身高(cm):"))
        self.labelHeight.setMidLineWidth(1)
        
        self.labelWeight = QtWidgets.QLabel(self.centralWidget)
        self.labelWeight.setGeometry(QtCore.QRect(171, 55, 137, 15))   # 水平位置,垂直位置,长,高
        self.labelWeight.setText("<font color=%s>%s</font>" % ('#000000', "请输入您的体重(kg):"))
        self.labelWeight.setMidLineWidth(1)

        self.labelBMI = QtWidgets.QLabel(self.centralWidget)
        self.labelBMI.setGeometry(QtCore.QRect(323, 55, 137, 15))  # 水平位置,垂直位置,长,高
        self.labelBMI.setText("<font color=%s>%s</font>" % ('#000000', "您的BMI:"))
        self.labelBMI.setMidLineWidth(1)

        self.labelGoal = QtWidgets.QLabel(self.centralWidget)
        self.labelGoal.setGeometry(QtCore.QRect(20, 115, 250, 15))     # 水平位置,垂直位置,长,高
        self.labelGoal.setText("<font color=%s>%s</font>" % ('#000000', "请选择或者输入您的个人情况/健康目标:"))
        self.labelGoal.setMidLineWidth(1)

        self.labelOught = QtWidgets.QLabel(self.centralWidget)
        self.labelOught.setGeometry(QtCore.QRect(20, 172, 250, 15))    # 水平位置,垂直位置,长,高
        self.labelOught.setText("<font color=%s>%s</font>" % ('#000000', "您今天应该获取的目标营养量为:"))
        self.labelOught.setMidLineWidth(1)

        self.labelBreakfast1 = QtWidgets.QLabel(self.centralWidget)
        self.labelBreakfast1.setGeometry(QtCore.QRect(20, 275, 250, 15))    # 水平位置,垂直位置,长,高
        self.labelBreakfast1.setText("<font color=%s>%s</font>" % ('#000000', "您的早饭吃了些什么呢🥛(g):"))
        self.labelBreakfast1.setMidLineWidth(1)

        self.labelBreakfast2 = QtWidgets.QLabel(self.centralWidget)
        self.labelBreakfast2.setGeometry(QtCore.QRect(240, 275, 250, 15))   # 水平位置,垂直位置,长,高
        self.labelBreakfast2.setText("<font color=%s>%s</font>" % ('#000000', "您的早饭获取的营养是(g):"))
        self.labelBreakfast2.setMidLineWidth(1)

        self.labelLunch1 = QtWidgets.QLabel(self.centralWidget)
        self.labelLunch1.setGeometry(QtCore.QRect(20, 420, 250, 15))  # 水平位置,垂直位置,长,高
        self.labelLunch1.setText("<font color=%s>%s</font>" % ('#000000', "您的午饭吃了些什么呢(g)🍔:"))
        self.labelLunch1.setMidLineWidth(1)

        self.labelLunch2 = QtWidgets.QLabel(self.centralWidget)
        self.labelLunch2.setGeometry(QtCore.QRect(240, 420, 250, 15))  # 水平位置,垂直位置,长,高
        self.labelLunch2.setText("<font color=%s>%s</font>" % ('#000000', "您的早饭获取的营养是(g):"))
        self.labelLunch2.setMidLineWidth(1)

        self.labelSupper = QtWidgets.QLabel(self.centralWidget)
        self.labelSupper.setGeometry(QtCore.QRect(20, 568, 250, 15))    # 水平位置,垂直位置,长,高
        self.labelSupper.setText("<font color=%s>%s</font>" % ('#000000', "晚饭的建议是(g)🥣:"))
        self.labelSupper.setMidLineWidth(1)

        self.labelSupper = QtWidgets.QLabel(self.centralWidget)
        self.labelSupper.setGeometry(QtCore.QRect(240, 568, 250, 15))    # 水平位置,垂直位置,长,高
        self.labelSupper.setText("<font color=%s>%s</font>" % ('#000000', "预计晚饭获取的营养是(g):"))
        self.labelSupper.setMidLineWidth(1)


        # ##textEdit###
        self.textEditHeight = QtWidgets.QLineEdit(self.centralWidget)
        self.textEditHeight.setGeometry(QtCore.QRect(20, 75, 137, 30))
        self.textEditHeight.setText("170")
        self.textEditHeight.setObjectName("textEdit")

        self.textEditWeight = QtWidgets.QLineEdit(self.centralWidget)
        self.textEditWeight.setGeometry(QtCore.QRect(171, 75, 137, 30))
        self.textEditWeight.setText("65")
        self.textEditWeight.setObjectName("textEdit")

        self.textEditBMI = QtWidgets.QLineEdit(self.centralWidget)
        self.textEditBMI.setGeometry(QtCore.QRect(323, 75, 75, 30))
        self.textEditBMI.setText("0")
        self.textEditBMI.setFocusPolicy(QtCore.Qt.NoFocus)
        self.textEditBMI.setObjectName("textEdit")

        # self.textEditAge = QtWidgets.QLineEdit(self.centralWidget)
        # self.textEditAge.setGeometry(QtCore.QRect(20, 135, 50, 25))
        # self.textEditAge.setPlaceholderText("Age")
        # self.textEditAge.setObjectName("textEdit")
        self.textEditAge = QtWidgets.QSpinBox(self.centralWidget)
        self.textEditAge.setGeometry(QtCore.QRect(20, 135, 50, 25))
        self.textEditAge.setRange(10, 90)
        self.textEditAge.setSingleStep(1)
        self.textEditAge.setValue(20)
        self.textEditAge.setObjectName("textEdit")
        self.textEditAge.valueChanged.connect(self.get_bmi_range)
        
        # self.textEditOught = QtWidgets.QTextEdit(self.centralWidget)
        # self.textEditOught.setGeometry(QtCore.QRect(20, 190, 440, 70))
        # self.textEditOught.setFocusPolicy(QtCore.Qt.NoFocus)
        # self.textEditOught.setObjectName("textEdit")

        self.nutri_table = QtWidgets.QTableWidget(1, 5, parent=self.centralWidget)
        # self.nutri_table.setColumnCount(5)
        # self.nutri_table.setRowCount(1)
        self.nutri_table.setHorizontalHeaderLabels(["热量", "蛋白质", "脂肪", "胆固醇", "碳水化合物"])
        self.nutri_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.nutri_table.verticalHeader().setHidden(True)
        self.nutri_table.setGeometry(QtCore.QRect(20, 190, 440, 70))
        # self.nutri_table.setItem()

        self.textEditBreakfast1 = QtWidgets.QTextEdit(self.centralWidget)
        self.textEditBreakfast1.setGeometry(QtCore.QRect(20, 295, 220, 100))
        self.textEditBreakfast1.setObjectName("textEdit")

        self.textEditBreakfast2 = QtWidgets.QTextEdit(self.centralWidget)
        self.textEditBreakfast2.setGeometry(QtCore.QRect(240, 295, 220, 100))
        self.textEditBreakfast2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.textEditBreakfast2.setObjectName("textEdit")

        self.textEditLunch1 = QtWidgets.QTextEdit(self.centralWidget)
        self.textEditLunch1.setGeometry(QtCore.QRect(20, 440, 220, 100))
        self.textEditLunch1.setObjectName("textEdit")

        self.textEditLunch2 = QtWidgets.QTextEdit(self.centralWidget)
        self.textEditLunch2.setGeometry(QtCore.QRect(240,440,220,100))
        self.textEditLunch2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.textEditLunch2.setObjectName("textEdit")

        self.textEditSupper1 = QtWidgets.QTextEdit(self.centralWidget)
        self.textEditSupper1.setGeometry(QtCore.QRect(20,588,220,125))
        self.textEditSupper1.setObjectName("textEdit")
        
        self.textEditSupper2 = QtWidgets.QTextEdit(self.centralWidget)
        self.textEditSupper2.setGeometry(QtCore.QRect(240,588,220,125))
        self.textEditSupper2.setObjectName("textEdit")

        # ##button###
        self.buttonBMI = QtWidgets.QPushButton(self.centralWidget)
        self.buttonBMI.setGeometry(QtCore.QRect(400, 75, 75, 30))  # 水平位置,垂直位置,长,高
        self.buttonBMI.setObjectName("buttonOpen")
        self.buttonBMI.setText("计算BMI")
        self.buttonBMI.clicked.connect(self.calcuateBMI)
        self.buttonBMI.clicked.connect(self.get_bmi_range)

        self.buttonConfirm1 = QtWidgets.QPushButton(self.centralWidget)
        self.buttonConfirm1.setGeometry(QtCore.QRect(400, 135, 75, 30))  # 水平位置,垂直位置,长,高
        self.buttonConfirm1.setObjectName("buttonConfirm1")
        self.buttonConfirm1.setText("确定")
        self.buttonConfirm1.clicked.connect(self.getAge)

        self.buttonConfirm2 = QtWidgets.QPushButton(self.centralWidget)
        self.buttonConfirm2.setGeometry(QtCore.QRect(365, 392, 100, 30))   # 水平位置,垂直位置,长,高
        self.buttonConfirm2.setObjectName("buttonConfirm2")
        self.buttonConfirm2.setText("确定")
        self.buttonConfirm2.clicked.connect(self.fun)
        
        self.buttonConfirm3 = QtWidgets.QPushButton(self.centralWidget)
        self.buttonConfirm3.setGeometry(QtCore.QRect(365, 537, 100, 30))    # 水平位置,垂直位置,长,高
        self.buttonConfirm3.setObjectName("buttonConfirm3")
        self.buttonConfirm3.setText("确定")
        self.buttonConfirm3.clicked.connect(self.getLunch)

        # ##combo###

        self.goal2 = QtWidgets.QComboBox(self.centralWidget)
        self.goal2.setGeometry(70, 135, 100, 30)
        self.goal2.addItems(['  男性  ', ' 女性  '])
        self.goal2.currentIndexChanged[str].connect(self.fun2)
        self.goal2.currentIndexChanged[int].connect(self.fun2)

        self.goal3 = QtWidgets.QComboBox(self.centralWidget)
        self.goal3.setGeometry(180, 135, 100, 30)
        self.goal3.addItems(['  维持体重  ', '  增重(全)  ', '  增重(肌)  ', '  减重  '])
        self.goal3.currentIndexChanged[str].connect(self.fun3)
        self.goal3.currentIndexChanged[int].connect(self.fun3)

        self.goal4 = QtWidgets.QComboBox(self.centralWidget)
        self.goal4.setGeometry(290, 135, 100, 30)
        self.goal4.addItems(['  健康  ', '  高血压  ', '  高血脂  ', '  高血糖  '])
        self.goal4.currentIndexChanged[str].connect(self.fun4)
        self.goal4.currentIndexChanged[int].connect(self.fun4)

# **********************************************************************

    def retranslate(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("Main Window", "KG"))
    
    goal = {'age': '', 'gender': '', 'shape': '', 'health': ''}

    def fun2(self,i):
        self.goal['gender'] = str(i).strip()
    
    def fun3(self,i):
        self.goal['shape'] = str(i).strip()

    def fun4(self,i):
        self.goal['health'] = str(i).strip()

    def getAge(self):
        #goal = {'age':'','gender':'','shape':'','health':''}
        # age = self.textEditAge.toPlainText()
        age = self.textEditAge.text()
        """gender = self.fun1(i)
        shape = self.fun2(i)
        health = self.fun3(i)
        goal['age'] = age
        goal['gender'] = gender
        goal['shape'] = shape
        goal['health'] = health"""
        self.goal['age'] = age
        print(self.goal)
        age, bmi = self.defaultGoal()
        self.csm = ChiShenMeCai.ChiShenMe(age, bmi,self.goal['shape'],self.goal['health'])
        d = self.csm.getNu_YingChi()
        # ought_nutrition = "热量: "+str(d[0])[:4]+"kcal\n蛋白质: "+str(d[1])[:4]+"g\n脂肪: "+str(d[2])[:4]+"g\n胆固醇: "\
        #                   +str(d[3])[:4]+"g\n碳水化合物: "+str(d[4])[:4]+"g"
        # self.textEditOught.setText(str(ought_nutrition))
        _translate = QtCore.QCoreApplication.translate
        for i in range(5):
            temp_item = QtWidgets.QTableWidgetItem()
            if i == 0:
                temp_item.setText(_translate("widget", str(d[i]) + "kcal"))
            else:
                temp_item.setText(_translate("widget", str(d[i]) + "g"))
            self.nutri_table.setItem(0, i, temp_item)

        return self.goal

    def getSupper(self):
        pass

    def fun(self):
        breakfast_nutrition = "蛋白质: "+str(20.2)+"\n脂肪: "+str(10.5)+"\n胆固醇: "+str(0.02)+"\n碳水化合物: "+str(85.3)
        self.textEditBreakfast2.setText(breakfast_nutrition)

    def fun1(self,i):
        print(i)

    def calcuateBMI(self):
        height = int(self.textEditHeight.text())
        weight = int(self.textEditWeight.text())
        bmi = weight/pow((height/100), 2)
        self.textEditBMI.setText(str(bmi)[:4])
        print('returned bmi ', bmi)
        return float(bmi)

    def defaultGoal(self):
        # bmi = float(self.textEditBMI.toPlainText())
        # age = int(self.textEditAge.toPlainText())
        bmi = float(self.textEditBMI.text())
        age = int(self.textEditAge.text())

        print("returned age ", age)
        return age, bmi

    def getLunch(self):
        age, bmi = self.defaultGoal()
        print(self.textEditLunch1.toPlainText())
        s = self.textEditLunch1.toPlainText()
        li = s.split()
        cai_name_li = []
        cai_weight_li = []
        for i in range(len(li)):
            if i % 2 == 0:
                cai_name_li.append(li[i])
            else:
                cai_weight_li.append(int(li[i][:4]))
        print(li)
        print(cai_name_li)
        print(cai_weight_li)


        nu_Lunch = self.csm.addYiChigetNu(cai_name_li, cai_weight_li)   # get lunch nu
        
        li1, li2 = self.csm.getChiShenMe(10, [20, 10, 0, 50])
        li3 = nu_Lunch
        
        supper = str('')
        lunch_nutrition = str('您摄入的营养是')
        
        for i in range(len(li1)):
            supper += str(li1[i])
            supper += ' '
            supper += str(li2[i])[:3]
            supper += '\n'
        self.textEditSupper.setText(supper)

        lunch_nutrition = "蛋白质: "+str(li3[0])[:4]+"\n脂肪: "+str(li3[1])[:4]+"\n胆固醇: "+str(li3[2])[:4]+"\n碳水化合物: "+str(li3[3])[:4]

        self.textEditSupper.setText(supper)
        self.textEditLunch2.setText(lunch_nutrition)

    def get_bmi_range(self):
        age = int(self.textEditAge.text())
        bmi = float(self.textEditBMI.text())
        graph = Graph('bolt://nas.boeing773er.site:7687')
        matcher = NodeMatcher(graph)
        age_node = matcher.match('age', name=age).first()
        r_matcher = RelationshipMatcher(graph)
        edge = r_matcher.match([age_node], r_type="normal_min_bmi").first()
        min_bmi = edge.end_node['name']
        edge = r_matcher.match([age_node], r_type="normal_max_bmi").first()
        max_bmi = edge.end_node['name']
        if bmi != 0:
            if bmi < min_bmi:
                self.goal3.setCurrentIndex(1)
            elif bmi > max_bmi:
                self.goal3.setCurrentIndex(3)
            else:
                self.goal3.setCurrentIndex(0)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    gui = GUI_MainWindow()
    gui.setUp(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
    # get_bmi_range(20, 21)