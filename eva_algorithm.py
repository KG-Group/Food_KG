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
    for key in std_food.keys():
        print(key)
        print(std_food[key])
    return std_food


def gen_score(std_food, title):
    data = xlrd.open_workbook("./document/Normalized.xls")
    temp_sheet = data.sheets()[0]
    n_row = temp_sheet.nrows
    n_col = temp_sheet.ncols
    food_result = []
    for i in range(1, n_row):
        # 种类，食物名，营养1，营养2……
        temp_row = temp_sheet.row_values(i, start_colx=2, end_colx=n_col)
        for j in range(len(temp_row)):
            if temp_row[j] == '':
                temp_row[j] = 0
        temp_std_food = std_food[temp_row[0]]
        temp_result = {"食品分类": temp_row[0], "样品名称": temp_row[1]}
        for j in range(2, len(temp_row)):
            temp_result[title[j-2]] = temp_row[j] - temp_std_food[title[j-2]]
        food_result.append(temp_result)
    return food_result
    print(food_result[0])

    header = food_result[0].keys()

    with open("./document/relative_norm.csv", "w", encoding="utf-8-sig", newline="") as f:
        # writer = csv.writer(f)
        # writer.writerow(["\xef\xbb\xbf"])
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        writer.writerows(food_result)


def eva_food(food_result):
    data = xlrd.open_workbook("./document/health_goal.xls")
    sheet = data.sheets()[0]
    print(sheet.ncols)
    temp_row = sheet.row_values(0, start_colx=1, end_colx=sheet.ncols)
    print(temp_row)


if __name__ == "__main__":
    cat_list = xlrd.open_workbook("./document/group.xls").sheet_names()
    temp_sheet = xlrd.open_workbook("./document/group.xls").sheets()[0]
    title = temp_sheet.row_values(0, start_colx=1, end_colx=temp_sheet.ncols)
    std_food = gen_std_food(cat_list, title)
    food_score = gen_score(std_food, title)
    eva_food(food_score)


#
# dict_by_cat = {}
# for i in range(len(FoodList)):
#     if dict_by_cat.get(FoodList[i]['食品分类']) is None:
#         dict_by_cat[FoodList[i]['食品分类']] = []
#     dict_by_cat[FoodList[i]['食品分类']].append(FoodList[i])
#
# for key in dict_by_cat.keys():
#     temp_list = dict_by_cat[key]
#     for item in temp_list:
#         for
