# haodoo
這是好讀網站的網路爬蟲, 可以把ebook連結找出來

# 使用方法
1. 首先更改project_config/下的config.json
  * target_link: 列出目錄網頁
2. 下載目錄網頁與把目錄網頁裡關於書的網頁連結找出來
  * command: python3 parser.py -t generate_book_page_links
  * 目錄網頁存在"index_html"
  * 書的連結以json format存在"index_link"
3. 下載書的網頁與把書的網頁裡關於ebook的下載連結找出來
  * command: python3 parser.py -t generate_book_download_links
  * 書的網頁存在"book_html"
  * ebook連結以json format存在"book_link"
4. 依序下載"book_link"下的ebook連結
  * command: python3 parser.py -t download_book
  
 
  
