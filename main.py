import pafy
from os.path import splitext
from os import rename, makedirs
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from threading import *


DOWNLOAD_FOLDER = r'C:\Users\wlgam\Downloads\YoutubeDownloader'

# PAFY
def show_download_details(total, recvd, ratio, rate, eta):
    total = total/(1024*1024)
    recvd = recvd/(1024*1024)
    progress = ratio*100
    lb_info.configure(text=f'[{int(progress)}%]   {recvd:.2f}MB / {total:.2f}MB   |   {int(eta)} sec')
    v_progress.set(progress)
    program.update()


def disable_buttons():
    bt_mp4.configure(state='disabled')
    bt_mp3.configure(state='disabled')
    lb_info.configure(text='Waiting for download ...')


def enable_buttons():
    bt_mp4.configure(state='active')
    bt_mp3.configure(state='active')
    lb_info.configure(text='Nothing right now')
    v_progress.set(0)


def download_mp4(video_url):
    disable_buttons()
    try:
        out_file = pafy.new(video_url)
        out_file.getbest().download(filepath=DOWNLOAD_FOLDER,callback=show_download_details)
        v_url.set('')
    except:
        messagebox.showerror('Something went wrong', 'Check the spelling and availability of the video.')
    else:
        messagebox.showinfo('Success', 'Video downloaded successfully')
    finally:
        enable_buttons()
        

def download_mp3(video_url):
    disable_buttons()
    try:
        out_file = pafy.new(video_url)
        out_file.getbest().download(filepath=DOWNLOAD_FOLDER, callback=show_download_details)
        type_ = out_file.getbest().generate_filename()
        base, ext = splitext(type_)
        new_file = base + '.mp3'
        rename(type_, new_file)
        v_url.set('')
    except:
        messagebox.showerror('Something went wrong', 'Check the spelling and availability of the video.')
    else:
        messagebox.showinfo('Success', 'Audio downloaded successfully')
    finally:
        enable_buttons()


# UTILS
def create_app_folder():
    makedirs(DOWNLOAD_FOLDER, exist_ok=True)
    with open(DOWNLOAD_FOLDER+r'\readme.txt', 'w') as file:
        file.write('YouTubeDownloader is an open-source project available at:\
             \n\nhttps://github.com/jwesleylima/YouTubeDownloader-Tkinter-Python\
             \n\nThis project was conceived by Wesley Lima. Visit the developer at GitHub:\
             \n\nhttps://github.com/jwesleylima\n\n(c) 2021 JWesleyLima. All rights reserved.')


# THREAD
def threading_mp4():
    t1=Thread(target=lambda: download_mp4(v_url.get()))
    t1.start()


def threading_mp3():
    t1=Thread(target=lambda: download_mp3(v_url.get()))
    t1.start()


# TKINTER
program = Tk()
program.title('Youtube Video/Audio Downloader | @jwesleylima')
program.geometry('380x600+100+100')
create_app_folder()

v_url = StringVar()
v_progress = DoubleVar()
v_progress.set(0)

img_youtube = PhotoImage(file='res/youtube-icon.png')
lb_youtube = Label(program, image=img_youtube)
lb_youtube.pack()

lb_title = Label(program, text='YouTube\nDownloader', font=('Arial', 18))
lb_title.pack(pady=15)

lb_help = Label(program, text='Enter the full URL or just the video ID')
lb_help.pack()

et_url = Entry(program, width=20, font=('Arial', 16), textvariable=v_url)
et_url.pack()

bt_mp4 = Button(program, text='DOWNLOAD MP4', background='#e22', width=18, 
    foreground='#fff', font=('Arial', 12), command=threading_mp4)
bt_mp4.pack(pady=12)

bt_mp3 = Button(program, text='DOWNLOAD MP3', background='#e22', width=18, 
    foreground='#fff', font=('Arial', 12), command=threading_mp3)
bt_mp3.pack()

fr_status = LabelFrame(program, text='Download status', borderwidth=1, relief='solid')
fr_status.pack(pady=20)

lb_info = Label(fr_status, text='Nothing right now', font=('Arial', 14))
lb_info.pack(padx=20, expand=True, fill=X)

pb = ttk.Progressbar(fr_status, variable=v_progress,
	maximum=100)
pb.pack(padx=20, pady=25, expand=True, fill=X)

if __name__ == '__main__':
    program.mainloop()
