import re
import requests
import hashlib
import time
from concurrent.futures import ThreadPoolExecutor
p=ThreadPoolExecutor(30) #����1���̳��У������̸߳���Ϊ30����


def get_index(url):
    respose = requests.get(url)
    if respose.status_code==200:
        return respose.text

def parse_index(res):
    res=res.result() #����ִ����Ϻ󣬵õ�1������
    urls = re.findall(r'class="items".*?href="(.*?)"', res,re.RegexFlag.S)  # re.S ���ı���Ϣת����1��ƥ��
    for url in urls:
        p.submit(get_detail(url))  #��ȡ����ҳ �ύ���̳߳�



def get_detail(url):  #ֻ����1����Ƶ
        if not url.startswith('http'):
            url='http://www.xiaohuar.com%s' %url
        result = requests.get(url)
        if result.status_code==200 :
            mp4_url_list = re.findall(r'id="media".*?src="(.*?)"', result.text, re.RegexFlag.S)
            if mp4_url_list:
                mp4_url=mp4_url_list[0]
                print(mp4_url)
                # save(mp4_url)


def save(url):
    video = requests.get(url)
    if video.status_code==200:
        m=hashlib.md5()
        m.updata(url.encode('utf-8'))
        m.updata(str(time.time()).encode('utf-8'))
        filename=r'%s.mp4'% m.hexdigest()
        filepath=r'D:\\%s'%filename
        with open(filepath, 'wb') as f:
            f.write(video.content)

def main():
    for i in range(5):
        p.submit(get_index,'http://www.xiaohuar.com/list-3-%s.html'% i ).add_done_callback(parse_index)
        #1���Ȱ�����ҳ������get_index���첽�ύ���̳߳�
        #2��get_index����ִ����󣬻�ͨ���ص���add_done_callback������֪ͨ���̣߳�������ɣ�
        #2����get_indexִ�н����ע���߳�ִ�н���Ƕ��󣬵���res=res.result()���������ܻ�ȡ����ִ�н������������������parse_index
        #3��parse_index����ִ����Ϻ�
        #4��ͨ��ѭ�����ٴΰѻ�ȡ����ҳ get_detail���������ύ���̳߳�ִ��



if __name__ == '__main__':
    main()