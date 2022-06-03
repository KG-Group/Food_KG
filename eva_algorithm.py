import csv

import xlrd
from py2neo import Graph, Node, Relationship


def gen_std_food(cat_name_list, title):
    data = xlrd.open_workbook("./document/group.xls")\
    # std_food = {'谷物类':[[]]}
    std_food = {}
    for food_cat in cat_name_list:
        temp_sheet = data.sheet_by_name(food_cat)
        n_row = temp_sheet.nrows
        n_col = temp_sheet.ncols
        temp_food = {}
        for i in range(0, len(title)):
            temp_col = temp_sheet.col_values(i+1, start_rowx=1, end_rowx=n_row)
            temp_value = temp_col.index(max(temp_col)) * 0.05 + 0.025
            temp_food[title[i]] = temp_value
        std_food[temp_sheet.name] = temp_food
    # for key in std_food.keys():
        # print(key)
        # print(std_food[key])
    return std_food


def gen_score(std_food, title):
    data = xlrd.open_workbook("./document/Normalized_2.xls")
    names = data.sheet_names()
    food_result = {}
    for name in names:
        temp_sheet = data.sheet_by_name(name)
        n_row = temp_sheet.nrows
        n_col = temp_sheet.ncols
        food_result[name] = {}
        for i in range(1, n_row):
            # 食物名，营养1，营养2……
            temp_row = temp_sheet.row_values(i, start_colx=3, end_colx=n_col)
            # for j in range(len(temp_row)):
            #     if temp_row[j] == '':
            #         temp_row[j] = 0
            temp_std_food = std_food[name]
            temp_result = {}
            for j in range(1, len(temp_row)):
                temp_result[title[j-1]] = temp_row[j] - temp_std_food[title[j-1]]
            food_result[name][temp_row[0]] = temp_result
    # print("food_result[谷物类][大麦仁]")
    # print(food_result["谷物类"]["大麦仁"])
    return food_result

    header = food_result[0].keys()

    with open("./document/relative_norm.csv", "w", encoding="utf-8-sig", newline="") as f:
        # writer = csv.writer(f)
        # writer.writerow(["\xef\xbb\xbf"])
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        writer.writerows(food_result)


def read_from_preference_sheet():
    data = xlrd.open_workbook("./document/健康目标-营养成分（多吃or少吃）20220530.xls")
    sheet = data.sheets()[0]
    # print(sheet.ncols)
    temp_row = sheet.row_values(1, start_colx=2, end_colx=sheet.ncols)
    # print(temp_row)
    temp_col = sheet.col_values(1, start_rowx=2, end_rowx=sheet.nrows)
    disease = {}
    for i in range(len(temp_col)):
        # print(i)
        # temp_col = 病名
        temp_list = sheet.row_values(i+2, start_colx=2, end_colx=sheet.ncols)
        disease[temp_col[i]] = {}
        for j in range(len(temp_row)):
            # j = 营养
            disease[temp_col[i]][temp_row[j]] = temp_list[j]
    return disease


def eva_food(disease, food):
    food_eva = {}
    for key in food.keys():
        food_eva[key] = {}
        for name in food[key].keys():
            food_eva[key][name] = 0
    for nutrition in disease.keys():
        if disease[nutrition] == '-':
            for food_type in food.keys():
                temp_type = food[food_type]
                for food_name in temp_type.keys():
                    food_eva[food_type][food_name] += food[food_type][food_name][nutrition] * -1
        elif disease[nutrition] == '+':
            for food_type in food.keys():
                temp_type = food[food_type]
                for food_name in temp_type.keys():
                    food_eva[food_type][food_name] += food[food_type][food_name][nutrition] * 1
    selected = {}
    for type_name in food_eva.keys():
        select_food = max(food_eva[type_name], key=food_eva[type_name].get)
        selected[type_name] = select_food
    return selected


def get_food():
# if __name__ == "__main__":
    cat_list = xlrd.open_workbook("./document/group.xls").sheet_names()
    temp_sheet = xlrd.open_workbook("./document/group.xls").sheets()[0]
    title = temp_sheet.row_values(0, start_colx=1, end_colx=temp_sheet.ncols)
    std_food = gen_std_food(cat_list, title)
    food_score = gen_score(std_food, title)
    disease_pref = read_from_preference_sheet()
    disease_food = {}
    for disease in disease_pref.keys():
        disease_food[disease] = eva_food(disease_pref[disease], food_score)
        # print(disease)
        # selected = eva_food(disease_pref[disease], food_score)
        # print(selected)
        # print()
    # print(disease_food)
    return disease_food

