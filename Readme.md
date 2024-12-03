# Streamlit 论文生成器

文档更新

| 时间      | 更新内容             | 修改人             |
| --------- | -------------------- | ------------------ |
| 2024.12.3 | 重置项目，初始化文档 | MiaowFisherSpeaker |

项目简要介绍：

利用Streamlit和翻译Api快速生成中文版论文大致信息的markdown，方便二次修改。

使用工具：

- Streamlit
- pdf相关软件包（pdfplumber）
- 简单的requests爬虫。
- 翻译API(自行解决)

## 一、教程：从配置环境开始

1. ### 配置环境

   * 选用是[Miniconda](https://docs.anaconda.com/miniconda/)`https://docs.anaconda.com/miniconda/`进行python环境管理;

     下载完成后，创建一个名为`StreamlitApp`的环境，用python=3.12指定python版本

     ```powershell
     conda create -n StreamlitApp python=3.12
     ```

   * 选用[Streamlit](https://streamlit.io/)`https://streamlit.io/`作为开发栈。

     API文档以及使用文档，都可以在Docs里找到。使用非常方便。

   * 安装Streamlit 这个Package

     `conda activate StreamlitApp`进入该环境

     `pip install streamlit` 在该环境下pip安装

   * 备注，所有的API文档均可在[Documentation](https://docs.streamlit.io/)的Develop的 [API reference [+] ](https://docs.streamlit.io/develop/api-reference)里找到。

   * 可以`pip install -r requirements.txt`

2. ### 开发，仅本地，不去部署（不是正经的开发教程）
   
   * **需求分析**
   
     1. 明确哪个期刊
   
     2. tab式页面布局，划分App为查询、网页浏览、markdown预览
   
     3. 查询需要做到的是
   
         [JMLR](https://www.jmlr.org/papers/)
   
        对于一篇论文的基础信息，需要如下信息
   
        | 属性                | 介绍       | 备注      |
        |-------------------|----------|---------|
        | paperTitle        | 论文标题     |         |
        | paperSimpleAuthor | 论文作者     |         |
        | paperAbsURL       | 论文摘要URL  | 主要从这里提取 |
        | paperPdfURL       | 论文pdfURL |         |
        | paperBibURL       | 论文BibURL |         |
   
        进一步
   
        需要Abstract、翻译、作者信息、Bibinfo、关键词
   
     4. 网页浏览，以嵌入网页的iframe样式将pdf放入，进行预览。
   
        只要第三步做好就很容易解决。
   
     5. markdown生成器
   
        可以做成flask的blueprint(蓝图)那种样式，然后用string的replace替换或者其他方式。
   
        此界面分为：
   
        1.markdown源代码。
   
        2.markdown预览
   
     6. 其他功能：
   
        1. 搜索功能的完善
   
           1. 指定JMLR卷数
           2. 通过ID查询（从爬虫知道的拥有ID)
           3. 通过论文名称查询，或者不完全的关键词匹配
   
        2. markdown生成器的优化
   
           暂时没想法
   
     7. 界面设计优化。
   
        1. 添加占位符、expander等
   
     8. 翻译功能
   
        这里选用的是[有道API](https://ai.youdao.com/DOCSIRMA/html/自然语言翻译/API文档/文本翻译服务/文本翻译服务-API文档.html)`https://ai.youdao.com/DOCSIRMA/html/自然语言翻译/API文档/文本翻译服务/文本翻译服务-API文档.html`
        
        
   
   * **项目结构介绍**

​		/  ...根目录（项目目录）

​		/models/ 					  ......模型包

​			 /jmlrModel.py 			......JMLR论文模型 ，存储论文数据

​			/JMLRWebScrapModel.py      ......JMLR论文信息爬虫

​		/pages/ 					     ......streamlit的网页分页存放位置

​			/01HomePage.py		    ......主页

​			/02JMLR.py                               ......机器学习期刊工具页

​			/03CVPR.py                               ......计算机视觉工具页（待做）

​		/utils/ 						......工具包

​			/Logger.py 				......日志（简单）

​			/Translator.py 			 ......翻译API

​			/JMLRUtils.py			   ......JMLR论文页的工具函数

​			/PdfReader.py			 ......pdf阅读提取信息工具，效果不太好

​		/config.py 				        ......配置文件存放API密钥等(**按照如下创建**)

```python
class CONFIG:
    # 有道翻译API信息
    APP_KEY=你的APPKEY
    APP_SECRET=你的APPSECRET
```
​		/main.py					   ......程序主入口

​		/Readme.md                                    ......你正在读的这个

​		/requirements.txt                           ......依赖包  

​		/ext.py 					     ......随便命名的（不做修改了）存放当前部分信息

​        	/data.txt                    			......(后期自动生成，存放处理数据)

​		/temp_html.txt                    	     ......(后期自动生成，存放爬取数据)

​	为了方便调试。可以在Pycharm在右上角的绿色三角添加Shell文本脚本为`streamlit run ./main.py`





3.  ## 本地运行

   - 配置环境

     - Windows操作系统。markdown为Typora编写，浏览器使用的是联想浏览器，其实无影响。python软件包管理使用conda。使用[网易有道翻译API](https://ai.youdao.com/DOCSIRMA/html/自然语言翻译/API文档/文本翻译服务/文本翻译服务-API文档.html)(链接为文档)

     - `conda create -n your_env_name python=3.12`

     - 切换环境为your_env_name或者使用pycharm选择对应环境，重新启动终端窗口。

       conda切换命令为`conda activate your_env_name`

     - `pip install -r requirement.txt`

   - 进入主目录

     - 可以右键以Pycharm项目打开目录
     - 确保根目录包含main.py即可
     - 如果想运行翻译功能，根目录新建config.py。按照2中提示填写APP_KEY和APP_SECRET
     - 进入命令行（也确保是项目目录），运行`streamlit run ./main.py`
     - 进入项目，点击侧边栏JMLR。
     - 选择卷数，会提示下载，处理以及保存。依次点击。
       - 分别对应着爬虫爬、数据处理、保存本地
     - 选择论文ID，会有默认值在ext.py里
     - 目前鲁棒性没有做得很好，不打算维护了。因为API免费额度快用完了。
