from py2neo import Graph, Node, NodeMatcher, Relationship
import xlrd

graph = Graph('bolt://nas.boeing773er.site:7687')

data = xlrd.open_workbook("./document/kacl_nutri.xls")
temp_sheet = data.sheets()[0]
nutri_name = temp_sheet.col_values(0, start_rowx=1, end_rowx=temp_sheet.nrows)
print(nutri_name)

upload_nutri_node = False
if upload_nutri_node:
    for nutri in nutri_name:
        GNode = Node('Nutrition', name=nutri )
        graph.create(GNode)
        graph.push(GNode)

kcal_list = temp_sheet.row_values(0, start_colx=1, end_colx=temp_sheet.ncols)
print(kcal_list)

upload_kcal_node = False
if upload_kcal_node:
    for kcal in kcal_list:
        GNode = Node('kcal', name=kcal )
        graph.create(GNode)
        graph.push(GNode)

upload_nutri_kcal_edge = False
if upload_nutri_kcal_edge:
    for i in range(1, temp_sheet.ncols):
        temp_col = temp_sheet.col_values(i, start_rowx=1, end_rowx=temp_sheet.nrows)
        print(temp_col)
        kcal = kcal_list[i-1]
        matcher = NodeMatcher(graph)
        kcal_node = matcher.match('kcal', name=kcal).first()
        for j in range(len(nutri_name)):
            nutri_node = matcher.match('Nutrition', name=nutri_name[j]).first()
            Edge = Relationship(kcal_node, str(temp_col[j]), nutri_node)
            graph.create(Edge)
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

upload_age_kcal_edge = True
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

