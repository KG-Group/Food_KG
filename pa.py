import requests
from bs4 import BeautifulSoup
import xlwt
import time

max = 95888
start = 60000
corpus = ''
MenuList = []
def pa():
    global corpus
    global MenuList
    indexs = 0
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
    }

    for page in range(start,max):
        url = f'https://home.meishichina.com/recipe-{page}.html'
        max_retry = 0
        while max_retry<5:
            try:
                response = requests.get(url=url, headers=headers)
                break
            except:
                time.sleep(1)
                max_retry+=1
                print("error")
        response.encoding='utf-8'#统一改成utf-8
        soup =BeautifulSoup(response.text,'lxml')#将爬取的网页以字符串的形式传入
        foods = soup.select('.recipe_De_title')#选中class选择器(菜名)
        material = soup.find_all('div',attrs={'class': 'recipeCategory_sub_R'})#（材料）
        step = soup.find_all('div',attrs={'class': 'recipeStep_word'})#做法步骤
        for food in foods:
            urls = food.find('a')#查找标签
            name = urls.get_text()#获取标签内文本
            link = urls["href"]#获取链接
            food_material=[]
            str1=''
            str2=''
            #---------------------------获取原料文本
            for mat in material:
                cai = mat.find_all('li')
                for c in cai :
                    food_material.append(c.text.strip().replace('\n',''))
            for s in food_material:
                str1 =str1+s+','
            for ste in step:
                str2 =str2+ste.text+','
                
        indexs = indexs+1
        str2 = str2[1:-1]
        food_material = food_material[:-4]
        #print(name)
        #print(food_material)
        #print(str2)
        
        print("正在读取第"+str(indexs)+"张网页----"+url)

        corpus = corpus + str2
        MenuList.append([name,food_material])
if __name__ == '__main__':
    pa()
    print("数据读取完毕！！！")
    #print(corpus)
    #print(MenuList)
    i = 1
    while True:
        if(i < len(MenuList)-1 and MenuList[i][0] == MenuList[i+1][0]):
            MenuList = MenuList[0:i+1]+MenuList[i+2:]
        else:
            i = i+1
        if(i>=len(MenuList)):
            break;

    #xl = xlwt.Workbook(encoding = 'utf-8')
    xl2 = xlwt.Workbook(encoding = 'utf-8')
    #sheet = xl.add_sheet("sheet1")
    sheet2 = xl2.add_sheet("sheet1")
    rangel = len(MenuList)
    #if len(MenuList)<60000:rangel = len(MenuList)
    #else:rangel = 60000
    for i in range (0,rangel):
        sheet2.write(i,0,MenuList[i][0])
        for j in range(0,len(MenuList[i][1])):
            sheet2.write(i,j+1,MenuList[i][1][j])
    xl2.save('./document/RowMenu35000.xls')
    #f = open('./document/corpus.txt',mode = 'w',encoding = 'UTF-8')
    #f.write(corpus)
    #f.close()