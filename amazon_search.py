#! python3
# amazon_search.py
# 2018/11/29
# 開発担当者：川本孝太朗
# 水口さんの基礎研




import requests     # webデータダウンロード用
import bs4          # HTML解析用のライブラリ
#import pyperclip    # コピー＆ペーストをするためのライブラリ
import csv          # csv形式でファイルへの出力

# 1ページ分のデータをリストにする関数
def get_reviews(url,rvw_list):
    res = requests.get(url)                 # URLのページをダウンロード
    amazon_soup = bs4.BeautifulSoup(res.text, features='lxml')  # HTMLを解析
    rvw = amazon_soup.select('div.a-row.a-spacing-small.review-data')   # レビューをリストにして取り出す
    for i in range(len(rvw)):
        rvw_list.append(rvw[i])     # リストにレビューを追加


# 全ページ分リストにする
def amazon_search(url,rvw_list):
    get_reviews(url, rvw_list)  # 一ページ目
    i = 1

    while True:
        res = requests.get(url)
        amazon_soup = bs4.BeautifulSoup(res.text, features='lxml')
        next_page = amazon_soup.select('li.a-last a')   # 次へボタン

        print(i,'seaching')
        i += 1
        if next_page != []:     # 次へボタンがあれば
            next_url = 'https://www.amazon.co.jp/' + next_page[0].attrs['href']    # 次へボタンの中にあるURLを参照
            get_reviews(next_url, rvw_list)     # 次のページのURLを取得
            url = next_url         # URLを更新
        else:
            break


if __name__ == '__main__':
    print('Amazonのレビューを検索します\n検索ワードを入力してください\n検索ワード：', end='')
    key_word = input()      # 検索キーワードの入力
    #url = pyperclip.paste()     # ペーストする。URLをコピーしておかないとエラー出る
    url='https://www.amazon.co.jp/'
    url += input('URLを貼り付けてください')

    # csv用
    res = requests.get(url)
    title_soup = bs4.BeautifulSoup(res.text, features='lxml')
    title = title_soup.select('#productTitle')
    output_file = open( 'レビュー.csv','w', newline='')
    output_writer = csv.writer(output_file)


    new_url = url.replace('dp', 'product-reviews')     # URLをレビューページのものに書き換える
    rvw_list = list()
    amazon_search(new_url, rvw_list)    # レビューの取得


    # 全データを表示
    for i in range(len(rvw_list)):
        output_writer.writerow(['review' + str(i+1), rvw_list[i].text])
        if key_word in rvw_list[i].text:    # 検索ワードが含まれていたら
            print('review', i+1, ' : ', rvw_list[i].text)

