from PIL import Image, ImageTk

from constants import IMG_SIZE


class Model():
    # 画像処理前か画像処理後かを指定
    BEFORE = 1
    AFTER = 2

    MAX_SIZE = IMG_SIZE

    def __init__(self):

        # PIL画像オブジェクトを参照
        self.before_image = None
        self.after_image = None

        # Tkinter画像オブジェクトを参照
        self.before_image_tk = None
        self.after_image_tk = None

    def get_image(self, type):
        'Tkinter画像オブジェクトを取得する'

        if type == Model.BEFORE:
            if self.before_image is not None:
                # Tkinter画像オブジェクトに変換
                self.before_image_tk = ImageTk.PhotoImage(self.before_image)
            return self.before_image_tk
        elif type == Model.AFTER:
            if self.after_image is not None:
                # Tkinter画像オブジェクトに変換
                self.after_image_tk = ImageTk.PhotoImage(self.after_image)
            return self.after_image_tk

        else:
            return None

    def read(self, path):
        '画像の読み込みを行う'

        # pathの画像を読み込んでPIL画像オブジェクト生成
        self.before_image = Image.open(path)
        self.resize()

    def resize(self):
        size = self.before_image.size
        r = self.MAX_SIZE / max(size)
        self.before_image = self.before_image.resize(
            (int(size[0] * r), int(size[1] * r)))

    def round(self, value, min, max):
        'valueをminからmaxの範囲に丸める'

        ret = value
        if (value < min):
            ret = min
        if (value > max):
            ret = max

        return ret

    def crop(self, param):
        '画像をクロップ'

        if len(param) != 4:
            return
        if self.before_image is None:
            return

        print(param)
        # 画像上の選択範囲を取得（x1,y1）-（x2,y2）
        x1, y1, x2, y2 = param

        # 画像外の選択範囲を画像内に切り詰める
        x1 = self.round(x1, 0, self.before_image.width)
        x2 = self.round(x2, 0, self.before_image.width)
        y1 = self.round(y1, 0, self.before_image.height)
        y2 = self.round(y2, 0, self.before_image.height)

        # x1 <= x2 になるように座標を調節
        if x1 <= x2:
            crop_x1 = x1
            crop_x2 = x2
        else:
            crop_x1 = x2
            crop_x2 = x1

        # y1 <= y2 になるように座標を調節
        if y1 <= y2:
            crop_y1 = y1
            crop_y2 = y2
        else:
            crop_y1 = y2
            crop_y2 = y1

        # PIL Imageのcropを実行
        self.after_image = self.before_image.crop(
            (crop_x1, crop_y1, crop_x2, crop_y2))
