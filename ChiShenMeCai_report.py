from scipy import optimize as op
import numpy as np
import sys
from py2neo import Node, Relationship, Graph, NodeMatcher, RelationshipMatcher

class ChiShenMe:
    # 构造函数
    def __init__(self, age=20, bmi=20, gender="m", JianKangMuBiao="", JiBing=""):
        self.age = age
        self.bmi = bmi
        self.gender = gender
        self.JianKangMuBiao = JianKangMuBiao
        self.JiBing = JiBing
        '''self.cai_name_li = cai_name_li
        self.cai_weight_li = cai_weight_li'''
        self.graph = Graph('bolt://nas.boeing773er.site:7687')
        self.dish_name, self.nu_cai = self.getCai()
        self.Nu_YiChi = np.array([0, 0, 0, 0])
        # 菜的单位为 克
    

    def clearNu_YiChi(self):
        self.Nu_YiChi = np.array([0, 0, 0, 0])


    # 通过健康目标与疾病，修改应吃营养成分量
    def changeYingChi_by_JKMBandJB(self, nl, dbz, zf, dgc, cho):
        JKMB_li = ["增重（全）", "增重（肌）", "减重"]
        JB_li = ["高血压", "高血脂", "高血糖"]
        rate = 0.85
        if self.JiBing in JB_li:
            if self.JiBing == JB_li[0]:
                zf *= rate
                cho *= rate
            elif self.JiBing == JB_li[1]:
                dbz /= rate
                zf *= rate
                dgc *= rate
            elif self.JiBing == JB_li[2]:
                zf *= rate
                cho *= rate
                dgc *= rate
        else:
            if self.JianKangMuBiao == JKMB_li[0]:
                nl /= rate
                dbz /= rate
                zf /= rate
                dgc /= rate
                cho /= rate
            elif self.JianKangMuBiao == JKMB_li[1]:
                nl /= (1-(1-rate)/2)
                dbz /= rate
            elif self.JianKangMuBiao == JKMB_li[2]:
                nl *= rate
                dbz *= rate
                zf *= rate
                dgc *= rate
                cho *= rate
        
        return nl, dbz, zf, dgc, cho
    

    # 获取应吃营养成分
    # 根据身高、体重、BMI查询，这个人应该摄入多少营养成分
    # 返回值：[能量，蛋白质，脂肪，胆固醇，CHO]
    def getNu_YingChi(self):
        age, bmi = self.age, self.bmi

        node_matcher = NodeMatcher(self.graph)
        relation_matcher = RelationshipMatcher(self.graph)
        nl = dbz = zf = dgc = cho = 0

        age_node = node_matcher.match("age", name = age).first()
        print(age_node)
        
        max_kcal_relation = relation_matcher.match(
            [age_node],
            r_type="max_kcal"
        ).first()
        max_kcal = int(max_kcal_relation.end_node['name'][:-4])

        min_kcal_relation = relation_matcher.match(
            [age_node],
            r_type='min_kcal'
        ).first()
        min_kcal = int(min_kcal_relation.end_node['name'][:-4])

        max_bmi_relation = relation_matcher.match(
            [age_node],
            r_type='normal_max_bmi'
        ).first()
        max_bmi = float(max_bmi_relation.end_node['name'])

        min_bmi_relation = relation_matcher.match(
            [age_node],
            r_type='normal_min_bmi'
        ).first()
        min_bmi = float(min_bmi_relation.end_node['name'])

        if max_kcal - min_kcal <= 200:
            if bmi > (max_bmi - min_bmi) / 2:
                nl = min_kcal
            else:
                nl = max_kcal
        else:
            if bmi > max_bmi:
                nl = min_kcal
            elif bmi < min_bmi:
                nl = max_kcal
            else:
                nl = (max_kcal + min_kcal) / 2
        
        kcal_node = node_matcher.match("kcal", name = str(int(nl))+'kcal').first()
        
        nu_relation = relation_matcher.match(
            nodes = [kcal_node],
            r_type = None
        )

        for i in list(nu_relation):
            val = float(i['value'])
            if i.end_node['name'] == 'CHO（g）':
                cho = val
            elif  i.end_node['name'] == '胆固醇（mg）':
                dgc = val / 1000
            elif  i.end_node['name'] == '脂肪（g）':
                zf = val
            elif  i.end_node['name'] == '蛋白质（g）':
                dbz = val
        
        # gender related
        m_f_rate = 0.95
        if self.gender == 'f':
            nl *= m_f_rate
            dbz *= m_f_rate
            zf *= m_f_rate
            dgc *= m_f_rate
            cho *= m_f_rate
        
        nl, dbz, zf, dgc, cho = self.changeYingChi_by_JKMBandJB(nl, dbz, zf, dgc, cho)

        print('cho ' + str(cho))
        print('dgc ' + str(dgc))
        print('zf  ' + str(zf))
        print('dbz ' + str(dbz))
        print('nl  ' + str(nl))
        
        # [能量，蛋白质，脂肪，胆固醇，CHO]
        return [nl, dbz, zf, dgc, cho]


    # [蛋白质，脂肪，胆固醇，CHO]
    def getCai(self):
        node_matcher = NodeMatcher(self.graph)
        dish_nodes = node_matcher.match("Dish")
        
        dish_name = []
        nu_cai = np.zeros((4,0))
        for i in list(dish_nodes):
            dish_dict = dict(i)
            dish_name.append(dish_dict['name'])

            dbz = float(dish_dict['粗蛋白(g)'])
            zf = float(dish_dict['粗脂肪(g)'])
            dgc = float(dish_dict['胆固醇(mg)']/1000)
            cho = float(dish_dict['总碳水化合物(g)'])
            
            this_cai = np.array([[dbz], [zf], [dgc], [cho]])
            nu_cai = np.append(nu_cai, this_cai, axis = 1)

        return dish_name, nu_cai


    # 获取每种营养成分已经吃了多少
    def getNu_YiChi(self, cai_li, cai_weight, nu_cai, dish_name):
        nu_YiChi = np.array([0, 0, 0, 0])
        i = 0
        for cai in cai_li:
            if cai in dish_name:
                nu_YiChi = nu_YiChi + nu_cai[:, dish_name.index(cai)] * cai_weight[i] / 300.00      # 200
            i += 1
        return nu_YiChi


    # 通过菜名和质量，获取各个营养成分的总和
    def getNuFromCai(self, nu_cai, cai_weight_li):
        cai_weight_li = np.array(cai_weight_li)
        cai_weight_li = cai_weight_li / 300.0
        nu = nu_cai * cai_weight_li.reshape((1, cai_weight_li.shape[0]))
        nu = np.dot(nu, np.ones((nu.shape[1], 1)))
        return nu
    

    # 添加一顿饭，返回这顿饭营养成分
    def addYiChigetNu(self, cai_name_li, cai_weight_li):
        thistime_nu_YiChi = self.getNu_YiChi(cai_name_li, cai_weight_li, self.nu_cai, self.dish_name)
        self.Nu_YiChi = self.Nu_YiChi + thistime_nu_YiChi
        return thistime_nu_YiChi


    # 获取晚饭吃什么，外部调用的函数
    def getChiShenMe(self, cai_num, else_nu_Yichi = [0,0,0,0]):
        # self.cai_name_li = cai_name_li
        # self.cai_weight_li = cai_weight_li

        self.dish_name, self.nu_cai = self.getCai()
        
        # 已吃-营养成分向量（4）
        nu_YiChi = self.Nu_YiChi
        nu_YiChi = nu_YiChi + np.array(else_nu_Yichi)
        # 应吃-营养成分向量（5）
        nu_YingChi = self.getNu_YingChi()  # age, bmi
        nu_YingChi = nu_YingChi[1:]     # 去除 能量

        # 相减得到：每种营养成分剩余摄入量
        # 求 剩余-营养成分向量（4）
        nu_Sheng = nu_YingChi - nu_YiChi    # 剩余 应该吃的营养成分量 [能量，蛋白质，脂肪，胆固醇，CHO]
        nu_Sheng = nu_Sheng.reshape((4, 1))

        # 最大值的函数的系数数组
        c = self.nu_cai / nu_Sheng
        c = np.dot(np.ones((1, 4)), c)      # 将每列加和在一起
        # 不等式未知量的系数矩阵
        A_ub = self.nu_cai * -1
        # 不等式的右边
        B_ub = nu_Sheng * -1

        res=op.linprog(c, A_ub, B_ub)   #, bounds=(x1,x2,x3))
        print(res)

        max_no_li = []
        max_no = 0
        res_x = []
        for i in res.x:
            res_x.append(i)
        
        for i in range(cai_num):
            # 查 第 i 大的
            j = 0
            for i in res_x:
                if i > res_x[max_no]:
                    max_no = j
                j += 1
            max_no_li.append(max_no)
            res_x[max_no] = 0
        
        # 更新 nu_cai 矩阵，仅使用三个菜进行计算
        # nu_cai_new = []
        nu_cai_shape_y = self.nu_cai.shape[1]
        for i in range(cai_num):
            self.nu_cai = np.append(self.nu_cai, self.nu_cai[:, max_no_li[i]].reshape((4,1)), axis = 1)

        self.nu_cai = self.nu_cai[:, nu_cai_shape_y:]
        

        # 更新 dish_name 矩阵
        dish_name_len = len(self.dish_name)
        for i in range(cai_num):
            self.dish_name.append(self.dish_name[max_no_li[i]])
        
        self.dish_name = self.dish_name[dish_name_len:]
        
        # 重新计算 n个菜分别吃多少
        # 最大值的函数的系数数组
        c = self.nu_cai / nu_Sheng
        c = np.dot(np.ones((1, 4)), c)      # 将每列加和在一起
        # 不等式未知量的系数矩阵
        A_ub = self.nu_cai * -1
        # 不等式的右边
        B_ub = nu_Sheng * -1

        res=op.linprog(c, A_ub, B_ub)   #, bounds=(x1,x2,x3))
        print(res)
        
        res_x = []
        for i in res.x:
            res_x.append(i * 300.00)       # 化为 300g  # 200
        
        low_li = []
        new_res_x = []
        new_dish_name = []
        new_nu_cai = np.array([])
        new_nu_cai = new_nu_cai.reshape((4, 0))
        i = 0
        j = 0
        for chi in res_x:
            if chi >= 50:
                j += 1
                new_dish_name.append(self.dish_name[i])
                new_res_x.append(chi)
                
                new_nu_cai = np.append(new_nu_cai, (self.nu_cai[:,i]).reshape((4, 1)), axis = 1)
            i += 1
        
        for i in range(len(new_dish_name)):
            print(new_dish_name[i] + '\t' + str(new_res_x[i]) + '\tg')
        
        nu_YouChi = self.getNuFromCai(new_nu_cai, new_res_x)

        nu_ChaJu = nu_Sheng - nu_YouChi     # 晚饭应吃 - 晚饭实际吃

        nu_Zong = nu_YouChi + nu_YiChi.reshape((4, 1))
        
        return new_dish_name, new_res_x, nu_YouChi, nu_ChaJu, nu_Zong
        

if __name__ == "__main__":
    # 仅用于测试
    csm = ChiShenMe()
    csm.addYiChigetNu(['红烧排骨米线'], [100])
    csm.getChiShenMe(5)