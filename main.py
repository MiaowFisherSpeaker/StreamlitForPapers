import time

import streamlit as st
import os


def Index():
    st.title("论文信息查询工具 项目目录")
    # 获取pages目录下的所有文件
    filenames = [name for name in os.listdir("pages")]
    files = [f"./pages/{name}" for name in filenames]
    print(files)
    # 为了可以github远程调用
    for i in range(len(files)):
        name = filenames[i]
        file = files[i]
        if not os.path.exists(file):
            files[i] = f"https://github.com/MiaowFisherSpeaker/StreamlitForPapers/raw/main/pages/{name}"
            print(True)
    print(files)
    labels = [" -> `go to`" + name for name in filenames]
    for page, label in zip(files, labels):
        st.page_link(page=page, label=label)

    project_intro = """
    该项目是一个基于Streamlit的论文信息查询工具，主要用于查询JMLR上的论文信息,
    
    并且根据此项目可自行修改拓展到其他会议期刊。比如CVPR
    
    不过这个只是一个摘要阅读的工具以及实现一个简单的markdown文本记录功能。"""

    def stream_text():
        for text in project_intro:
            yield text
            time.sleep(0.01)

    st.write_stream(stream_text)

if __name__ == '__main__':
    Index()
