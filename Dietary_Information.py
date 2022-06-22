from py2neo import Graph, Node, NodeMatcher, Relationship, RelationshipMatcher
import xlrd

# 连接至数据库
graph = Graph('bolt://nas.boeing773er.site:7687')
# 读取excel文件
data = xlrd.open_workbook("./document/kacl_nutri.xls")
temp_sheet = data.sheets()[0]
# 获取营养名
nutri_name = temp_sheet.col_values(0, start_rowx=1, end_rowx=temp_sheet.nrows)

upload_nutri_node = False
if upload_nutri_node:
# 根据营养名创建Nutrition节点
    for nutri in nutri_name:
        GNode = Node('Nutrition', name=nutri)
        graph.create(GNode)
        graph.push(GNode)
# 获取能量值
kcal_list = temp_sheet.row_values(0, start_colx=1, end_colx=temp_sheet.ncols)

upload_kcal_node = False
if upload_kcal_node:
# 根据能量值创建Kcal节点
    for kcal in kcal_list:
        GNode = Node('kcal', name=kcal )
        graph.create(GNode)
        graph.push(GNode)

upload_nutri_kcal_edge = True
if upload_nutri_kcal_edge:
# 创建requires边
    for i in range(1, temp_sheet.ncols):
        temp_col = temp_sheet.col_values(i, start_rowx=1, end_rowx=temp_sheet.nrows)
        kcal = kcal_list[i-1]
        matcher = NodeMatcher(graph)
        # 查询获取kcal节点
        kcal_node = matcher.match('kcal', name=kcal).first()
        for j in range(len(nutri_name)):
            # 查询获取Nutrition节点
            nutri_node = matcher.match('Nutrition', name=nutri_name[j]).first()
            Edge = Relationship(kcal_node, str(temp_col[j]), nutri_node)
            graph.create(Edge)
            # 提交边
            graph.push(Edge)

upload_age_node = False
if upload_age_node:
    for age in range(7, 70):
        GNode = Node('age', name=age)
        graph.create(GNode)
        graph.push(GNode)

upload_bmi_node = False
if upload_bmi_node:
    GNode = Node('bmi', name=19.0)
    graph.create(GNode)
    graph.push(GNode)
    GNode = Node('bmi', name=23.0)
    graph.create(GNode)
    graph.push(GNode)

upload_age_bmi_edge = False
if upload_age_bmi_edge:
    matcher = NodeMatcher(graph)
    age_list = matcher.match("age").where("_.name>17")
    for age_node in age_list:
        bmi_node = matcher.match("bmi").where(name=19.0).first()
        Edge = Relationship(age_node, "normal_min_bmi", bmi_node)
        graph.create(Edge)
        graph.push(Edge)
        bmi_node = matcher.match("bmi").where(name=23.0).first()
        Edge = Relationship(age_node, "normal_max_bmi", bmi_node)
        graph.create(Edge)
        graph.push(Edge)

upload_age_kcal_edge = False
if upload_age_kcal_edge:
    matcher = NodeMatcher(graph)
    age_list = matcher.match("age").where("_.name<11")
    for age_node in age_list:
        kcal_node = matcher.match("kcal").where(name='1400kcal').first()
        Edge = Relationship(age_node, "min_kcal", kcal_node)
        graph.create(Edge)
        graph.push(Edge)
        kcal_node = matcher.match("kcal").where(name='1800kcal').first()
        Edge = Relationship(age_node, "max_kcal", kcal_node)
        graph.create(Edge)
        graph.push(Edge)
    age_list = matcher.match("age").where("_.name>10 and _.name<14")
    for age_node in age_list:
        kcal_node = matcher.match("kcal").where(name='1800kcal').first()
        Edge = Relationship(age_node, "min_kcal", kcal_node)
        graph.create(Edge)
        graph.push(Edge)
        kcal_node = matcher.match("kcal").where(name='2000kcal').first()
        Edge = Relationship(age_node, "max_kcal", kcal_node)
        graph.create(Edge)
        graph.push(Edge)
    age_list = matcher.match("age").where("_.name>13 and _.name<18")
    for age_node in age_list:
        kcal_node = matcher.match("kcal").where(name='2000kcal').first()
        Edge = Relationship(age_node, "min_kcal", kcal_node)
        graph.create(Edge)
        graph.push(Edge)
        kcal_node = matcher.match("kcal").where(name='2600kcal').first()
        Edge = Relationship(age_node, "max_kcal", kcal_node)
        graph.create(Edge)
        graph.push(Edge)
    age_list = matcher.match("age").where("_.name>17 and _.name<65")
    for age_node in age_list:
        kcal_node = matcher.match("kcal").where(name='1800kcal').first()
        Edge = Relationship(age_node, "min_kcal", kcal_node)
        graph.create(Edge)
        graph.push(Edge)
        kcal_node = matcher.match("kcal").where(name='2200kcal').first()
        Edge = Relationship(age_node, "max_kcal", kcal_node)
        graph.create(Edge)
        graph.push(Edge)
    age_list = matcher.match("age").where("_.name>65")
    for age_node in age_list:
        kcal_node = matcher.match("kcal").where(name='1400kcal').first()
        Edge = Relationship(age_node, "min_kcal", kcal_node)
        graph.create(Edge)
        graph.push(Edge)
        kcal_node = matcher.match("kcal").where(name='2000kcal').first()
        Edge = Relationship(age_node, "max_kcal", kcal_node)
        graph.create(Edge)
        graph.push(Edge)


upload = False
if upload:
    bmi_min_list = [14.0, 14.1, 14.2, 14.5, 15.0, 15.5, 16.0, 16.5, 17.0, 17.4, 17.8]
    bmi_max_list = [17.3, 18.0, 18.8, 19.5, 20.2, 20.9, 21.8, 22.5, 23.0, 23.4, 23.7]
    matcher = NodeMatcher(graph)
    for i in range(len(bmi_max_list)):
        age_node = matcher.match("age").where(name=i+7).first()
        GNode = Node('bmi', name=bmi_min_list[i])
        graph.create(GNode)
        graph.push(GNode)
        Edge = Relationship(age_node, "normal_min_bmi", GNode)
        # Edge.
        graph.create(Edge)
        graph.push(Edge)
        GNode = Node('bmi', name=bmi_max_list[i])
        graph.create(GNode)
        graph.push(GNode)
        Edge = Relationship(age_node, "normal_max_bmi", GNode)
        graph.create(Edge)
        graph.push(Edge)

# node_matcher = NodeMatcher(graph)
# node1 = node_matcher.match("age").where(name=18).first()
# print(node1)
# matcher = RelationshipMatcher(graph)
# result = matcher.match([node1], r_type=None)
# for temp in result:
#     print(temp)
#     print(temp.labels())
