import xlrd
from py2neo import Graph, Node, Relationship


def gen_std_food(cat_name_list):
    data = xlrd.open_workbook("./document/group.xls")
    std_food = {}
    for food_cat in cat_name_list:
        temp_sheet = data.sheet_by_name(food_cat)
        n_row = temp_sheet.nrows
        n_col = temp_sheet.ncols
        title = temp_sheet.row_values(0, start_colx=1, end_colx=n_col)
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


def gen_score(std_food):
    data = xlrd.open_workbook("./document/Normalized.xls")
    temp_sheet = data.sheets()[0]
    n_row = temp_sheet.nrows
    n_col = temp_sheet.ncols
    for i in range(1, n_row):
        temp_row = temp_sheet.row_values(i, start_colx=2, end_colx=n_col)
        nowDic = {}
        for j in range(2, colNum-1):
            if nowRow[j] != '':
    #             nowDic[title[j]] = nowRow[j]
    #         else:
    #             nowDic[title[j]] = 0
    #     FoodList.append(nowDic)
    # print(FoodList[1])


if __name__ == "__main__":
    cat_list = xlrd.open_workbook("./document/group.xls").sheet_names()
    std_food = gen_std_food(cat_name_list=cat_list)


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
