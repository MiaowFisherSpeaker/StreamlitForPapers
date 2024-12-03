import os.path

import streamlit as st
from models.JMLRWebScrapModel import JMLRModel
from ext import current_page
from utils.PdfReader import PDFReader
from utils.JMLRUtils import *

def JMLR_page():
    st.set_page_config(page_title="JMLR论文查询",
                       page_icon="🎈✨🧨",
                       layout="wide",
                       initial_sidebar_state="auto")
    if st.sidebar.button("Rerun without clear cache"):
        st.rerun()
    ML = JMLRModel()
    tab1, tab2, tab3= st.tabs(["查询", "浏览论文网页", "markdown预览"])

    placeholder = tab1.empty()

    abstract_expander = tab1.expander("Abstract")
    translation_expander = tab1.expander("Translation")
    bib_expander = tab1.expander("Bib_info")

    with st.sidebar:  # 先爬取数据才能用！
        volume_number = st.number_input("请输入你要爬的卷", min_value=1, max_value=25, value=25,
                                        step=1)
        st.write(f"The current volume is <font size=8 face=Calibri color=green>**{volume_number}**</font>",
                 unsafe_allow_html=True)
        ML.volume = volume_number
        ML.update_url()
        st.write("The current URL is", ML.url)
        with open("data.txt", "r", encoding="utf-8") as f:
            data = eval(f.read())
        if volume_number not in data:
            fetchDataButton = st.button("获取数据", on_click=ML.fetchInformation())  # 不知道为啥自动处理了
            processDataButton = st.button("处理数据", on_click=ML.dataProcess())
            saveDataButton = st.button("存储数据", on_click=ML.depositProcessedData())
            if saveDataButton:
                showData = st.write("展示数据", ML.papers)
            st.stop()

        # ---------------------------------------------------------------------------------
        st.write("<br>", unsafe_allow_html=True)
        volume_searchNum = st.number_input("请输入你要查询的卷1-25", min_value=1, max_value=25, value=25, step=1)
        # 搜索途径
        multiSearch = st.selectbox("筛选途径", ["paperID", "paperTitle"])
        content = st.empty()

        # searchById
        if multiSearch == "paperID":
            try:
                content = id_searchNum = st.number_input("请输入你要查询的论文序号", min_value=1, value=current_page,
                                                     step=1)
                if id_searchNum != current_page:
                    with open('ext.py', 'w', encoding='utf-8') as f:
                        f.write(f"current_page = {id_searchNum}")
            except:
                with open('ext.py', 'w', encoding='utf-8') as f:
                    f.write(f"current_page = 1")
        # searchByTitle
        elif multiSearch == "paperTitle":  # 完全匹配
            content = paperTitle_search = st.text_input("请输入你要查询的论文标题")
        searchButton = st.button("开始搜索并下载pdf",
                                 on_click=search(volume_searchNum, multiSearch, content, placeholder,
                                                 abstract_expander, bib_expander, translation_expander, ML))
        paper = search(volume_searchNum, multiSearch, content, placeholder,
                       abstract_expander, bib_expander, translation_expander, ML, baseMode=1)
        paper_url = paper.paperPdfURL
    pdf = PDFReader(paper=paper)  # 实例化
    # createMarkdownButton = st.sidebar.button("点击下载pdf生成markdown")
    # 论文数据的进一步更新
    if searchButton:
        pdf.download_pdf()  # 下载预处理
    paper = pdf.readPdf()  # 读取信息

    author, keywords = paper.authorDetails, paper.keywords
    with tab1:
        author_expander = st.expander("Author_details")
        author_expander.text(author)
        keywords_expander = st.expander("Keywords")
        keywords_expander.write(keywords)

    with tab2:
        st.write(f"{paper.paperPdfURL}")
        st.write(f'''<iframe src={paper_url} width="100%" height="2000" frameborder="no"></iframe>''',
                 unsafe_allow_html=True)

    with tab3:
        # 快捷栏，上一页，下一页。标重点？
        page_column1, page_column2, page_column3 = st.columns(3)
        with page_column1:
            pre_current_paper_button = st.button(f"上一篇{current_page - 1}")
            if pre_current_paper_button:
                update_current_page(mode='pre')
        with page_column2:
            next_current_paper_button = st.button(f"下一篇{current_page + 1}")
            if next_current_paper_button:
                update_current_page(mode='next')
        with page_column3:
            noDateButton = st.button('无日期Markdown')
            if noDateButton:
                noDateState = True
            else:
                noDateState = False

        raw_code_expander = st.expander("markdown源代码")

        txt = createMarkdown(paper=paper, WebScrapModel=ML, noDate=noDateState)
        raw_code_expander.code(txt)
        st.write(txt, unsafe_allow_html=True)

    paper.clearExtra()  # 清理多余


if __name__ == '__main__':
    JMLR_page()