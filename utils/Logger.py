class Logger:
    def __init__(self, mode=0):
        self.mode = 0

    def log(self, content: str):
        with open("log.txt", "a+", encoding='utf-8') as f:
            f.write(content+"\n")

    def clear(self, flag=0):
        if flag == 1:
            f = open("log.txt","w",encoding="utf-8")
            f.write("")
            f.close()