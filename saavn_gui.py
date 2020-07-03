#!/usr/bin/python3
from time import sleep
import tkinter
from tkinter import *
from tkinter import messagebox
import saavn
from saavn import By,play_pause, next_song, prev_song, repeat, info, wait_and_find, initialize, fix_volume_bug
import concurrent.futures
import time
from threading import Thread

# main window configs:
main_frame = Tk()
# main_frame.configure(bg='green')
main_frame.geometry("1366x768")
main_frame.title('Saavn - Desktop - Interface')

# default font:
font = ('Ubuntu',15,'normal')

root = Frame(main_frame)
# frames:
input_frame = Frame(root)
song_choice = Frame(root)
controls_frame = Frame(root)
info_frame = Frame(root)

# button and label definitions:print
welcome_msg = Label(root,text='Welcome to Saavn...',font=('Comic Sans MS',40,'bold','italic'))
input_label = Label(input_frame, text="Enter the name of the song:", font=font)
search_bar = Entry(input_frame, font=font)
search_btn = Button(input_frame, text='Search', font=font)
play_pause_btn = Button(controls_frame,text='Play / Pause',font=font,bg='green',fg='white',command=play_pause)
next_btn = Button(controls_frame,text='Next',font=font,bg='green',fg='white',command=next_song)
prev_btn = Button(controls_frame,text='Previous',font=font,bg='green',fg='white',command=prev_song)
repeat_btn = Button(controls_frame,text='Repeat Current Song',font=font,bg='green',fg='white',command=repeat)
song_choice_label = Label(song_choice,text="Searching...",font=font)
track_label = Label(info_frame,font=font)
track_meta = Label(info_frame, font=font)
track_elapsed = Label(info_frame, font=font)

# event listeners and bindings:
def load_info(event=None):    
    track_name,meta_name,duration = info(True)

    track_label.config(text="Track name: "+track_name)
    track_meta.config(text="Album/Artist: "+meta_name)
    track_elapsed.config(text="Track duration: " +duration)

    if saavn.browser.execute_script('return MUSIC_PLAYER.getVolume()') != 100:
        saavn.browser.execute_script("MUSIC_PLAYER.setVolume(100);")

    info_frame.after(1000, load_info)

def search(event):
    def select():
        index = choice.get()
        saavn.browser.execute_script("arguments[0].click();", titles[index])

        time.sleep(3)
        saavn.browser.execute_script("window.scrollTo(0,100);")
        play_btn = wait_and_find("//p/a[@class='c-btn c-btn--primary']",By.XPATH,saavn.browser)[0]
        play_btn.click()
        
        # clear search results:
        for widget in song_choice.winfo_children():
            widget.grid_forget()

        song_choice.grid_remove()
        input_frame.grid()
        info_frame.grid(pady=100)
        controls_frame.grid()
        Thread(target=fix_volume_bug).start()
        load_info()
    
    song_choice.grid()
    song_choice_label.grid(row=0, pady=20)
    song_choice_label.config(text="Searching...")
    input_frame.grid_remove()
    info_frame.grid_remove()
    controls_frame.grid_remove()

    song_name = '+'.join(search_bar.get().split())
    data = saavn.navigate(song_name,True)

    if len(data) < 1:
        messagebox.showerror(title="Oops!", message="No results found!")
        sys.exit()

    titles = [j for i,j,k in data]

    choice = IntVar()
    
    for i,j,k in data:
        r = Radiobutton(song_choice, text=j.text+' : '+k.text,variable=choice,value=i,command=select)
        r.grid(row=i+1,column=0)
    
    song_choice_label.config(text="Select a song from the list...")

# button and label placements:
root.pack()
welcome_msg.grid(ipady=20)
input_label.grid(pady=10)
search_bar.grid(pady=10)
search_btn.grid()
input_frame.grid()
prev_btn.grid(row=0, column=0)
play_pause_btn.grid(row=0, column=1, padx=10)
next_btn.grid(row=0, column=2)
repeat_btn.grid(row=1, column=1,pady=10)
track_label.grid(sticky="W", row=0, column=0, columnspan=2)
track_elapsed.grid(sticky="W", row=1, column=0)
track_meta.grid(sticky="W", row=2, column=0)

# initial button bindings:
search_btn.bind('<Button-1>', search)

if __name__ == '__main__':
    try:
        sys.argv.append('firefox')
        sys.argv.append('off')
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(initialize)
            return_value = future.result()
            
            if return_value != True:
                raise Exception(return_value)
        try:
            main_frame.mainloop()
        except Exception as e:
            messagebox.showerror(title="Oops!", message=e)
            sleep(5)
            sys.exit(1)
    finally:
        try:
            saavn.browser.quit()
        except:
            pass
        sys.exit("Thank you for using this software. Keep rockin' 🎵🤘🎵")
