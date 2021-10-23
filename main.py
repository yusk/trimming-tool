import tkinter

from model import Model
from view import View
from controller import Controller

app = tkinter.Tk()

# アプリのウィンドウのサイズ設定
app.geometry("1000x430")
app.title("トリミングアプリ")

model = Model()
view = View(app, model)
controller = Controller(app, model, view)

app.mainloop()
