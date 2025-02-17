# PaperSearchApp

ハッカソン

# report

## Kuranuki

6/8

- flask と html を使用し、簡単な arxiv の検索 web サイトを作成
  
6/9~6/13

- フロントの作成
　-次すること：ページの遷移を作り、バブルチャートを表示   

6/14

- routerの導入
6/15

- バイト
  6/16

- ソースコードが上手く反映されないため、パワポ作成
  - 残り：実行画面とセリフを考えるだけ 

## Wada

6/9

- 検索クエリの種類を選択できる機能の追加：著者名検索 →"Author"，タイトル検索 →"Title"
- semanticscholar の API を用いて引用数を表示，引用数順に検索結果を示す
  - 問題点：検索に時間がかかる，引用数が入手できない論文は"0"表示となり上位検索結果に現れない

6/10
- Dockerでfrontendとbackendのコンテナを作り，frontendにvueでのプロジェクトを作成するための方法を勉強
 - うまくいかず明日へ持ち越し 

6/11
- vueを用いたDockerを作成（中身は関係ないもの）

6/14
- 閲覧数のデータベースを作成し、フロントにも閲覧数を表示

6/15
- 並列処理を用いて検索の高速化
  - 検索件数30件でも3秒以下で表示

6/16
- 検索履歴をキャッシュとして5分間保存
  - 何分残すべきか検討（5分？1時間？1日？）

6/17
- $マークで囲まれた数式は正常に表示させれる
- APIのリクエストに3秒の間隔をあける 

# 目標

6 月 9 日まで
・arXiv での実装

# わからないこと

・トップカンファレンスからデータを取得するのが難しい
google custum search の使用の検討

Arxiv API を利用して論文を検索し、結果を表示する Web アプリを作成
フロントエンドは Vue.js を使用
バックエンドは FastAPI、flask を使用
Docker と Docker Compose を使用

