from tkinter import *
from tkinter import filedialog
class CodeEditor:
     def __init__(self, master):
        self.master = master
        master.title("PyCode Editor by rakuzan2weak")
         # Create the text area
        self.text_area = Text(master, undo=True)
        self.text_area.pack(fill=BOTH, expand=YES)
        self.text_area.focus()
         # Create the line numbers column
        self.line_numbers = Text(master, width=4, padx=4, takefocus=0, border=0, background="lightgray", state="disabled")
        self.line_numbers.pack(side=LEFT, fill=Y)
         # Create the scrollbar
        self.scrollbar = Scrollbar(master)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.text_area.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.text_area.yview)
         # Create the menu bar
        self.menu_bar = Menu(master)
        self.master.config(menu=self.menu_bar)
         # Create the file menu
        self.file_menu = Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="New", command=self.new_file)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_command(label="Save As", command=self.save_file_as)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=master.quit)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
         # Create the edit menu
        self.edit_menu = Menu(self.menu_bar, tearoff=0)
        self.edit_menu.add_command(label="Undo", command=self.undo)
        self.edit_menu.add_command(label="Redo", command=self.redo)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Cut", command=self.cut)
        self.edit_menu.add_command(label="Copy", command=self.copy)
        self.edit_menu.add_command(label="Paste", command=self.paste)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Select All", command=self.select_all)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)
         # Create the view menu
        self.view_menu = Menu(self.menu_bar, tearoff=0)
        self.view_menu.add_command(label="Toggle Line Numbers", command=self.toggle_line_numbers)
        self.menu_bar.add_cascade(label="View", menu=self.view_menu)
         # Create the status bar
        self.status_bar = Label(master, text="Line 1, Column 1", bd=1, relief=SUNKEN, anchor=W)
        self.status_bar.pack(side=BOTTOM, fill=X)
         # Bind the events
        self.text_area.bind("<Key>", self.key_event)
        self.text_area.bind("<Button-1>", self.mouse_click)
        self.text_area.bind("<Motion>", self.mouse_motion)
        self.text_area.bind("<Control-y>", self.redo)
        self.text_area.bind("<Control-Y>", self.redo)
        self.text_area.bind("<Control-z>", self.undo)
        self.text_area.bind("<Control-Z>", self.undo)
        self.text_area.bind("<Control-f>", self.find)
        self.text_area.bind("<Control-F>", self.find)
        self.text_area.bind("<Control-a>", self.select_all)
        self.text_area.bind("<Control-A>", self.select_all)
     def new_file(self):
        self.text_area.delete('1.0', END)
        self.update_line_numbers()
        self.master.title("Code Editor")
     def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[('Text Files', '*.txt'), ('Python Files', '*.py')])
        if file_path:
            self.text_area.delete('1.0', END)
            with open(file_path, 'r') as f:
                self.text_area.insert(END, f.read())
            self.update_line_numbers()
            self.master.title(f"Code Editor - {file_path}")
     def save_file(self):
        file_path = self.master.title().replace("Code Editor - ", "")
        if file_path:
            with open(file_path, 'w') as f:
                f.write(self.text_area.get('1.0', END))
                self.master.title(f"Code Editor - {file_path}")
        else:
            self.save_file_as()
     def save_file_as(self):
        file_path = filedialog.asksaveasfilename(defaultextension='.txt', filetypes=[('Text Files', '*.txt'), ('Python Files', '*.py')])
        if file_path:
            self.master.title(f"Code Editor - {file_path}")
            with open(file_path, 'w') as f:
                f.write(self.text_area.get('1.0', END))
            self.update_line_numbers()
     def undo(self, event=None):
        try:
            self.text_area.edit_undo()
            self.update_line_numbers()
        except:
            pass
     def redo(self, event=None):
        try:
            self.text_area.edit_redo()
            self.update_line_numbers()
        except:
            pass
     def cut(self):
        self.text_area.event_generate("<<Cut>>")
     def copy(self):
        self.text_area.event_generate("<<Copy>>")
     def paste(self):
        self.text_area.event_generate("<<Paste>>")
     def select_all(self, event=None):
        self.text_area.tag_add(SEL, "1.0", END)
        self.text_area.mark_set(INSERT, "1.0")
        self.text_area.see(INSERT)
        return 'break'
     def find(self, event=None):
        # Implement the find functionality here
        pass
     def key_event(self, event):
        self.update_line_numbers()
     def mouse_click(self, event):
        self.update_line_numbers()
     def mouse_motion(self, event):
        self.status_bar.config(text=f"Line {self.text_area.index(CURRENT).split('.')[0]}, Column {self.text_area.index(CURRENT).split('.')[1]}")
     def update_line_numbers(self):
        lines = str(self.text_area.get(1.0, END)).count('\n')
        line_numbers_text = ""
        for line in range(1, lines+2):
            line_numbers_text += str(line) + '\n'
        self.line_numbers.config(state=NORMAL)
        self.line_numbers.delete('1.0', END)
        self.line_numbers.insert(END, line_numbers_text)
        self.line_numbers.config(state=DISABLED)
     def toggle_line_numbers(self):
        if self.line_numbers.winfo_ismapped():
            self.line_numbers.pack_forget()
        else:
            self.line_numbers.pack(side=LEFT, fill=Y)
root = Tk()
editor = CodeEditor(root)
root.mainloop()