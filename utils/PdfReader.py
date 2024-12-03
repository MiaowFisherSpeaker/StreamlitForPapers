import io
import os.path

import requests
import pdfplumber

from models.jmlrModel import Paper


class PDFReader:
    def __init__(self, save_path='./temp_pdf/', pdf_name='tempPdf', pdf_url=None, paper: Paper = None, paperMode=True):
        self.save_path = save_path
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        self.pdf_name = pdf_name
        if paperMode:
            self.pdf_url = paper.paperPdfURL
            self.paper: Paper = paper
        else:
            self.pdf_url = pdf_url
        self.paperMode = paperMode

    def download_pdf(self):
        send_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
            "Connection": "keep-alive",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.8"}
        response = requests.get(self.pdf_url, headers=send_headers)
        bytes_io = io.BytesIO(response.content)
        with open(self.save_path + "%s.PDF" % self.pdf_name, mode='wb') as f:
            f.write(bytes_io.getvalue())
            print('%s.PDF,下载成功！' % self.pdf_name)

    def readPdf(self):
        if self.paperMode:
            with pdfplumber.open('./temp_pdf/tempPdf.PDF') as pdf:
                for i, page in enumerate(pdf.pages):
                    if i == 1:
                        break
                    text = page.extract_text()
                    # print(text)
                    # 作者[x1,x2] 关键词[x3,x4]
                    x1 = text.replace("\n", " ").find(self.paper.paperTitle)
                    x1 += len(self.paper.paperTitle) + 1
                    x2 = text.find("Editor")
                    x3 = text.find("Keywords")
                    x4 = text.find("1. Introduction")
                    authorDetails = text[x1:x2]
                    keywords = text[x3:x4][9:]
                    self.paper.updateKeywords(keywords)
                    self.paper.updateAuthorDetails(authorDetails)
                    return self.paper
        else:
            with pdfplumber.open('./temp_pdf/tempPdf.PDF') as pdf:
                for i, page in enumerate(pdf.pages):
                    if i == 1:
                        break
                    text = page.extract_text()
                    print(text)
                    print("-----------分割线----------------")
                    # 作者[x1,x2] 关键词[x3,x4]
                    paperTitle = "Joint Estimation and Inference for Data Integration Problems based on Multiple Multi-layered Gaussian Graphical Models"
                    x1 = text.replace("\n", " ").find(paperTitle)
                    x1 += len(paperTitle) + 1
                    x2 = text.find("Editor") - 1
                    x3 = text.find("Keywords")
                    x4 = text.find("1. Introduction")
                    print(text[x1:x2])
                    print("----------------------------------------------")
                    print(text[x3:x4])


if __name__ == '__main__':
    save_path = './temp_pdf/'
    pdf_name = 'tempPdf'
    pdf_url = "https://www.jmlr.org/papers/volume23/18-131/18-131.pdf"
    # download_pdf(save_path, pdf_name, pdf_url)
    pdfReader = PDFReader(save_path, pdf_name, pdf_url, paperMode=False)
    pdfReader.readPdf()
