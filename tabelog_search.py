#! pythin3
# tabelog_search.py
# 2018/11/24
# 開発担当者：川本孝太朗

import bs4
import requests
import webbrowser
import pyperclip

# 1ページ分のデータをリストにする関数
def get_list(url,val_list, rst_list):   #, list_url):
    res = requests.get(url)
    tabelog_soup = bs4.BeautifulSoup(res.text)
    rst = tabelog_soup.select('a.list-rst__rst-name-target.cpy-rst-name')
    rst_val = tabelog_soup.select('div.list-rst__rst-data')
    for i in range(len(rst)):
        rst_list.append(rst[i])
        rating = rst_val[i].select('span.c-rating__val--strong.list-rst__rating-val')
        if rating == []:
            val_list.append(0)  #評価ないところの例外処理
        else:
            try:
                num = rating[0].get_text()
                val_list.append(num)
            except IndexError:
                print('例外処理１')

# 全ページ分リストにする
def tabelog_search(url,val_list, rst_list):
    get_list(url,val_list, rst_list)

    while True:
        res = requests.get(url)
        tabelog_soup = bs4.BeautifulSoup(res.text)
        next_page = tabelog_soup.select('a.c-pagination__arrow.c-pagination__arrow--next')
        print('seaching')
        if next_page != []:
            next_url = next_page[0].attrs['href']
            get_list(next_url,val_list, rst_list)
            url = next_url
        else:
            break

# 評価に合わせてソートする
def bubble_sort(val_list, list1):
    for i in range(len(val_list)):
        for j in range(len(val_list) - i):
            try:
                str1 = val_list[j]
                str2 = val_list[j+1]
                if float(str1) < float(str2):
                    temp_val = val_list[j+1]
                    temp1 = list1[j+1]

                    val_list[j + 1] = val_list[j]
                    list1[j+1] = list1[j]

                    val_list[j] = temp_val
                    list1[j] = temp1
            except IndexError:
                print('例外処理2')

if __name__ == '__main__':
    url = pyperclip.paste()
    rst_list = list()
    rst_val_list = list()
    tabelog_search(url, rst_val_list, rst_list)
    bubble_sort(rst_val_list, rst_list)

    # 全ソート済みデータを表示
    for i in range(len(rst_val_list)):
        print(i+1,'位')
        print( rst_list[i].get_text() ,'評価：', rst_val_list[i] ,'url:', rst_list[i].attrs['href'] )

    # 上位10リンクを開く
    for i in range(10):
        webbrowser.open(rst_list[i].attrs['href'])


# ToDo 条件に応じたURL作成（.format使う）
# ToDo pyperclipから適切な範囲のURLをカット (.findでrstLstを探す)

