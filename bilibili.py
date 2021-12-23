#实现bilibili视频爬取 实际上有点造轮子的意思
#毕竟有现成的 现在来介绍一下原理 bilibili将视频分为mp4 和mp3 我们负责爬取到对应链接 并且下载 这个其实我也发现了 而且从外网访问时bilibili的重定向会出问题 所以可以直接打开 中国访问会因为referer问题 无法打开
#我们目标则是合成这两个 还原原视频
import requests
import os
import re

from moviepy.editor import *



class Bilibili():
    def __init__(self,bid:str) -> None:
        self.video_url = 'https://www.bilibili.com/video/{}'.format(bid)#参数为bv号
        self.headers = {
            'referer':'https://www.bilibili.com/video/'+bid,
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
        }
        self.headers2 = {
            'cookie':"buvid3=77DCE3E2-1099-6E04-F8A2-9FECD2308C7C58045infoc; _uuid=6D7F3938-F327-4E85-E8DA-21C323410E5B259080infoc; buvid_fp=77DCE3E2-1099-6E04-F8A2-9FECD2308C7C58045infoc; sid=b16hqu5g; fingerprint=705e1eb49a4fbcc6a6b494a0d32171d2; buvid_fp_plain=77DCE3E2-1099-6E04-F8A2-9FECD2308C7C58045infoc; DedeUserID=7277814; DedeUserID__ckMd5=70925b19a945a660; SESSDATA=df7f037f%2C1655216211%2C6f6c3*c1; bili_jct=82b1a24ec51e149ac969c1de8046bc4c; CURRENT_FNVAL=2000; rpdid=|(J~Jm|~|J~k0J'uYR||uuY|); PVID=1; b_ut=5; i-wanna-go-back=2; innersign=1; CURRENT_BLACKGAP=0; blackside_state=0; b_lsid=434F126D_17DE805CCC5",
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
        }
        self.video_file = './video/'
        self.audio_file = './audio/'
        self.bv_file = './bvideo/'
        if not os.path.exists(self.video_file):
            os.mkdir(self.video_file)
        if not os.path.exists(self.audio_file):
            os.mkdir(self.audio_file)
        if not os.path.exists(self.bv_file):
            os.mkdir(self.bv_file)
        self.bv = bid

    def post_url(self,alist=None):
        r = requests.get(self.video_url,self.headers2)
        if r.status_code == 200:
            # print(r.text)
            self.get_url(r.text)
        else:
            print("你看看你是不是有问题")

    def get_url(self,s:str):
        #这个里面通过正则将视频链接和音频链接提取出来
        #在访问过程中 当然也发现了一些规律 比如<script>window.__playinfo__=(.*?)</script>的形式获取到一个json 格式格式数据 里面video 和audio 里面有我们所需要的链接 里面用64 32 16区分 64 -720p 32 -480p 16 -360p
        video_patten = r'{"id":64,"baseUrl":"(.*?)",'
        audio_patten = r'{"id":30280,"baseUrl":"(.*?)",'
        video = re.findall(pattern=video_patten,string=s)[0]
        audio = re.findall(audio_patten,string=s)[0]        
        print(video,audio)
        self.down(video)
        self.down(audio,'mp3')
        print('下载完毕准备合成')
        self.mov_clips()
        print('合成完毕'+self.bv)

    def down(self,url,mode='mp4'):
        #其实可以给这个添上标题 不过先用bv表示吧
        size = 0
        filename = self.video_file + self.bv + '.'+mode
        if mode == 'mp3':
            filename = self.audio_file + self.bv + '.'+mode
        r = requests.get(url,headers=self.headers)
        if r.status_code == 200:
            chunk_size= 1024
            # print(r.headers)
            content_size = int(r.headers['content-length'])
            # print(content_size)
            print('[文件总大小]:{:.0f} MB'.format(content_size / 1024 / 1024))
            with open(filename,'wb') as f:
                for data in r.iter_content(chunk_size=chunk_size):
                    f.write(data)
                    size += len(data)
                    print('\r'+'[下载进度]:%s%.2f%%' % ('>'*int(size*50/ content_size),float(size/content_size * 100)),end='')  
        else:
            print('出问题了',r.status_code)

    def mov_clips(self):
        #这个会将指定的两个音频和视频 文件合成成一个完整的视频 现在命名规则还没写 先将就bv号
        vd = VideoFileClip(self.video_file + self.bv + '.mp4')
        ad = AudioFileClip(self.audio_file + self.bv + '.mp3')

        vd2 = vd.set_audio(ad)
        vd2.write_videofile(self.bv_file+self.bv+ '.mp4')
B = Bilibili('BV19r4y1S7s2')
B.post_url()
# B.mov_clips()