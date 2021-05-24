# -*- coding: utf-8 -*-
import tkinter as tk
import  tkinter.font   as  tkFont
import json

root=tk.Tk()
root.title("对话筛选")

config = json.load(open("./config.json"))
source = config["source"]
target = config["target"]

class App(tk.Frame):
    def set_num_label(self):
        try:
            self.numbers_label.destroy()
        except Exception:
            None
        self.numbers_label = tk.Label(self.numbers, text="数据集中的位置：" + str(self.corpus_pointer) + "已标注数量：" + str(len(self.utterances)), fg='black',height=3,width=100, font=self.font)
        self.numbers_label.pack()
        self.numbers.update()


    def extract_utterance(self):
        utterance = []
        for a in self.acceptive_queue[:self.pointer_position]:
            utterance.append(a["sentence"])
        self.corpus_pointer += 1
        if len(utterance) > 1:
            self.utterances.append(utterance)
            if(self.pointer_position < len(self.acceptive_queue)):
                self.utterances_del_counter += 1
                self.corpus_pointer -= 1
                self.jump_stack.append(self.jump_counter)
            else:
                self.utterances_del_num.append(self.utterances_del_counter)
                if(self.utterances_del_counter == 0):
                    self.jump_stack.append(self.jump_counter)
                self.utterances_del_counter = 0
            self.jump_counter = 0

        else:
            self.corpus_pointer -= 1

        self.destroy_all_utteraces()
        self.get_utterance()
        self.set_num_label()

    def de_acceptive_queue(self):
        if self.pointer_position > 0 :
            self.acceptive_queue[self.pointer_position - 1]["Frame"].forget()
            self.pointer_position -= 1
        self.delta = 1

    def en_acceptive_queue(self):
        if self.pointer_position < self.converLength:
            self.acceptive_queue[self.pointer_position]["Frame"].pack()
            self.pointer_position += 1

    def destroy_all_utteraces(self):
        for a in self.acceptive_queue:
            a["Frame"].destroy()
        self.acceptive_queue = []
        self.pointer_position = 0

    def get_utterance(self):
        if(self.corpus_pointer >= len(self.corpus)):
            f = tk.Frame(root, borderwidth=2,bg='#FFFFFF',height=30,width=20)
            tk.Label(f, text="你整完了所有的数据集!", fg='red',height=3,width=100, font=self.font).pack()
            f.pack()
            return
        utterance = self.corpus[self.corpus_pointer]
        self.converLength = len(utterance)
        for i in range(self.converLength):
            a = tk.E if (self.converLength - i)%2 == 0 else tk.W
            f = tk.Frame(root, borderwidth=2,bg='#FFFFFF',height=30,width=20)
            tk.Label(f, text=utterance[i].replace(" ",""), fg='black',anchor=a,height=3,width=75, font=self.font).pack()
            f.pack()
            self.acceptive_queue.append({"Frame":f,"sentence":utterance[i]})
        self.pointer_position = len(self.acceptive_queue)

    
    def roll_back(self):
        if(self.corpus_pointer > self.corpus_bound):
            if self.utterances_del_counter == 0:
                roll_utterances = self.utterances_del_num.pop()
            else:
                roll_utterances = self.utterances_del_counter
            if(self.jump_counter == 0 and len(self.jump_stack) > 1):
                if self.utterances_del_counter == 0:
                    self.utterances.pop()
                else:
                    self.utterances_del_counter = 0
                for _ in range(roll_utterances):
                    self.utterances.pop()
                self.jump_counter = self.jump_stack.pop()
            else:
                self.jump_counter -= 1
            self.destroy_all_utteraces()
            if(self.corpus_pointer > 0):
                self.corpus_pointer -= 1
            self.get_utterance()
        self.set_num_label()

    
    def throw_away(self):
        self.utterances_del_num.append(self.utterances_del_counter)
        if(self.utterances_del_counter == 0):
            self.jump_counter += 1
        else:
            self.utterances_del_num[-1] -= 1
        self.utterances_del_counter = 0
        self.corpus_pointer += 1
        self.destroy_all_utteraces()
        self.get_utterance()
        self.set_num_label()
    
    def save_all(self):
        self.save_file.seek(0)
        self.save_file.truncate()
        self.save_file.write(json.dumps(self.utterances, ensure_ascii=False))
        self.save_file.flush()
        
    def begin(self):
        self.numbers = tk.Frame(root,height=30,width=20)
        self.set_num_label()
        self.numbers.pack()
        self.extract_utterance()
        self.save = tk.Button(self, text="保存这条对话", fg="green",command=self.extract_utterance)
        self.save.pack(side="right")
        self.throw = tk.Button(self, text="丢弃这条对话", fg="green",command=self.throw_away)
        self.throw.pack(side="right")
        self.roll = tk.Button(self, text="滚回上条对话", fg="green", command=self.roll_back)
        self.roll.pack(side="right")
        self.dlo = tk.Button(self, text="删掉最后一句", fg="green", command=self.de_acceptive_queue)
        self.dlo.pack(side="right")
        self.rlo = tk.Button(self, text="恢复最后一句", fg="green", command=self.en_acceptive_queue)
        self.rlo.pack(side="right")
        self.sa = tk.Button(self, text="全部保存在文件中", fg="green", command=self.save_all)
        self.sa.pack(side="right")
        self.quit = tk.Button(self, text="退出", fg="red", command=self.master.destroy)
        self.quit.pack(side="bottom")
        
        

    def say_hi(self):
        print("hi there, everyone!")
    
    def get_initial_number(self, event):
        try:
            self.corpus_pointer = int(self.contents.get())
            self.entrythingy.destroy()
            self.corpus_bound = self.corpus_pointer
            self.begin()

        except Exception:
            None

        
    def __init__(self, master, file_path, save_path):
        super().__init__(master)
        self.master = master
        self.pack()
        self.jump_stack = []
        self.jump_counter = 0
        self.utterances_del_num = []
        self.utterances_del_counter = 0
        with open(file_path, encoding="utf-8", mode="r") as f:
            self.corpus = json.load(f)
        helv36 = tkFont.Font ( family="Helvetica",size=36, weight="bold",slant= "italic"  ,underline=1)
        w = tk.Label(root, text="对话筛选", font=helv36) 
        w.pack()
        self.font = tkFont.Font ( family="Helvetica",size=10)
        intro = "说明：筛选过程中，最后的一句话是期望聊天机器人说出的。\n每次使用都会在result.json上累加, result.json会自动生成。\n数据总量：" + str(len(self.corpus))
        introf = tk.Frame(root,height=30,width=20)
        tk.Label(introf, text=intro, fg='black',height=3,width=100, font=self.font).pack()
        introf.pack()
        fb = tkFont.Font(font=w["font"]).copy()
        fb.config(weight="bold")
        fb.config(size=20)
        w.config(font=fb)
        self.acceptive_queue = []
        self.pointer_position = 0
        self.converLength = 0
        self.corpus_bound = 0
        self.delta = 0

        self.corpus_pointer = 0
        self.utterances = None
        try:
            with open(save_path, encoding="utf-8", mode="r") as f:
                self.utterances = json.load(f)
        except Exception:
            None

        if not self.utterances:
            self.utterances = []
        self.save_file = open(save_path, encoding="utf-8", mode="w")
        self.save_all()


        self.entrythingy = tk.Entry(width=100)
        self.entrythingy.pack()

        self.contents = tk.StringVar()
        self.contents.set("请输入对话开始号码,需要小于数据总量，并按下回车键")
        self.entrythingy["textvariable"] = self.contents

        self.entrythingy.bind('<Key-Return>',
                             self.get_initial_number)

    

myapp = App(root, source, target)

myapp.mainloop()
