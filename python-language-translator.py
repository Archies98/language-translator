from tkinter import *
from tkinter import ttk
from google_trans import GoogleTranslator

# draw the root
root = Tk()

# define the boundary of app on screen
len_x = 1080
len_y = 400

root.geometry('1200x400')
root.resizable(0, 0)
root.title("Data PyRates--Language Translator")
root.config(bg='ghost white')

# heading
Label(root, text="LANGUAGE TRANSLATOR", font="arial 20 bold", bg='white smoke').pack()
Label(root, text="Project Data PyRates", font='arial 20 bold', bg='white smoke', width='20').pack(side='bottom')

# Label(root, text="Enter Text", font='arial 13 bold', bg='white smoke').place(x=200, y=60)
# draw the input text box
Input_text = Text(root, font='arial 10', height=11, wrap=WORD, padx=5, pady=5, width=60)
Input_text.place(x=len_x * 0.10, y=100)

# Label(root, text="Output", font='arial 13 bold', bg='white smoke').place(x=780, y=60)
# draw the output textbox
Output_text = Text(root, font='arial 10', height=11, wrap=WORD, padx=5, pady=5, width=60)
Output_text.place(x=len_x * 0.60, y=100)

# retrieve the language list
language_list = GoogleTranslator.get_supported_languages()  # output: [arabic, french, english etc...]

src_lang = ttk.Combobox(root, values=language_list, width=22)
src_lang.place(x=len_x * 0.25, y=60)
src_lang.set(language_list[0])
dest_lang = ttk.Combobox(root, values=language_list, width=22)
dest_lang.place(x=len_x * 0.75, y=60)
dest_lang.set(language_list[0])


def translate():
    translated = GoogleTranslator(source=src_lang.get(), target=dest_lang.get()).translate(Input_text.get(1.0, END))
    Output_text.delete(1.0, END)
    Output_text.insert(END, translated)


trans_btn = Button(root, text='Translate', font='arial 12 bold', pady=5, command=translate, bg='royal blue1',
                   activebackground='sky blue')
trans_btn.place(x=len_x * 0.51, y=180)

root.mainloop()
