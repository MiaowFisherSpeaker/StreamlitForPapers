import os.path
import re
import time

import requests

from models.jmlrModel import Paper
from utils.Logger import Logger
from utils.Translator import YouDaoFanYi

class JMLRModel:
    def __init__(self, url="https://www.jmlr.org", volume=23, flag=0):
        # url相关
        self.raw_url = url  # 原输入url     https://www.jmlr.org
        self.url = url  # 更改后的url       https://www.jmlr.org/papers/v.../...

        self.volume = volume  # 卷数参数
        self.parameters = ""  # 文章参数
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
        }  # 请求头，防止反爬

        # 日志相关
        self.logger = Logger()  # 调试
        self.flag = flag  # flag为1开启调试，默认关闭（传递其他值）

        # 数据存放位置
        self.temp_html = "temp_html.txt"  # 待处理html文件
        self.processedData = "data.txt"  # 处理好的data文件，格式在后面说明

        # 爬取信息相关
        self.status_code = 404  # 返回网页信息状态
        with open(self.temp_html, "r", encoding="utf-8") as f:
            self.raw_text = f.read()  # 获取原数据
        with open(self.processedData, "r", encoding="utf-8") as f:
            txt = f.read()
            if txt == "":
                self.papers = {}
            elif "{" in txt and "}" in txt:
                self.papers = eval(txt)  # 容器，存放处理过的data
        # self.Paper = Paper  # 存放指定论文的容器

        # 翻译相关
        self.abstract = ""  # 摘要暂时存储，方便后面调用
        self.bib = ""

    # 设置url的修饰参数 volume 和 parameter
    def setParameter(self, volume, parameter):
        self.volume = volume
        self.parameters = parameter

    # 更新url
    def update_url(self):
        self.url = self.raw_url  # 重置基础url
        self.url += "/papers/v%d" % self.volume
        self.url += "/%s" % self.parameters

    # 发送请求获取数据data: 即 raw_text
    def fetchInformation(self):
        self.update_url()
        try:
            r = requests.get(self.url, headers=self.headers)
            r.encoding = "utf-8"
            status_code = r.status_code
            self.status_code = status_code
            self.raw_text = r.text
            with open(self.temp_html, "w", encoding="utf-8") as f:
                f.write(f"{self.raw_text}")
        except:
            pass
        if self.flag == 1:
            self.logger.log(f'''【{time.strftime("%Y年%m月%d日-%H时%M分%S秒")}】\n
                                    \t你访问的url为{r.url},返回http状态码为{status_code}\n''')
            if status_code == 200:
                self.logger.log("\t请求成功\n")
            elif status_code == 400:
                self.logger.log("\tNot Found\n")
            else:
                self.logger.log("\t无响应\n")

    # 数据打包放到容器里
    def dataProcess(self):
        # 论文序号id,存储位置papersVolume, 论文标题paperTitle, 论文地址paperURL, 论文关键词paperKeywords(待做),作者paperAuthor待做， 是否有代码beCoded
        self.raw_text.replace("\n", "")
        papersVolume = int(re.findall("<h1>JMLR Volume(.+?)</h1>", self.raw_text)[0])  # 卷几
        paperSimpleAuthor = re.findall("<b><i>(.+?)</i></b>", self.raw_text)  # 简要作者
        paperSimpleInfo = re.findall("</b>; (.+?). ", self.raw_text)  # 简明信息原信息
        paperId = [int(re.findall("\((\d+?)\):1&minus", x)[0]) for x in paperSimpleInfo]  # 论文序号
        paperTitle = re.findall("<dt>(.+?)</dt>", self.raw_text)  # 论文标题
        paperAbsURL = [self.raw_url + x for x in re.findall("\[<a href='(.+?)'>abs</a>\]", self.raw_text)]  # 论文摘要url
        paperPdfURL = [self.raw_url + x for x in
                       re.findall("\[<a target=_blank href='(.+?)'>pdf</a>\]", self.raw_text)]  # 论文PDFurl
        paperBibURL = [self.raw_url + x for x in
                       re.findall("\[<a href=\"(.+?)\">bib</a>\]", self.raw_text)]  # 论文bib url
        # 处理bib获取其他数据
        if self.papers.get(papersVolume, 0) == 0:
            self.papers[papersVolume] = list(
                zip(paperId, paperTitle, paperSimpleAuthor, paperAbsURL, paperPdfURL, paperBibURL))
            self.papers[papersVolume] = [[{"paperId": a},
                                          {"paperTitle": b},
                                          {"paperSimpleAuthor": c},
                                          {"paperAbsURL": d},
                                          {"paperPdfURL": e},
                                          {"paperBibURL": f}] for a, b, c, d, e, f in self.papers[papersVolume]]
        ''' 故data 结构如下: 
            data = {volumeNum: volumeContent :list}
                               volumeContent = paperInfos :list
                                               paperInfos = [paperInfo1 :dict,paperInfo2 :dict,...]
                                                             paperInfo = [{"paperId": a},
                                                                         {"paperTitle": b},
                                                                         {"paperSimpleAuthor": c},
                                                                         {"paperAbsURL": d},
                                                                         {"paperPdfURL": e},
                                                                         {"paperBibURL": f}]       
        '''
        # self.papers[papersVolume] = paperBibURL

    def depositProcessedData(self):
        # 网页中可直接调用papers 不做详细处理
        with open(self.processedData, "w", encoding="utf-8") as f:
            f.write(str(self.papers))
        if self.flag == 1:
            # self.logger.log(f"self.raw_text为{self.raw_text}")
            self.logger.log(str(self.papers)[:100])  # 只显示前100个字符

    def readAbstract(self, paper, expander=None):
        '''
        :param expander: 存放的容器（st.expander)
        :return: None
        '''
        # url 格式为   https://jmlr.org/papers/volumeNum/specialId.html
        # 判断content类型，可能为int（id）或者str（title）
        # 先在data里直接找url
        try:
            r = requests.get(paper.paperAbsURL, headers=self.headers)
            r.encoding = "utf-8"
            status_code = r.status_code
            self.status_code = status_code
            abstract_html = r.text.replace('\n', '')
            if self.flag == 1:
                self.logger.log(f"status_code={status_code}")
                self.logger.log(f"{abstract_html}")
            paperTitle = re.findall("", abstract_html)
            self.abstract = abstract_txt = re.findall('''<p class="abstract">(.+?)</p>''', abstract_html)[0]
            if expander is not None:
                expander.markdown("<font size=4 face=Calibri>" + abstract_txt + "</font>", unsafe_allow_html=True)
            else:
                return self.abstract

        except:
            pass
        return self.abstract

    def readBib(self, paper, expander=None):
        try:
            r = requests.get(paper.paperBibURL, headers=self.headers)
            r.encoding = "utf-8"
            self.bib = bib_html = r.text.replace(", ", ",\n")
            if expander is not None:
                expander.text(f'{bib_html}')
            else:
                expander.text(f'{bib_html}')
                return self.bib
        except:
            pass

    # 翻译功能(google,百度,有道...)  因为需要网站接口，放到爬虫模型里  # 不再做翻译
    def translateToChinese(self, paper: Paper, expander=None, content=None,show=0):
        '''
        1. 谷歌翻译原本使用googletrans包
        对应网站  https://py-googletrans.readthedocs.io/en/latest/  有点不好用
        2. 现在使用 github上的google翻译，失败
        3. 使用有道。github上找的不行。自己使用了网上的
        '''
        translator = YouDaoFanYi()
        if content is not None:
            translatedStr = translator.connect_trans(content)
            return translatedStr

        if expander is not None and content is None:
            translatedStr = translator.connect_trans(self.abstract)
            paper.updateTranslation(translatedStr)
            if show==1:
                expander.write(translatedStr)
            return paper

    def clear_log(self, flag=0):  # 清理"logger.py" 其中flag=1时清空(原理，写一个"")
        self.logger.clear(flag)


if __name__ == '__main__':        # use WebScrapModel
        ML = JMLRModel(volume=24, flag=1)
        ML.fetchInformation()  # 获取原数据
        # process data
        ML.logger.clear(flag=1)
        ML.dataProcess()
        ML.depositProcessedData()
