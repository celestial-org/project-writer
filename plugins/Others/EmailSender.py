from hydrogram import Client, filters
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib, os

SERVER = os.getenv("SMTP")
EMAIL = os.getenv("EMAIL")
EMAIL_PW = os.getenv("EMAIL_PW")
server = smtplib.SMTP(SERVER, 587)
registers = []

def sendmail(subject, receiver, content):
    server.starttls()
    server.login("bosuutap@alwaysdata.net", "Tlc@1000")
    msg = MIMEMultipart()
    msg['From'] = EMAIL
    msg['To'] = receiver
    msg['Subject'] = subject
    msg.attach(MIMEText(content, 'markdown'))
    server.sendmail(EMAIL, receiver, msg.as_string())
    server.quit()
    print("Email sent successfully")
    
@Client.on_message(filters.command("set_mail_server") & filters.user(5665225938))
def set_mail_server(c, m):
    for i in m.command:
        if i.startswith("email:"):
            os.environ["EMAIL"]=i.replace("email:", "")
        if i.startswith("server:"):
            os.environ["SMTP"]=i.replace("server:", "")
        if i.startswith("password:"):
            os.environ["EMAIL_PW"]=i.replace("password:", "")
    m.reply("OK")
    
@Client.on_message(filters.command("register"))
def registering(c, m):
    global registers
    user = m.from_user.id
    if "@" in m.text:
        for i in m.command:
            if "@" in i:
                registers.append({"user": user, "email": i})
        m.reply("Đã đăng ký", quote=True)
        
@Client.on_message(filters.command("cancel_email"))
def cancel_register(c, m):
    global registers
    for i in registers:
        if i["user"] == m.from_user.id:
            registers.remove(i)
    m.reply("OK", quote=True)
            
    
def _email_(_, __, m):
    return os.getenv("EMAIL") is not None
   
@Client.on_message(filters.text & filters.group & filters.create(_email_), group=3)
def send_update(c, m):
    fn = m.from_user.first_name
    chat = m.chat.title
    if m.from_user.last_name:
        ln = m.from_user.last_name
        subject = f"**{fn} {ln}** from chat **{chat}**"
    else:
        subject = f"**{fn}** from chat **{chat}**"
    content = m.text
    if registers:
        for user in registers:
            sendmail(subject, user["email"], content)