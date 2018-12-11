import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

class Mail(object):
    '''
    发送邮件   两参数,   收件人 和正文
    '''
    def __init__(self,address,text_data):
        self.address = address  #  收件人地址
        self.text_data = text_data  #  正文内容(连接)
        self.my_sender = '1654919279@qq.com'  # 发件人邮箱账号
        self.my_pass = '############################'  # 发件人邮箱密码(当时申请smtp给的口令)

    def send(self,):
        ret = True
        try:
            msg = MIMEText('请点击验证,%s'%self.text_data, 'plain', 'utf-8')
            msg['From'] = formataddr(["留言板官方", self.my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
            msg['To'] = formataddr(["收件人昵称",  self.address])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
            msg['Subject'] = '留言板验证-官方'  # 邮件的主题，也可以说是标题

            server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是465
            server.login(self.my_sender, self.my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
            server.sendmail(self.my_sender, [self.address, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
            server.quit()  # 关闭连接
        except Exception:  # 如果 try 中的语句执行GG，则会执行下面的 ret=False
            ret = False
        return ret




if __name__ == '__main__':
    #  测试Ok
    M = Mail('1225458568@qq.com','www.baidu.com')
    state = M.send()
    print(state)
