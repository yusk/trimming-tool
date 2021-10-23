class Controller():

    INTERVAL = 50

    def __init__(self, app, model, view):
        self.master = app
        self.model = model
        self.view = view

        # マウスボタン管理用
        self.pressing = False
        self.selection = None

        # ラベル表示メッセージ管理用
        self.message = "ファイルを読み込んでください"

        self.set_events()

    def set_events(self):
        '受け付けるイベントを設定する'

        # キャンバス上のマウス押し下げ開始イベント受付
        self.view.left_canvas.bind("<ButtonPress>", self.button_press)

        # キャンバス上のマウス動作イベント受付
        self.view.left_canvas.bind(
            "<Motion>",
            self.mouse_motion,
        )

        # キャンバス上のマウス押し下げ終了イベント受付
        self.view.left_canvas.bind(
            "<ButtonRelease>",
            self.button_release,
        )

        # 読み込みボタン押し下げイベント受付
        self.view.load_button['command'] = self.push_load_button
        self.view.load_dir_btn['command'] = self.push_input_dir_btn

        # 画像の描画用のタイマーセット
        self.master.after(Controller.INTERVAL, self.timer)

    def timer(self):
        '一定間隔で画像等を描画'

        # 画像処理前の画像を左側のキャンバスに描画
        self.view.draw_image(self.view.LEFT_CANVAS)

        # 画像処理後の画像を右側のキャンバスに描画
        self.view.draw_image(self.view.RIGHT_CANVAS)

        # トリミング選択範囲を左側のキャンバスに描画
        self.view.draw_selection(self.selection, self.view.LEFT_CANVAS)

        # ラベルにメッセージを描画
        self.view.draw_message(self.message)

        # 再度タイマー設定
        self.master.after(Controller.INTERVAL, self.timer)

    def push_load_button(self):
        'ファイル選択ボタンが押された時の処理'

        # ファイル選択画面表示
        file_path = self.view.select_file()

        # 画像ファイルの読み込みと描画
        if len(file_path) != 0:
            self.model.read(file_path)

        self.selection = None

        # 選択範囲を表示するオブジェクトを削除
        self.view.delete_selection(self.view.LEFT_CANVAS)

        # メッセージを更新
        self.message = "トリミングする範囲を指定してください"

    def push_input_dir_btn(self):
        file_dir = self.view.select_dir()
        print(file_dir)

    def button_press(self, event):
        'マウスボタン押し下げ開始時の処理'

        # マウスクリック中に設定
        self.pressing = True

        self.selection = None

        # 現在のマウスでの選択範囲を設定
        self.selection = [event.x, event.y, event.x, event.y]

        # 選択範囲を表示するオブジェクトを削除
        self.view.delete_selection(self.view.LEFT_CANVAS)

    def mouse_motion(self, event):
        'マウスボタン移動時の処理'

        if self.pressing:

            # マウスでの選択範囲を更新
            self.selection[2] = event.x
            self.selection[3] = event.y

    def button_release(self, event):
        'マウスボタン押し下げ終了時の処理'

        if self.pressing:

            # マウスボタン押し下げ終了
            self.pressing = False

            # マウスでの選択範囲を更新
            self.selection[2] = event.x
            self.selection[3] = event.y

            # 画像の描画位置を取得
            objs = self.view.left_canvas.find_withtag("image")
            if len(objs) != 0:
                draw_coord = self.view.left_canvas.coords(objs[0])

                # 選択範囲をキャンバス上の座標から画像上の座標に変換
                x1 = self.selection[0] - draw_coord[0]
                y1 = self.selection[1] - draw_coord[1]
                x2 = self.selection[2] - draw_coord[0]
                y2 = self.selection[3] - draw_coord[1]

                # 画像をcropでトリミング
                self.model.crop((int(x1), int(y1), int(x2), int(y2)))

                # メッセージを更新
                self.message = "トリミングしました！"
