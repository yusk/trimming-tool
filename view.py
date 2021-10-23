import tkinter
import tkinter.filedialog


class View():
    # キャンバス指定用
    LEFT_CANVAS = 1
    RIGHT_CANVAS = 2

    def __init__(self, app, model):
        self.master = app
        self.model = model

        # アプリ内のウィジェットを作成
        self.create_widgets()

    def create_widgets(self):
        'アプリ内にウィジェットを作成・配置する'

        # キャンバスのサイズ
        canvas_width = 400
        canvas_height = 400

        # キャンバスとボタンを配置するフレームの作成と配置
        self.main_frame = tkinter.Frame(self.master)
        self.main_frame.pack()

        # ラベルを配置するフレームの作成と配置
        self.sub_frame = tkinter.Frame(self.master)
        self.sub_frame.pack()

        # キャンバスを配置するフレームの作成と配置
        self.canvas_frame = tkinter.Frame(self.main_frame)
        self.canvas_frame.grid(column=1, row=1)

        # ボタンを８位するフレームの作成と配置
        self.button_frame = tkinter.Frame(self.main_frame)
        self.button_frame.grid(column=2, row=1)

        # １つ目のキャンバスの作成と配置
        self.left_canvas = tkinter.Canvas(
            self.canvas_frame,
            width=canvas_width,
            height=canvas_height,
            bg="gray",
        )
        self.left_canvas.grid(column=1, row=1)

        # ２つ目のキャンバスの作成と配置
        self.right_canvas = tkinter.Canvas(
            self.canvas_frame,
            width=canvas_width,
            height=canvas_height,
            bg="gray",
        )
        self.right_canvas.grid(column=2, row=1)

        # btns
        self.input_dir_btn = tkinter.Button(self.button_frame,
                                            text="input dir")
        self.input_dir_btn.pack()
        self.output_dir_btn = tkinter.Button(self.button_frame,
                                             text="output dir")
        self.output_dir_btn.pack()
        self.left_btn = tkinter.Button(self.button_frame, text="←")
        self.left_btn.pack()
        self.right_btn = tkinter.Button(self.button_frame, text="→")
        self.right_btn.pack()
        self.save_btn = tkinter.Button(self.button_frame, text="save")
        self.save_btn.pack()

        # メッセージ表示ラベルの作成と配置

        # メッセージ更新用
        self.message = tkinter.StringVar()

        self.message_label = tkinter.Label(self.sub_frame,
                                           textvariable=self.message)
        self.message_label.pack()

    def draw_image(self, type):
        '画像をキャンバスに描画'

        # typeに応じて描画先キャンバスを決定
        if type == View.LEFT_CANVAS:
            canvas = self.left_canvas
            image = self.model.get_image(self.model.BEFORE)
        elif type == View.RIGHT_CANVAS:
            canvas = self.right_canvas
            image = self.model.get_image(self.model.AFTER)
        else:
            return

        if image is not None:
            # キャンバス上の画像の左上座標を決定
            sx = (canvas.winfo_width() - image.width()) // 2
            sy = (canvas.winfo_height() - image.height()) // 2

            # キャンバスに描画済みの画像を削除
            objs = canvas.find_withtag("image")
            for obj in objs:
                canvas.delete(obj)

            # 画像をキャンバスの真ん中に描画
            canvas.create_image(sx,
                                sy,
                                image=image,
                                anchor=tkinter.NW,
                                tag="image")

    def draw_selection(self, selection, type):
        '選択範囲を描画'

        # typeに応じて描画先キャンバスを決定
        if type == View.LEFT_CANVAS:
            canvas = self.left_canvas
        elif type == View.RIGHT_CANVAS:
            canvas = self.right_canvas
        else:
            return

        # 一旦描画済みの選択範囲を削除
        self.delete_selection(type)

        if selection:
            # 選択範囲を長方形で描画
            canvas.create_rectangle(selection[0],
                                    selection[1],
                                    selection[2],
                                    selection[3],
                                    outline="red",
                                    width=3,
                                    tag="selection_rectangle")

    def delete_selection(self, type):
        '選択範囲表示用オブジェクトを削除する'

        # typeに応じて描画先キャンバスを決定
        if type == View.LEFT_CANVAS:
            canvas = self.left_canvas
        elif type == View.RIGHT_CANVAS:
            canvas = self.right_canvas
        else:
            return

        # キャンバスに描画済みの選択範囲を削除
        objs = canvas.find_withtag("selection_rectangle")
        for obj in objs:
            canvas.delete(obj)

    def draw_message(self, message):
        self.message.set(message)

    def select_file(self):
        'ファイル選択画面を表示'

        # ファイル選択ダイアログを表示
        file_path = tkinter.filedialog.askopenfilename(initialdir=".")
        return file_path

    def select_dir(self):
        file_dir = tkinter.filedialog.askdirectory()
        return file_dir
