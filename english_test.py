#! python3
#  english_test.py 英単語を登録してテストする

import webbrowser   #pip install webbrowser
import requests     #pip install requests
import bs4          #pip install beautifulsoup4

#これ以下は使ってないライブラリ
import random
import pickle
import pprint

# Weblioの目的の単語へアクセス
def search_word(word):
    webbrowser.open(r'https://ejje.weblio.jp/content/'+ word)

# Weblioから意味をとってくる
def get_e2j(word):
    #print('こっち来てる')
    res =  requests.get(r'https://ejje.weblio.jp/content/'+ word)
    res.raise_for_status()
    word_soup = bs4.BeautifulSoup(res.text, features="lxml")
    means = word_soup.select('td.content-explanation.ej')
    audio = word_soup.select('#audioDownloadPlayUrl')
    # 音声再生する
    try:
        # print(means[0].get_text())
        # webbrowser.open(audio[0].attrs['href'])
        return means[0].get_text()
    except IndexError:
        pass
        #print('音声ファイルがありません')
    return False


def get_j2e(word):
    res =  requests.get(r'https://ejje.weblio.jp/content/'+ word)
    #print(res.raise_for_status())
    word_soup = bs4.BeautifulSoup(res.text, features="lxml")
    means = word_soup.select('td.content-explanation.je')
    audio = word_soup.select('#audioDownloadPlayUrl')
    # 音声再生する
    #print(means[0].get_text())
    try:
        #print(means[0].get_text())
        return means[0].get_text()

    except IndexError:
        pass
        #print('音声ファイルがありません')
    return False



if __name__ == '__main__':
    while True:
        print('単語を入力してください(push q to quit)')
        word = input()
        if word == 'q':
            break

        e2j = get_e2j(word)
        j2e = get_j2e(word)

        if e2j == False and j2e == False:
            print('単語が見つかりませんでした')
        elif e2j != False:
            print(e2j)
        else:
            print(j2e)


# ToDo 辞書を保存
# ToDo 英語から日本語
# ToDo 日本語から英語
# ToDo 4択version
# ToDo 自動で辞書から削除
# ToDo 使い方説明モード
# ToDo 習熟度を可視化
