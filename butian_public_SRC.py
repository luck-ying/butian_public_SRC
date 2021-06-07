import requests
import re
import json
Cookie=''
headers = {
           'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0',
           'content-type': 'application/x-www-form-urlencoded',
           'Cookie':Cookie
           }
src_name=[] #网站名字+URL临时缓存
src_url=[] #URL临时缓存
class bt():
    def title(self):
        print('''
+------------------------------------------------+
# 爬取所有公益厂商的ID
# 保存为src_url_list.txt 内容：URL
# 保存为src_name_list.txt 内容：厂商+URL
+------------------------------------------------+                                     
''')
    def crawl_id(self,page):
        target_url='https://www.butian.net/Reward/pub'
        data={
            's':'1',
            'p':page,
            'token':''
        }
        res=requests.post(url=target_url,headers=headers,data=data)
        #每一页厂商的数量
        page_num=len(json.loads(res.text)['data']['list'])
        #当前页数
        current=json.loads(res.text)['data']['current']
        print(f'------正在爬取第 {current} 页')
        return res
        
    def crawl_url(self,company_id):
        target_url=f'https://www.butian.net/Loo/submit?cid={company_id}'
        res=requests.get(url=target_url,headers=headers)
        if res.status_code==200:
            name=re.findall('name="company_name".*\n.* value="(.*)"',res.text)
            url=re.findall('name="host".*\n.* value="([^"]{4,})"',res.text)
            #print(str(name)+' '+str(url))
            #src_name=(name[0]+'\n').encode()
            #src_url=(url[0]+'\n').encode()
            try:
                src_name=(name[0]+':'+url[0]+'\n').encode()
                src_url=(url[0]+'\n').encode()
                self.save(src_name,src_url)
            except Exception as e:
                pass
            """ src_name.append(name[0]+':'+url[0])
            src_url.append(url[0]) """
            print(str(name)+':'+str(url))
    def save(self,src_name,src_url):
        with open('src_name_list.txt',mode='ab+') as file:
            file.write(src_name)
        with open('src_url_list.txt',mode='ab+') as file2:
            file2.write(src_url)    
    def main(self):
        self.title()
        #循环爬取每页
        page = int(input('请输入开始爬取的页数：')) or 1
        pages = int(input('请输入总共需要爬取的页数：')) or 20
        while True:
            res=self.crawl_id(page)
            for num in range(0,30):
                #厂商对应ID
                company_id=json.loads(res.text)['data']['list'][num]['company_id']
                self.crawl_url(company_id)
            page+=1
            if page==pages:break
if __name__ == '__main__':
    run = bt()
    run.main()
