import datetime
import re
import pandas as pd
import streamlit as st
from models.jmlrModel import Paper
from models.JMLRWebScrapModel import JMLRModel
from ext import current_page


def update_current_page(mode):
    '''
    mode为pre 前一篇；
    next 后一篇
    '''
    if mode not in ['pre', 'next']:
        return None
    d_page = {'pre': -1, 'next': 1}
    with open('ext.py', 'w', encoding='utf-8') as f:
        try:
            f.write(f"current_page = {current_page + d_page[mode]}")
        except:
            pass


@st.cache_data()
def fetch_data():
    f = open("data.txt", 'r', encoding='utf-8')
    data = eval(f.read())
    f.close()
    return data


def search(volume: int, mode: str, content, placeholder, abs_expander, bib_expander, translation_expander,
           WebScrapModel, baseMode=0):
    """
    :param volume:  卷数
    :param mode:    ID or Title
    :param content: 获取文本框的数据
    :param placeholder: 占位符，用于存放获取信息的表格
    :param abs_expander: 用于存放Abstract等详细信息
    :param bib_expander: 用于存放Bib等详细信息
    :param WebScrapModel: 爬虫模型类
    :param baseMode:
    :return: None
    """
    data = fetch_data()  # 获取数据
    urls = []  # 存放某一篇的地址

    try:
        if mode == "paperID":
            # 传入content为int类型
            try:
                paper = placePaperInfo(data, content - 1, volume, placeholder, baseMode=baseMode)
            except:
                placeholder.warning("传入错误Id")
        elif mode == 'paperTitle':
            # 先根据标题获取id,此时传入content为str
            try:
                if content == "":
                    placeholder.write(None)
                else:
                    # 思路一：正则表达式
                    result_num = \
                        re.findall('''\[{'paperId': (\d+?)}, {'paperTitle': '%s'}''' % content, str(data[volume]))[0]
                    # placeholder.markdown(result_num)
                    paper = placePaperInfo(data, int(result_num) - 1, volume, placeholder, baseMode=baseMode)
            except:
                placeholder.warning("出错啦")
        # Abstract 以及 翻译 以及 bib
        if baseMode == 1:
            paper = WebScrapModel.translateToChinese(expander=translation_expander, paper=paper,show=1)
            paper.updateBib(WebScrapModel.readBib(paper=paper))
            return paper
        if baseMode != 1:
            abs_expander.subheader(paper.paperTitle)
            WebScrapModel.readAbstract(paper, abs_expander)
            paper.updateAbstract(WebScrapModel.abstract)
            WebScrapModel.readBib(paper, bib_expander)
            paper.updateBib(WebScrapModel.readBib(paper=paper))
            paper = WebScrapModel.translateToChinese(expander=translation_expander, paper=paper)
    except:
        placeholder.warning("真出错了！")


def placePaperInfo(data, id, volume, placeholder, baseMode=0):
    """
    :param baseMode:
    :param data:    获取的数据
    :param id:      论文id
    :param volume:  卷数
    :param placeholder:     占位符
    :return: 准备以元组形式返回 abstract, paper,bib的url
    """
    if baseMode == 0:
        placeholder.success("查找成功")
    fetched_data: list = data[volume][id]
    info_name = [list(info.keys())[0] for info in fetched_data]
    info = [list(info.values())[0] for info in fetched_data]
    processed_data = list(zip(info_name, info))
    processed_data = pd.DataFrame(processed_data, columns=["INFO", "Content"]).astype("str")

    paper = Paper(
        processed_data[processed_data['INFO'] == "paperId"]["Content"].values[0],
        processed_data[processed_data['INFO'] == "paperTitle"]["Content"].values[0],
        processed_data[processed_data['INFO'] == "paperSimpleAuthor"]["Content"].values[0],
        processed_data[processed_data['INFO'] == "paperAbsURL"]["Content"].values[0],
        processed_data[processed_data['INFO'] == "paperPdfURL"]["Content"].values[0],
        processed_data[processed_data['INFO'] == "paperBibURL"]["Content"].values[0],
    )

    if baseMode == 1:
        return paper
    placeholder.table(processed_data)
    return paper


def createMarkdown(paper, WebScrapModel: JMLRModel, noDate: bool = None):
    try:
        txt = f'''
# {paper.paperId}{"—" + str(datetime.datetime.now().month) + "-" + str(datetime.datetime.now().day) if not noDate else ''}

## {paper.paperTitle}
## 

<details>
	<summary>author</summary>
	<pre>
{paper.authorDetails}</pre>
</details>

<details>
	<summary>bib</summary>
	<pre>
{paper.bib}</pre>
</details>

**keywords**:{paper.keywords}<br>
**关键词**:

## Abstract
| |备注|
|---|---|
|{JMLRModel().readAbstract(paper=paper)} | |

## Translation
| |备注|
|---|---|
|{paper.translation} | |


## 参考资料
    '''


    except:
        txt = f'''
# {paper.paperId}{"—" + str(datetime.datetime.now().month) + "-" + str(datetime.datetime.now().day) if not noDate else ''}

## {paper.paperTitle}
## 

<details>
	<summary>author</summary>
	<pre>
{paper.authorDetails}</pre>
</details>

<details>
	<summary>bib</summary>
	<pre>
{paper.bib}</pre>
</details>

**keywords**:{paper.keywords}<br>
**关键词**:

## Abstract
| |备注|
|---|---|
|{JMLRModel().readAbstract(paper=paper)} | |

## Translation
| |备注|
|---|---|
|{paper.translation} | |


## 参考资料
    '''
    return txt
