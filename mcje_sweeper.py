# -*- coding:utf-8 -*-
import tkinter
from tkinter import messagebox
import random
from convert_mcje import MCJESweeper
from mcje.minecraft import Minecraft
import param_MCJE as param


# 各種設定
BOARD_WIDTH = 20
BOARD_HEIGHT = 10
MINE_NUM = 20

MINE_BG_COLOR = "pink"
FLAG_BG_COLOR = "gold"
EMPTY_BG_COLOR = "lightgray"

fg_color = {
    1: "blue",
    2: "green",
    3: "purple",
    4: "olive",
    5: "chocolate",
    6: "magenta",
    7: "darkorange",
    8: "red",
}

# 定数定義
MINE = -1

#mcje側の操作
mc = Minecraft.create(port=param.PORT_MC)
mjs = MCJESweeper(mc)
mjs.setMass(BOARD_WIDTH,BOARD_HEIGHT)
        
class MineSweeper():
    def __init__(self, app):

        # *** 各種メンバの初期化 *** #

        self.app = app
        self.cells = None 
        self.labels = None
        self.width = BOARD_WIDTH
        self.height = BOARD_HEIGHT
        self.mine_num = MINE_NUM
        self.clear_num = self.width * self.height - self.mine_num
        self.open_num = 0
        self.open_mine = False
        self.play_game = False

        # 地雷を管理するボード
        self.cells = None

        # 画面に表示するラベルウィジェットの管理リスト
        self.labels = None

        # *** 爆弾を管理するボード作成 *** #

        # ボードを初期化
        self.init_cells()

        # ボードに地雷を配置
        self.place_mines()

        # 各マスに周りの地雷の数を設定
        self.set_mine_num()

        # *** ウィジェットの表示とイベント設定 *** #

        # ウィジェットの作成と配置
        self.create_widgets()

        # イベントの設定
        self.set_events()

        # 最後にゲーム中フラグをTrueに設定
        self.play_game = True
        

    # ボードの初期化
    def init_cells(self):

        # ボードのサイズ分の２次元リストを作成
        self.cells = [[0] * self.width for _ in range(self.height)]

    # 地雷を配置
    def place_mines(self):

        mine_num = 0
        while mine_num < self.mine_num:

            # 地雷の位置をランダムに決定
            j = random.randint(0, self.height - 1)
            i = random.randint(0, self.width - 1)

            if self.cells[j][i] != MINE:

                # その位置に地雷があることを示すMINE(-1)を格納
                self.cells[j][i] = MINE
                mine_num += 1

    # 各マスに周りの地雷の数を設定
    def set_mine_num(self):
        for j in range(self.height):
            for i in range(self.width):

                # そのマスが地雷の場合は何もしない
                if self.cells[j][i] == MINE:
                    continue

                # 隣接する８方向のマスの地雷の数をカウント
                num_mine = 0

                # 方向を決める２重ループ
                for y in range(-1, 2):
                    for x in range(-1, 2):
                        if y != 0 or x != 0:
                            # その方向に地雷があるかチェック
                            is_mine = self.is_mine(i + x, j + y)

                            if is_mine:
                                # 地雷があればカウントアップ
                                num_mine += 1

                # 周りの地雷の数をセット
                self.cells[j][i] = num_mine

    # そのマスに地雷があるかどうかを判断する関数
    def is_mine(self, i, j):

        # ボード内の座標かチェック
        if j >= 0 and i >= 0 and j < self.height and i < self.width:

            # その座標に地雷があるかどうかをチェック
            if self.cells[j][i] == MINE:

                # そのマスが地雷の場合はTrueを返却
                return True

        # ボード外 or 地雷でない場合はFalseを返却
        return False

    # ウィジェットを作成
    def create_widgets(self):
        # ラベルウィジェット管理用のリストを作成
        self.labels = [[None] * self.width for j in range(self.height)]

        for j in range(self.height):
            for i in range(self.width):

                # まずはテキストなしでラベルを作成
                label = tkinter.Label(
                    self.app,
                    width=2,
                    height=1,
                    bg=EMPTY_BG_COLOR,
                    relief=tkinter.RAISED
                )
                # ラベルを配置
                label.grid(column=i, row=j)

                # その座標のラベルのインスタンスを覚えておく
                self.labels[j][i] = label

    # イベントを設定
    def set_events(self):

        # 全ラベルに対してイベントを設定
        for j in range(self.height):
            for i in range(self.width):

                label = self.labels[j][i]

                # 左クリック時のイベント設定
                label.bind("<ButtonPress-1>", self.open_cell)

                # 右クリック時のイベント設定
                # 右クリックが反応しない場合は第１引数を"<ButtonPress-3>"に変更してみてください
                label.bind("<ButtonPress-2>", self.raise_flag)

    # 右クリック時に実行する関数
    def raise_flag(self, event):

        # ゲーム中でなければ何もしない
        if not self.play_game:
            return

        # クリックされたラベルを取得
        label = event.widget

        # 既にそのマスを開いている場合は何もしない
        if label.cget("relief") != tkinter.RAISED:
            return

        # 既に旗が設定されている場合
        if label.cget("text") != "F":

            # ラベルの色を設定
            bg = FLAG_BG_COLOR

            # そのラベル上に旗(F)を立てる
            label.config(
                text="F",
                bg=bg
            )
        else:
            # ラベルの色を設定
            bg = EMPTY_BG_COLOR

            # そのラベル上の旗(F)を取り除く
            label.config(
                text="",
                bg=bg
            )

    # 左クリック時に実行する関数
    def open_cell(self, event):

        # ゲーム中でなければ何もしない
        if not self.play_game:
            return

        # クリックされたラベルを取得
        label = event.widget

        # ラベルの座標を取得
        for y in range(self.height):
            for x in range(self.width):
                if self.labels[y][x] == label:
                    j = y
                    i = x

        cell = self.cells[j][i]
        print(cell,j,i)
        # 既にそのマスを開いている場合は何もしない
        if label.cget("relief") != tkinter.RAISED:
            return

        # マスの状態に応じて表示するテキストと色を設定
        text, bg, fg = self.get_text_info(cell)

        # そこに地雷がある場合
        if cell == MINE:

            # ゲームオーバーフラグをTrueに設定
            self.open_mine = True

        # ラベルの設定変更
        label.config(
            text=text,
            bg=bg,
            fg=fg,
            relief=tkinter.SUNKEN
        )

        # 開いたマス数をカウントアップ
        self.open_num += 1

        # 周辺の座標も開けるかどうかを調べていく
        if cell == 0:
            self.open_neighbor(i - 1, j - 1)
            self.open_neighbor(i, j - 1)
            self.open_neighbor(i + 1, j - 1)
            self.open_neighbor(i - 1, j)
            self.open_neighbor(i + 1, j)
            self.open_neighbor(i - 1, j + 1)
            self.open_neighbor(i, j + 1)
            self.open_neighbor(i + 1, j + 1)
            

        # ゲームオーバーならゲームオーバー処理
        if self.open_mine:
            self.app.after_idle(self.game_over)

        # ゲームクリアならゲームクリア処理
        elif self.open_num == self.clear_num:
            self.app.after_idle(self.game_clear)

    # クリックされたマスをの周辺を開く処理
    def open_neighbor(self, i, j):

        # 地雷を開けてしまっていたら何もしない
        if self.open_mine:
            return

        # ボード外の座標であれば何もしない
        if not (j >= 0 and i >= 0 and j < self.height and i < self.width):
            return

        # その座標のラベルを取得
        label = self.labels[j][i]

        # 既にそのマスを開いている場合は何もしない
        if label.cget("relief") != tkinter.RAISED:
            return

        # そのマスが地雷であれば何もしない
        if self.cells[j][i] == MINE:
            return

        # ↑ の条件に当てはまらないのであればそのマスは開ける

        # ラベルの座標に応じて表示するテキストと色を設定
        text, bg, fg = self.get_text_info(self.cells[j][i])

        # ラベルの設定変更
        label.config(
            text=text,
            bg=bg,
            fg=fg,
            relief=tkinter.SUNKEN
        )

        # 開いたマス数をカウントアップ
        self.open_num += 1

        # 周辺の座標も開けるかどうかを調べていく
        if self.cells[j][i] == 0:
            self.open_neighbor(i - 1, j - 1)
            self.open_neighbor(i, j - 1)
            self.open_neighbor(i + 1, j - 1)
            self.open_neighbor(i - 1, j)
            self.open_neighbor(i + 1, j)
            self.open_neighbor(i - 1, j + 1)
            self.open_neighbor(i, j + 1)
            self.open_neighbor(i + 1, j + 1)

    # ゲームオーバー時の処理
    def game_over(self):

        # 全マスを開く
        self.open_all()

        # ゲーム中フラグをFalseに設定
        self.play_game = False

        # メッセージを表示
        messagebox.showerror(
            "ゲームオーバー",
            "地雷を開いてしまいました..."
        )

    # ゲームクリア時の処理
    def game_clear(self):

        # 全マスを開く
        self.open_all()

        # ゲーム中フラグをFalseに設定
        self.play_game = False

        # メッセージを表示
        messagebox.showinfo(
            "ゲームクリア",
            "おめでとうございます！ゲームクリア！"
        )

    # マスを全て開く
    def open_all(self):

        # 全マスに対するループ
        for j in range(self.height):
            for i in range(self.width):
                label = self.labels[j][i]

                # ラベルの座標に応じて表示するテキストと色を設定
                text, bg, fg = self.get_text_info(self.cells[j][i])

                # ラベルの設定変更
                label.config(
                    text=text,
                    bg=bg,
                    fg=fg,
                    relief=tkinter.SUNKEN
                )

    # テキストと文字と背景色を取得する関数
    def get_text_info(self, num):

        # 指定された数字を表示する色を決定
        if num == MINE:
            text = "X"
            bg = MINE_BG_COLOR
            fg = "darkred"
        elif num == 0:
            text = ""
            bg = EMPTY_BG_COLOR
            fg = "black"
        else:
            text = str(num)
            bg = EMPTY_BG_COLOR
            fg = fg_color[num]

        return (text, bg, fg)


# プログラムの開始
app = tkinter.Tk()
game = MineSweeper(app)

app.mainloop()