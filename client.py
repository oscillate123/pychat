import socket
import select
import errno
import sys
from appJar import gui

def button_repeat():
    while True:
        receive_things()

def connect_to_server(name):
    global username

    username = name.encode('utf-8')
    username_header = f'{len(username):<{HEADER_LENGTH}}'.encode('utf-8')
    client_socket.send(username_header + username)


def receive_things():
    try:
        while True:

            # Receive things
            remote_username_header = client_socket.recv(HEADER_LENGTH)
            if not len(remote_username_header):
                app.setTextArea('Display', '\n--- Connection closed by the server ---\n')
                print('--- Connection closed by the server ---')
                sys.exit()

            remote_username_length = int(remote_username_header.decode('utf-8').strip())
            remote_username = client_socket.recv(remote_username_length).decode('utf-8')

            remote_message_header = client_socket.recv(HEADER_LENGTH)
            remote_message_length = int(remote_message_header.decode('utf-8').strip())
            remote_message = client_socket.recv(remote_message_length).decode('utf-8')

            app.setTextArea('Display', f'{remote_username} > {remote_message}\n')


    except IOError as error:
        if error.errno != errno.EAGAIN and error.errno != errno.EWOULDBLOCK:
            print('---Reading error---')
            sys.exit()

    except Exception as error:
        print('---General error---')


def send_things(message):
        if message:
            app.setTextArea('Display', username.decode('utf-8') + ' > ' + message + '\n')
            message = message.encode('utf-8')
            message_header = f'{len(message):< {HEADER_LENGTH}}'.encode('utf-8')
            client_socket.send(message_header + message)


# GUI FUNCTION
def button(name):

    if name == 'Send':
        user_entry = app.getTextArea('usersText')
        app.clearTextArea('usersText')
        send_things(user_entry)

    elif name == ':)':
        pass

    elif name == 'OK':

        if len(app.getEntry('usernameentry')) == 0:
            app.errorBox('Error', 'Invalid username!\nPlease try again!')
        else:
            my_name = app.getEntry('usernameentry')
            connect_to_server(my_name)
            app.hideSubWindow('Login')

    elif name == 'Cancel':
        app.stop()

def enterbutton():
    button('Send')


HEADER_LENGTH = 10
# Typsikt lokalt nätverk: 192.168.51.0
# 127.0.0.0 är enbart på denna dator
#IP = '172.20.200.195'
IP = input("IP: ")
PORT = int(input("PORT: "))

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))
client_socket.setblocking(False)

app = gui('Chat')
app.setBg('Dimgray')

# SUB WINDOW (LOG IN)
app.startSubWindow("Login", modal=True)
app.startLabelFrame('Login')

app.addLabel("usernamelabel", "Please Enter Username", 0, 0, colspan=2)
app.addEntry('usernameentry', 1 , 0, colspan=2)
app.startFrame('buttonframe', 2, 1)
app.addButton('OK', button, 2, 0)
app.addButton('Cancel', button, 2, 1)
app.stopFrame()

app.setBg('Gray')
app.setEntryBg('usernameentry','silver')
app.setButtonBg('OK', 'darkgray')
app.setButtonBg('Cancel', 'darkgray')
app.stopLabelFrame()
app.stopSubWindow()

# MAIN WINDOW
app.setSize('650x400')
app.startFrame('OuterFRAME', 1, 0)
app.startLabelFrame('')

# Makes a column of empty labels to the left
for i in range(8):
    if i == 7:
        i+=1
    app.addEmptyLabel('Label' + str(i), i, 0)


# DISPLAY
app.addScrolledTextArea('Display', 0, 1, 6, 6)
app.disableTextArea('Display')
app.setTextAreaHeight('Display', 20)
app.setTextAreaWidth('Display', 70)
app.setTextAreaBg('Display', 'darkgray')

# ENTRY AREA
app.addTextArea('usersText', 7, 1, 3, 5)
app.setTextAreaHeight('usersText', 5)
app.setTextAreaWidth('usersText', 65)
app.setTextAreaBg('usersText', 'darkgray')


# BUTTONS
app.startFrame('buttonFrame', 7, 6)
app.addEmptyLabel('bl1', 0, 0)
app.addEmptyLabel('bl2', 1, 0)
app.addEmptyLabel('br1', 0, 2)
app.addEmptyLabel('br2', 1, 2)

app.addButton('Send', button, 0, 1)
app.addButton(':)', button, 1, 1)

app.setButtonBg('Send', 'Gray')
app.setButtonBg(':)', 'Gray')
app.stopFrame()


app.stopLabelFrame()
app.stopFrame() # OuterFRAME


app.showSubWindow('Login')
app.setFocus('usernameentry')

app.thread(button_repeat)
app.enableEnter(enterbutton)

app.go()
