# downloadbilibili
记得pip install moviepy 下个库 方便我们代码运行
引用方式 
from moviepy.editor import *
想法来源 其实我自己也知道 用外网访问时 估计b站referer有问题 让我直接给打开了 发现现在音频 视频分离的现状
有一天看到https://www.bilibili.com/video/BV1Fi4y1o7PJ?p=46这个时 感觉是时候了 就参考了一下 里面 简单学习了 一下moviepy的用法 发现这个库还挺好用的
以后批量处理视频 说不定会用到呢

想法很多 暂时就到这了

2021.12.24凌晨开写 醒来后继续写了会
顺利写完了 能通过bv号 爬取这个视频下 完整的所有视频 分p也全部获取到
这得益于爬取时 点分p视频时 看到的network 
https://api.bilibili.com/x/player/playurl
虽然里面的session我没有解密出来 不过我发现parasms 里面 随着参数的增多和减少 返回来的东西不太一样 只有cid 和 bv是不行的
cid 获取方式 是直接用的api https://api.bilibili.com/x/web-interface/view?bvid={} 这样就导致上个版本写的让我觉得完全不行 索性一切顺利 还发现 1080 对应的id是80 
又让我想吐槽那个教学视频了 正则直接写的id:64  我这个默认爬最高的 也没有用到正则了
最后        parasms = {
            'cid':cid,
            'bvid':self.bv,
            'qn':64,
            'otype':'json',
            'fourk':0,
            'fnval':2000
        }参数形式也有了
        后面就简简单单了 没有写爬取大量bv号 这种功能 或者什么下载一个up的指定分类视频 这个功能以前就写过 就偷个懒 这个能用就行 直接运行bilibili.py就行
