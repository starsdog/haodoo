#coding=utf-8
from lxml import etree
from lxml import html
import requests
import os
import json
import argparse
import time
import codecs   

class htmlParser(object):
    def __init__(self):
        self.header={"Connection":"close"}
        self.project_dir = os.path.dirname(os.path.abspath(__file__))
        self.base_link='http://www.haodoo.net/'

    def check_folder(self, folder_path):
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

    def parse_book_link(self, file_path, title):
        parser=etree.HTMLParser()
        try:
            tree=html.parse(file_path)
        except:
            return False, ''

        link_info=tree.xpath("//input[@type='button']")
        book_link={"updb":[], "prc":[], "mobi":[], "epub":[], "vepub":[]}
        for info in link_info:
            innertext=etree.tostring(info, encoding='unicode', method='html')
            
            #find updb download link
            start_idx=innertext.find('DownloadUpdb')
            if start_idx!=-1:
                target=innertext[start_idx+14:]
                end_idx=target.find('\'')
                target=target[:end_idx]
                updb_link=self.base_link+'?M=d&P='+target+'.updb'
                book_link['updb'].append(updb_link)

            #find prc link
            start_idx=innertext.find('DownloadPrc')
            if start_idx!=-1:
                target=innertext[start_idx+13:]
                end_idx=target.find('\'')
                target=target[:end_idx]
                prc_link=self.base_link+'?M=d&P='+target+'.prc'
                book_link['prc'].append(prc_link)

            #find mobi link
            start_idx=innertext.find('DownloadMobi')
            if start_idx!=-1:
                target=innertext[start_idx+14:]
                end_idx=target.find('\'')
                target=target[:end_idx]
                mobi_link=self.base_link+'?M=d&P='+target+'.mobi'
                book_link['mobi'].append(mobi_link)     
            
            #find epub link
            start_idx=innertext.find('DownloadEpub')
            if start_idx!=-1:
                target=innertext[start_idx+14:]
                end_idx=target.find('\'')
                target=target[:end_idx]
                epub_link=self.base_link+'?M=d&P='+target+'.epub'
                book_link['epub'].append(epub_link)     

            #find vepub link
            start_idx=innertext.find('DownloadVEpub')
            if start_idx!=-1:
                target=innertext[start_idx+15:]
                end_idx=target.find('\'')
                target=target[:end_idx]
                vepub_link=self.base_link+'?M=d&P='+target+'.epub'
                book_link['vepub'].append(vepub_link) 

        head, tail=os.path.split(file_path)
        output_filename='{}.json'.format(tail[:-5])
        output_folder=os.path.join(self.project_dir, 'book_link', title)
        self.check_folder(output_folder)
        output_path=os.path.join(output_folder, output_filename)
        output_handler=codecs.open(output_path, 'w', encoding='utf-8')
        output_handler.write(json.dumps(book_link, ensure_ascii=False))
        output_handler.close()
            
    def parse_book_link_folder(self, folder):
        for dirPath, dirNames, fileNames in os.walk(folder_path):        
            for f in fileNames:  
                if '.html' in f:
                    file_path="{}".format(os.path.join(dirPath, f))  
                    title=os.path.basename(dirPath)
                    self.parse_book_link(file_path, title) 

    def parse_index_link(self, file_path, parent_foldername):
        parser=etree.HTMLParser()
        try:
            tree=html.parse(file_path)
        except:
            return False, ''

        index_link=[]
        link_info=tree.xpath("//div[@class='a03']")    
        for child in link_info:  
            for info in child.iter('a'):
                if(info.text!=None):
                    title=info.text
                    link='http://www.haodoo.net/'+info.attrib.get('href')
                    index_link.append({"title":title, "link":link})

        head, tail=os.path.split(file_path)
        output_filename='{}.json'.format(tail[:-5])
        output_folder=os.path.join(self.project_dir, 'index_link', parent_foldername)
        self.check_folder(output_folder)
        output_path=os.path.join(output_folder, output_filename)
        output_handler=codecs.open(output_path, 'w', encoding='utf-8')
        output_handler.write(json.dumps(index_link, ensure_ascii=False))
        output_handler.close()
                    
    def parse_index_link_folder(self, folder):
        for dirPath, dirNames, fileNames in os.walk(folder_path):        
            for f in fileNames:  
                if '.html' in f:
                    file_path="{}".format(os.path.join(dirPath, f)) 
                    title=os.path.basename(dirPath) 
                    self.parse_index_link(file_path, title) 
    
    def download_book_html_fodler(self, file_path):
        for dirPath, dirNames, fileNames in os.walk(folder_path):        
            for f in fileNames:  
                if '.json' in f:
                    file_path="{}".format(os.path.join(dirPath, f))  
                    input_handler=codecs.open(file_path,'r', encoding='utf-8')
                    content=json.load(input_handler)
                    for info in content:
                        title=info['title']
                        link=info['link']
                        self.download_html(title, link, "book_html")
                        time.sleep(60)

    def download_index_html(self, target_links):
        for info in target_links:
            title=info['title']
            link=info['link']
            self.download_html(title, link, "index_html")
            time.sleep(60)

    def download_book_folder(self, folder):
        for dirPath, dirNames, fileNames in os.walk(folder_path):        
            for f in fileNames:  
                if '.json' in f:
                    file_path="{}".format(os.path.join(dirPath, f))  
                    input_handler=codecs.open(file_path,'r', encoding='utf-8')
                    content=json.load(input_handler)
                    book_title=os.path.basename(dirPath)
                    output_folder=os.path.join(self.project_dir, 'ebook', book_title)
                    self.check_folder(output_folder)
                    for key in content.keys():
                        ebook_format=key
                        links=content[key]
                        for link in links:
                            r=requests.get(link, headers=self.header)
                            if r.status_code==200:
                                link_part=link.split('/')
                                filename="{}.{}".format(link_part[-1][1:], key)
                                output_file=os.path.join(output_folder, filename)
                                output=open(output_file, "wb")
                                output.write(r.content)
                            time.sleep(60)


    def download_html(self, title, link, target_folder):
        output_folder=os.path.join(self.project_dir, target_folder, title)
        self.check_folder(output_folder)
        link_part=link.split('/')
        filename="{}.html".format(link_part[-1][1:])
        output_file=os.path.join(output_folder, filename)
        if not os.path.exists(output_file):
            r=requests.get(link, headers=self.header)
            if r.status_code==200:
                output=open(output_file, "wb")
                output.write(r.content)
                output.close()

if __name__=="__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-t', '--task', metavar='parse', type=str, nargs=1, required=True,
        help='Specify a task to do. (parse)')
     
    args = arg_parser.parse_args()

    if args.task!=None:
        task=args.task[0]

    project_dir = os.path.dirname(os.path.abspath(__file__))
    config_file = project_dir + '/project_config/config.json'
    with codecs.open(config_file , "r", encoding='utf-8') as file:
        project_config=json.load(file)

    parser=htmlParser()    
    '''
    step:
    1. download index html
    2. parse index html and save to index_link
    3. download book html in index_link
    4. parse book html and save to book_link
    5. download book_link
    '''
    if task=='generate_book_page_links':
        parser.download_index_html(project_config['target_link'])
        folder_path=os.path.join(project_dir, 'index_html')
        parser.parse_index_link_folder(folder_path)
    elif task=='generate_book_download_links':
        folder_path=os.path.join(project_dir, 'index_link')
        parser.download_book_html_fodler(folder_path)
        folder_path=os.path.join(project_dir, 'book_html')
        parser.parse_book_link_folder(folder_path)
    elif task=='download_book':
        folder_path=os.path.join(project_dir, 'book_link')
        parser.download_book_folder(folder_path)
            
    

  


    

