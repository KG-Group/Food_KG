from scipy import optimize as op
import numpy as np
import sys
from py2neo import Node, Relationship, Graph, NodeMatcher, RelationshipMatcher
# import Wang_Gui


class ChiShenMe:
    # cai_weight_li 中单位为 克
    def __init__(self, age, bmi, cai_name_li, cai_weight_li):
        self.age = age
        self.bmi = bmi
        self.cai_name_li = cai_name_li
        self.cai_weight_li = cai_weight_li
        self.graph = Graph('bolt://nas.boeing773er.site:7687')

    # 已经吃了什么菜
    # -> 每种营养成分已经吃了多少

    # 根据身高、体重、BMI查询，这个人应该摄入多少营养成分
    # -> 相减得到：每种营养成分剩余摄入量
    age = 20
    h = 160
    w = 70
    bmi = 20

    # [能量，蛋白质，脂肪，胆固醇，CHO]
    def getNu(self, age, bmi):
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
        # print(max_kcal_relation.end_node['name'])

        min_kcal_relation = relation_matcher.match(
            [age_node],
            r_type='min_kcal'
        ).first()
        min_kcal = int(min_kcal_relation.end_node['name'][:-4])
        # print(min_kcal_relation)

        max_bmi_relation = relation_matcher.match(
            [age_node],
            r_type='normal_max_bmi'
        ).first()
        max_bmi = float(max_bmi_relation.end_node['name'])
        # print(max_bmi_relation)

        min_bmi_relation = relation_matcher.match(
            [age_node],
            r_type='normal_min_bmi'
        ).first()
        min_bmi = float(min_bmi_relation.end_node['name'])
        # print(min_bmi_relation)

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
            if i.end_node['name'] == 'CHO（g）':
                cho = float(type(i).__name__)
            elif  i.end_node['name'] == '胆固醇（mg）':
                dgc = float(type(i).__name__) / 1000
            elif  i.end_node['name'] == '脂肪（g）':
                zf = float(type(i).__name__)
            elif  i.end_node['name'] == '蛋白质（g）':
                dbz = float(type(i).__name__)
        
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
        relation_matcher = RelationshipMatcher(self.graph)
        dish_nodes = node_matcher.match("Dish")
        
        dish_name = []
        nu_cai = np.zeros((4,0))
        for i in list(dish_nodes):
            dish_dict = dict(i)
            dish_name.append(dish_dict['name'])

            dbz = float(dish_dict['粗蛋白(g)'])

            zf = float(dish_dict['脂肪酸P总量(mg)']/1000)
            zf += float(dish_dict['脂肪酸S总量(mg)']/1000)
            zf += float(dish_dict['脂肪酸M总量(mg)']/1000)
            zf += float(dish_dict['反式脂肪(mg)']/1000)
            zf += float(dish_dict['粗脂肪(g)'])
            zf += float(dish_dict['饱和脂肪(g)'])
            zf += float(dish_dict['其他脂肪酸(mg)']/1000)

            dgc = float(dish_dict['胆固醇(mg)']/1000)

            cho = float(dish_dict['总碳水化合物(g)'])
            
            this_cai = np.array([[dbz], [zf], [dgc], [cho]])
            nu_cai = np.append(nu_cai, this_cai, axis = 1)
        
        nu_cai = nu_cai[:, 1:]      #  去除第一列0值
        # print(nu_cai.shape)

        return dish_name, nu_cai

    def getNu_YiChi(self, cai_li, nu_cai, dish_name, cai_weight):
        nu_YiChi = np.array([0, 0, 0, 0])
        i = 0
        for cai in cai_li:
            if cai in dish_name:
                nu_YiChi = nu_YiChi + nu_cai[:, dish_name.index(cai)] * cai_weight[i] / 300.0
            i += 1
        return nu_YiChi

    # 外部调用的函数
    def getChiShenMe(self, cai_num, else_nu_Yichi):
        dish_name, nu_cai = self.getCai()

        # 已吃-营养成分向量（4）
        nu_YiChi = self.getNu_YiChi(self.cai_name_li, nu_cai, dish_name, self.cai_weight_li)   # 已经吃了的营养成分量 (能量)[蛋白质，脂肪，胆固醇，CHO]
        nu_YiChi = nu_YiChi + np.array(else_nu_Yichi) / 300
        # 应吃-营养成分向量（5）
        nu_YingChi = self.getNu(self.age, self.bmi)  # age, bmi

        # 设能量
        # nl = nu_YingChi[0]
        nu_YingChi = nu_YingChi[1:]     # 去除 能量

        # 求 剩余-营养成分向量（4）
        nu_Sheng = nu_YingChi - nu_YiChi    # 剩余 应该吃的营养成分量 [能量，蛋白质，脂肪，胆固醇，CHO]
        nu_Sheng = nu_Sheng.reshape((4, 1))



        # 最大值的函数的系数数组
        c = nu_cai / nu_Sheng
        c = np.dot(np.ones((1, 4)), c)      # 将每列加和在一起
        # 不等式未知量的系数矩阵
        A_ub = nu_cai * -1
        # 不等式的右边
        B_ub = nu_Sheng * -1
        print("c")
        print(c.shape)
        print("A_ub")
        print(A_ub.shape)
        res=op.linprog(c, A_ub, B_ub)   #, bounds=(x1,x2,x3))
        print(res)
        print("---------")
        print(res.x) # .reshape(1,nu_cai.shape[1])


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

        for i in max_no_li:
            print(dish_name[i])
        

        # 更新 nu_cai 矩阵，仅使用三个菜进行计算
        # nu_cai_new = []
        nu_cai_shape_y = nu_cai.shape[1]
        for i in range(cai_num):
            nu_cai = np.append(nu_cai, nu_cai[:, max_no_li[i]].reshape((4,1)), axis = 1)
            # nu_cai_new.append(nu_cai[:, max_no_li[i]])
        '''nu_cai0 = nu_cai[:, max_no_li[0]]
        nu_cai1 = nu_cai[:, max_no_li[1]]
        nu_cai2 = nu_cai[:, max_no_li[2]]'''
        print(nu_cai.shape)
        nu_cai = nu_cai[:, nu_cai_shape_y:]
        print(nu_cai.shape)
        

        '''print("??????????????????????????")
        print(nu_cai_new[0])#.shape)
        print(np.array(nu_cai_new).reshape((4, cai_num), order = 'F').shape)
        print(np.array(nu_cai_new).reshape((4, cai_num), order = 'F'))'''

        '''nu_cai = np.append(nu_cai0.reshape((4, 1)), nu_cai1.reshape((4, 1)), axis = 1)  # .reshape((4, 2))
        nu_cai = np.append(nu_cai, nu_cai2.reshape((4, 1)), axis = 1)'''

        # print(nu_cai.shape)
        # print(nu_cai)

        # 更新 dish_name 矩阵
        dish_name_len = len(dish_name)
        for i in range(cai_num):
            dish_name.append(dish_name[max_no_li[i]])
            # nu_cai_new.append(nu_cai[:, max_no_li[i]])
        
        print("dish_name:")
        print(len(dish_name))
        dish_name = dish_name[dish_name_len:]
        print(len(dish_name))





        # 重新计算 三个菜分别吃多少
        # 最大值的函数的系数数组
        c = nu_cai / nu_Sheng
        c = np.dot(np.ones((1, 4)), c)      # 将每列加和在一起
        # 不等式未知量的系数矩阵
        A_ub = nu_cai * -1
        # 不等式的右边
        B_ub = nu_Sheng * -1
        print("c")
        print(c.shape)
        print("A_ub")
        print(A_ub.shape)
        res=op.linprog(c, A_ub, B_ub)   #, bounds=(x1,x2,x3))
        print(res)
        print("---------")
        print(res.x) # .reshape(1,nu_cai.shape[1])

        res_x = []
        for i in res.x:
            res_x.append(i * 300)       # 化为 100g
        
        i = 0
        for i in range(cai_num):
            print(dish_name[i] + '\t' + str(res_x[i]) + '\tg')
        
        return dish_name, res_x
        


if __name__ == "__main__":
    csm = ChiShenMe(22, 25, ['红烧排骨米线'], [300])
    dish_name, res_x = csm.getChiShenMe(5, [0, 0, 0, 0])   # 传入其余 已吃营养成分 [蛋白质，脂肪，胆固醇，CHO]
    





        
    



# 获取 每种菜肴的营养成含量



# 根据 每种营养成分剩余摄入量、每种菜肴的营养成含量
# 计算应该吃什么菜吃多少
'''['宫保鸡丁', '焯奥里给']    # 返回 菜 （list）
年龄    # 返回 年龄（int）
bmi     # 返回 bmi（float）'''


# nu_YingChi = np.array([100, 100, 100, 100, 100])    # 应吃的营养成分量 (能量)[蛋白质，脂肪，胆固醇，CHO]




# print(nu_YingChi)

# 菜-营养成分矩阵，形状=(4, cai_num)，每列是同一个菜
'''cai_num = 2
cai = np.zeros((4, cai_num))    # 值位于0-1之间
cai = np.array([[0.8, 0],
                [0.8, 0.2],
                [0.01, 0.39],
                [0.1, 0.1]])
cai = nu_cai'''
'''cai = [[1000, 1000],
        [1000, 1000],
        [1000, 1000],
        [1000, 1000],
        [1000, 1000]]'''



# print(np.dot(res.x.reshape(1,2) * cai, np.ones((2,1))))

'''max_no = 0
j = 0
for i in res.x:
    if i > res.x[max_no]:
        max_no = j
    j += 1

print(max_no)
print(dish_name[max_no])'''
'''c=np.array([2,3,-5])        # 最大值的函数的系数数组
A_ub=np.array([[-2,5,-1],[1,3,1]])  #注意是-2，5，-1
B_ub=np.array([-10,12])
A_eq=np.array([[1,1,1]])
B_eq=np.array([7])
# 上限7是根据约束条件1和4得出的
x1=(0,7)
x2=(0,7)
x3=(0,7)
res=op.linprog(-c,A_ub,B_ub,A_eq,B_eq,bounds=(x1,x2,x3))
print(res)'''


# 仅测试 getNu_YiChi 功能用{

'''cai_li = ['香菇菜心']# , '酸菜鱼']

nu_YiChi = getNu_YiChi(cai_li, nu_cai, dish_name)
print(nu_YiChi)     # [蛋白质，脂肪，胆固醇，CHO]

# 宫保鸡丁 100
# 宫保鸭丁 50

['宫保鸡丁', '宫保鸭丁']
[100, 50]'''

# 仅测试 getNu_YiChi 功能用}

