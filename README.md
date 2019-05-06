# haodoo
這是好讀網站的網路爬蟲, 可以把ebook連結找出來

# 建立環境
1. 安裝python package 管理軟體 
  ``` 
  sudo python3 get-pip.py
  ```
2. 安裝virtualenv
  ```
   pip3 install virtualenv
   virtualenv bin
  ```
3. 進入virtualenv
  ```
  source bin/bin/activate
  ```
4. 安裝所需軟體
  ```
  pip3 install -r requirements.txt
  ```
5. 離開virtualenv
  ```
  deactivate
  ```

# 使用方法

此tool會依據三個步驟下載ebook連結
* 步驟一: 下載目錄網頁, 並把目錄網頁裡書的網頁連結
  ```
  python3 parser.py -t generate_book_page_links
  ```
* 步驟二: 下載書的網頁與把書的網頁裡關於ebook的下載連結找出來
  ```
  python3 parser.py -t generate_book_download_links
  ```
* 步驟三: 依序下載"book_link"下的ebook連結
  ```
  python3 parser.py -t download_book
  ```

步驟詳細說明如下: 
1. 目前列出的目錄網頁包括
  * 世紀百強
  * 隨身智囊
  * 歷史煙雲
  * 武俠小說
  * 懸疑小說
  * 言情小說
  * 奇幻小說
  * 小說園地
 * 有聲書
  
  如您只想下載某些目錄, 您可以更改project_config/config.json(需符合JSON格式), 例如您只想下載"歷史煙雲"種類, 可改成
  ```
  {
    "target_link":[
        {"title":"歷史煙雲", "link":"http://www.haodoo.net/?M=hd&P=history"}
    ]
  }
  ``` 
  
  
2. 一共會建立五個目錄,

   目錄網頁會儲存在"index_html"目錄下
   
   書的網頁連結會儲存在"index_link"目錄下
   
   書的網頁會儲存在"book_html"目錄下
   
   ebook連結會儲存在"book_link"目錄下
   
   ebook儲存在"ebook"目錄下, 所有的格式(updb, prc, mobi, epub, vepub) 皆會下載 
  
3. 因為怕弄壞"好讀"網站, 每次下載都會間隔數分鐘, 請耐心等候. 
 
