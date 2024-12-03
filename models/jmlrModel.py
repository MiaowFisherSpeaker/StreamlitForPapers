class Paper:
    def __init__(self, paperId=None, paperTitle=None, paperSimpleAuthor=None, paperAbsURL=None, paperPdfURL=None, paperBibURL=None):
        self.paperId = paperId
        self.paperTitle = paperTitle
        self.paperSimpleAuthor = paperSimpleAuthor
        self.paperAbsURL = paperAbsURL
        self.paperPdfURL = paperPdfURL
        self.paperBibURL = paperBibURL
        self.abstract = ""
        self.translation = ""
        self.keywords = ""
        self.authorDetails = ""
        self.bib = ""

    def updatePaperInfo(self, paperId, paperTitle, paperSimpleAuthor, paperAbsURL, paperPdfURL, paperBibURL):
        self.paperId = paperId
        self.paperTitle = paperTitle
        self.paperSimpleAuthor = paperSimpleAuthor
        self.paperAbsURL = paperAbsURL
        self.paperPdfURL = paperPdfURL
        self.paperBibURL = paperBibURL

    def updateAbstract(self, abstract):
        self.abstract = abstract

    def updateTranslation(self, translation):
        self.translation = translation

    def updateKeywords(self, keywords):
        self.keywords = keywords.replace("\n","")

    def updateAuthorDetails(self, authorDetails):
        self.authorDetails = authorDetails

    def updateBib(self, bib):
        self.bib = bib

    def clearExtra(self):
        self.abstract = ""
        self.translation = ""
        self.keywords = ""
        self.authorDetails = ""
        self.bib = ""
