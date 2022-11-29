import csv
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from unicodedata import category

data = []
labelled_data = []
categories = [
    "Appearance",
    "Financial status",
    "Social status",
    "Crime & violence",
    "Mistreatment & death",
    "Personality & behavior",
    "Competence & ability",
    "Morality",
    "Value & belief",
    "Health",
    "Family & relationship",
    "Culture",
    "Not offensive/grammatically wrong/\nambiguous/too narrow",
]

categories_dict = dict(enumerate(categories))

class Tool():
    def __init__(self):
        self.i = 0
        master = Tk()
        master.title('Bias Evaluation Tool')
        menubar = Menu(master)
        master.config(menu=menubar)
        file_menu = Menu(menubar,tearoff=0)
        menubar.add_cascade(label='Files', menu=file_menu)
        file_menu.add_command(label='Load file', command=self.load)
        file_menu.add_command(label='Save file', command=self.save)

        frame1 = Frame(master)
        frame1.pack(fill=X)

        label_adj = Label(frame1, text='Sentence:     They ')
        label_adj.grid(row=1, column=0, sticky='w')
        self.text_sentence = Text(frame1, width=80, height=1)
        self.text_sentence.grid(row=1, column=1, sticky='w')

        label1 = Label(frame1, text='Classification task:')
        label1.grid(row=2, column=0, sticky ='w')
        label2 = Label(frame1, text='What aspect does this offensive sentece say about "them"? Choose 1-3 labels')
        label2.grid(row=2, column=1, sticky ='w')

        frame2 = Frame(master)
        frame2.pack(fill=X)

        self.label_progress = Label(frame2, text=f'Progress: {len(labelled_data)} / {len(data)}')
        self.label_progress.grid(row=1, column=0, sticky ='w')

        self.class_labels = []
        self.class_boxes = []

        for i in range(len(categories)):
            label = IntVar()
            label_ = Checkbutton(frame2, text=categories[i], variable=label, onvalue=i+1, offvalue=0, command=label.get())
            label_.grid(row=i % 4 + 2, column=i // 4, sticky ='w')
            self.class_labels.append(label)
            self.class_boxes.append(label_)

        frame9 = Frame(master)
        frame9.pack()
        submit = Button(frame9, text='submit', command=self.submit)
        submit.grid(row=0, column=1)

        prev = Button(frame9, text='previous', command=self.previous)
        prev.grid(row=0, column=0)

        master.mainloop()

    def load(self):
        if labelled_data != []:
            messagebox.showwarning('Warning', 'Please save the current file first')
        else:
            data.clear()
            self.i = 0
            file = open(askopenfilename(title='Please choose a CSV file', 
                        initialdir='./', filetypes=[('CSV file','*.csv')]), 'r')
            csv_reader = csv.reader(file)
            for row in csv_reader:
                data.append(row)
            file.close()

            for row in data:
                if len(row) > 1:
                    if row[1] != "":
                        labelled_data.append(row)
                        self.i += 1
                    else: break
                else:
                    break

            self.text_sentence.insert("insert", data[self.i][0])
            self.label_progress.config(text=f'Progress: {self.i} / {len(data)}')

    def save(self):
        with open(asksaveasfilename(title='Please choose a CSV file', initialdir='/',
                  filetypes=[('CSV file','*.csv')]), 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(labelled_data + data[len(labelled_data):])
        messagebox.showinfo('Success', 'Save successfully!')

    def submit(self):
        annotations = [str(x.get()) for x in self.class_labels if x.get() != 0]

        if len(annotations) == 0 or len(annotations) > 3:
            messagebox.showinfo("showinfo", "Please choose 1-3 categories")
            return

        if self.i == len(labelled_data):
            labelled_data.append([data[self.i][0], ", ".join(annotations)])        
        else:
            labelled_data[self.i] = [data[self.i][0], ", ".join(annotations)]

        self.i += 1

        if self.i == len(data):
            messagebox.showinfo("showinfo", "Finished!")
            return

        self.text_sentence.delete(1.0, "end")
        self.text_sentence.insert("insert", data[self.i][0])
        self.label_progress.config(text=f'Progress: {self.i} / {len(data)}')
        
        for label in self.class_labels:
                label.set(0)

        if self.i < len(labelled_data):
            checked = [int(x) for x in labelled_data[self.i][1].split(", ") if labelled_data[self.i][1] != "" ]
            for i in checked:
                self.class_boxes[i-1].select()           

    def previous(self):
        if self.i > 0:
            self.i -= 1
            self.text_sentence.delete(1.0, "end")
            self.text_sentence.insert("insert", data[self.i][0])
            self.label_progress.config(text=f'Progress: {self.i} / {len(data)}')
            for label in self.class_labels:
                    label.set(0)
            
            checked = [int(x) for x in labelled_data[self.i][1].split(", ") if labelled_data[self.i][1] != "" ]
            for i in checked:
                self.class_boxes[i-1].select()
        else:
            messagebox.showinfo("showinfo", "This is the first one!")
        
    def red(self):
        self.group['bg'] = 'red'
    def blue(self):
        self.group['bg'] = 'blue'
    def yellow(self):
        self.group['bg'] = 'yellow'
    def nomal(self):
        self.group['bg'] = 'SystemButtonFace'

Tool()