#! python3
# cosme_search.py
# 2018/11/29
# 開発担当者：川本孝太朗
# 水口さんの基礎研

import requests     # webデータダウンロード用
import bs4          # HTML解析用のライブラリ
import pyperclip    # コピー＆ペーストをするためのライブラリ
import csv          # csv形式でファイルへの出力
import textwrap     # 長い文字列を改行して表示


# 1ページ分のデータをリストにする関数
def get_reviews(url,rvw_list):
    res = requests.get(url)                 # URLのページをダウンロード
    cosme_soup = bs4.BeautifulSoup(res.text, features='lxml')  # HTMLを解析
    rvw = cosme_soup.select('div.body p.read')   # レビューをリストにして取り出す
    for i in range(len(rvw)):
        rvw_list.append(rvw[i])     # リストにレビューを追加


# 全ページ分リストにする
def cosme_search(url,rvw_list):
    get_reviews(url, rvw_list)  # 一ページ目
    i = 1

    while True:
        res = requests.get(url)
        cosme_soup = bs4.BeautifulSoup(res.text, features='lxml')
        next_page = cosme_soup.select('li.next a')   # 次へボタン

        print('{}seaching'.format(i))
        i += 1
        if next_page != []:     # 次へボタンがあれば
            next_url = next_page[0].attrs['href']    # 次へボタンの中にあるURLを参照
            get_reviews(next_url, rvw_list)     # 次のページのURLを取得
            url = next_url         # URLを更新
        else:
            break

# レビューの全文を整形して表示
def print_review(url):
    res = requests.get(url)
    soup = bs4.BeautifulSoup(res.text, features='lxml')
    review = soup.select('p.read')
    print(textwrap.fill(review[0].text,40),end='\n\n')


if __name__ == '__main__':
    print('商品のレビューを検索します\n検索ワードを入力してください\n検索ワード：', end='')
    key_word = input()      # 検索キーワードの入力
    url = pyperclip.paste()     # ペーストする。URLをコピーしておかないとエラー出る
    new_url = url.replace('top', 'reviews')     # URLをレビューページのものに書き換える
    rvw_list = list()
    cosme_search(new_url, rvw_list)    # レビューの取得


    # 全データを表示
    for i in range(len(rvw_list)):
        if key_word in rvw_list[i].text:    # 検索ワードが含まれていたら
            temp =  rvw_list[i].select('span.read-more a') #レビュー全文のページのURLを取得
            url = temp[0].attrs['href']
            print('review{}:'.format(i))
            print_review(url)       # レビューページの文章を表示

