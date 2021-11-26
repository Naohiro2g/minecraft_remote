# Naohiro2g/minecraft_remote

|[1.12 World of Color Update](https://www.youtube.com/watch?v=k2dQuIIUT-o)|[1.13 Update Aquatic](https://www.youtbe.com/watch?v=hcutClmY1pI)|[1.16 Nether update](https://www.youtube.com/watch?v=1DhWXAiNgfQ)|
|--|--|--|
|[<img src="./images/1.12_world_of_color_update.jpg" width="240">](./images/1.12_world_of_color_update.jpg)|[<img src="./images/1.13_update_aquatic.jpg" width="240">](./images/1.13_update_aquatic.jpg)|[<img src="./images/1.16_nether_update.png" width="240">](./images/1.16_nether_update.png)|


色の世界（World of Color）で4年間、立ち止まっていました。いよいよ、ようやく、マインクラフトJava版 ver.1.16.5をScratchやPythonでコントロールできます。

## PythonやScratchでマイクラをリモコンする
[**(English here.)**](./README.md)

マインクラフトAPIを使ってScratchやPythonでコーディングして、ブロックを置いたり、スティーブをあちこち動かしたりなどできます。

ご存知のように、マイクラ世界でそういうことを手動でやるのは、もちろん面白いことなんですが、コーディングしてリモコンするのも楽しいです。そして、ScrathやPythonを学ぶことに興味を持つための素晴らしい教材になります。

私のクラスでは、gitやGitHub.comの使い方までが含まれていますが、若い学習者から経験者まで楽しめる自習教材となっています。**まずやりたいことが先にある、というのは、プログラミング言語を学ぶ上でとても良いやり方なのです。**

このことは、外国語を学ぶ上でも同じく正しいと考えています。**言語を学ぶな、言語を使え。**　（格言ぽいのを、今、作りました。;)）


## 版／バージョンと環境
マイクラの版とバージョンの組み合わせによって、3種類の環境があります。Pythonモジュールについて、Java版1.12.2はラズパイ版と同じく従来のmcpiが使えますが、Java版1.16.5は新しいmcjeを使います。ラズパイ版はmodが不要で、Java版の2種類それぞれにマイクラと同じバージョンのmodと、modを収容するForgeが必要になります。

|Minecraft|Forge|mod|Python module|Scratch + Extension|
|---|---|---|---|---|
|Pi Edition (MCPI) Raspbery Pi|-|-|[mcpi](https://github.com/martinohanlon/mcpi)|Scratch 1.4 + [Scratch2MCPI](https://github.com/scratch2mcpi/scratch2mcpi)|
|Java Edition (MCJE) 1.12.2|[Forge 1.12.2](https://files.minecraftforge.net/net/minecraftforge/forge/index_1.12.2.html)|[RemoteControllerMod-1.12.2 v0.02](https://www.curseforge.com/minecraft/mc-mods/remote-controller/files/3242375)|[mcpi](https://github.com/martinohanlon/mcpi)|[Scratch 3 + MC Ext 1.12.2](https://takecx.github.io/scratch-gui/1-12-2/)|
|Java Edition (MCJE) 1.16.5|[Forge 1.16.5](https://files.minecraftforge.net/net/minecraftforge/forge/index_1.16.5.html)|[RemoteControllerMod-1.16.5 v0.05](https://www.curseforge.com/minecraft/mc-mods/remote-controller/files/3363255)|[mcje](./mcje)|[Scratch 3 + MC Ext 1.16.5](https://takecx.github.io/scratch-gui/1-16-5/)|

**OptiFineというmodは、Java版マイクラの見た目を簡素にして軽量化する事ができます。マイクラ、Forgeと同じバージョンを選ぶ必要があります。https://optifine.net/downloads**

**Forgeを実行するために、Java SE 8 JREが必要になるかもしれません。 https://www.java.com/download/ie_manual.jsp**

Java版マイクラをラズパイを含むLinux、Mac、PCで動かすことができます。ラズパイでのJava版マイクラに関しては後述。

Java版マイクラのバージョン1.13「Update Aquatic、水のアップデート」での変化は、とても大きいものだったため、マイクラをリモコンする我々は1.12.2で3年もの間足止めを余儀なくされたのです。 [takecx](https://github.com/takecx)さんの甚大なる努力によりそれを打ち破り、1.16.5での動作を可能にすることができました。

しかし、またまた、バージョン1.17での変化も大きいものでした。マイクラ - Forge 1.17での互換性の問題で、「しばらく、お待ち下さい」に。というか、待ち時間を少なくするためにGitHub.comでの[RemoteControllerMod](https://github.com/takecx/RemoteControllerMod) 開発を手伝ってください。

（黒馬くんは我々を助けようとしている。。のか？）
[<img src="./images/minecraft_remote_digitalclock.png" width="400">](./images/minecraft_remote_digitalclock.png)

#### ラズパイでのJava版マイクラ
現在、ちょっと残念な状況。Mojangアカウントを持っていない（新規あるいは、マイクロソフトアカウントに移行してしまった）ユーザーが、Java版マイクラを動かすことが非常に困難な状況です。方法はあるがとても面倒。面倒な割に新しいバージョンほど動作がめちゃくちゃ重い。1.12.2は、まだまし。1.16.5はかなり重い。（Mojangアカウントからマイクロソフトアカウントへの移行が進行中。マイクロソフトはARMプラットフォームをサポートしていない。という事情で、ランチャーからのMojangアカウントでのサインインができなくなった。）

## マイクラ世界にブロック（ヴォクセル、ボリュームピクセル）で何かを描くサンプルコード

すみません、今の所、Python版しか置いてません。Scratchで始める方法に関しては、 [takecyさんのリポジトリ](https://github.com/takecx/RemoteControllerMod) を見てください。

 - [hello_MCPI.py](./hello_MCPI.py), [hello_MCJE.py](./hello_MCJE.py), [hello_MCJE1122.py](./hello_MCJE1122.py) :　典型的なハローワールド。**これを一番に試してください。自分の環境に合わせてPythonモジュールのmcpiかmcjeを選ぶ方法がわかります。**
mcpiモジュールをPypiからインストールするには、
``` sudo pip3 install mcpi ```(Mac, Linux) あるいは ``` pip install mcpi ```(Windows) で。

 - [digitalclock.py](./digitalclock.py)：手作りのLCDフォントをダブルバッファで使い、「クラス」を学ぶことができます。時刻表示にシーランタンを使うのが好みですが、残念ながらMCPI（ラズパイ版）にはシーランタンがありません。

   - 日付と時刻を５ｘ７のLCDフォントで、以下のフォーマットにてリアルタイム表示するデジタル時計。（上の画像のやつ。）

```
        2021-06-26
         21:28:45
```

 - [axis_flat.py](./axis_flat.py)  :　ｘ，ｙ，ｚ軸を描き、おまけに世界を平らにするモジュールです。仮想原点をMCJEでは(0, 80, 0)、MCPIでは (0, 20, 0)にセットした軸を以下のような素材で描きます。
    - x軸: 石ブロック
    - y軸: 草土ブロック
    - z軸: 金ブロック
 - demo1.py, demo2.py :　axis_flat（軸とフラット化）と double_buffer_display（ダブルバッファ表示）モジュールの使い方デモ。

 - **（新作）** [maze.py](./maze.py) :　マイクラ世界に迷路を建築します。サプーさんというPython VTuberの作品。彼女の解説動画はこちら。
**[【Pythonでマイクラ操作！】自動で迷路を作成してマインクラフト上で遊んでみよう 〜 Minecraftプログラミング入門 〜](https://www.youtube.com/watch?v=iK3V8q2EiI8)**
   - mazelibというPythonモジュールを使っています。C++コードを含んでおり、Pypiにバイナリがないためインストール時にビルドが必要。
   - Mac, Linux：
       - ```sudo pip3 install mazelib ```などでインストール／ビルドできるはず。
   - Windows 10／11：
      - C++ビルドツールがインストールされていれば、```pip install mazelib```でオッケー。詳しくは後述。

[<img src="./images/maze_letters.png" width="220">](./images/maze_letters.png) [<img src="./images/maze_blocks.png" width="220">](./images/maze_blocks.png)

(文字による迷路、マイクラ世界のブロックによる迷路）


**8歳の子どもがx軸y軸を学ぶのは難しすぎる、あるいは早すぎる、と思うかもしれませんが、そんなことはありません。彼らに「教えよう」としているのなら、確かにそうでしょう。子どもたちが学ぶのを助けるだけにしてみてください。あー、実際のところ、私は彼らと一緒に遊んでいるだけです。**


### Widows C++ビルドツールのインストール (mazelib用)
https://visualstudio.microsoft.com/ja/downloads/
ここで「Visual Studio 2022用のツール」を開き、Build Tools for Visual Studio 2022をゲット。スタンドアロンで動くので**Visual Studio自体は不要**。pipからの利用ならVisual Studio Build Toolsアプリを開くこともない。

実態はVisual Studio Installerで、これを起動。
「変更」 →「個別のコンポーネント」でWindowsのバージョンに合わせて、以下の２つを探し出してインストール。
 1.  Windows 10 SDK あるいは Windows 11 SDK
 1.  MSVC v143 VS2022 C++ x64/x86ビルドツール（最新）

(1)はwindowsで検索。(2)はmsvcで検索。

## デジタルクロックで使われているファイルたち

#### [digitalclock.py](./digitalclock.py)
 - ```python digitalclock.py```　で走る、メインファイル。Python 3.7.9を想定していますが、環境によってはpythoあるいはpython3で起動されます。
 - ふたつの表示インスタンスをそれぞれ日付、時刻に使います。
 - Pythonモジュールをmcpiかmcjeからひとつ選ぶ必要があります。
#### [double_buffer_display.py](./double_buffer_display.py)
 - BufferDisplayクラス
 - 前回からの変化分だけを描くための、ふたつの切り替えバッファを持つ、表示クラス
 - Pythonモジュールをmcpiかmcjeからひとつ選ぶ必要があります。
#### [font_5x7.py](./font_5x7.py)
 - 5 x 7 LCDフォントのデザイン
#### [param_MCJE.py](./param_MCJE.py), [param_MCJE1122.py](./param_MCJE1122.py), [param_MCPI.py](./param_MCPI.py)
 - ブロックタイプ、世界の大きさ、xyz軸のパラメーターなどの定数値
 - param_MCJE: Java版マイクラ1.16.5用
 - param_MCJE1122: Java版マイクラ1.12.2用
 - param_MCPI: ラズパイのマイクラ用
#### [mcje (minecraft java edition)](./mcje)
 - https://github.com/lasteamlab/mcpi2 からフォークした、Pythonモジュール
 - Named as mcjeと名付け、Java版マイクラ1.13以降向けに改造
 - そのうち、Pypiにアップロードします。

## PythonやJavaなど開発環境

(そのうち書きます。。)
 - Python 3.7.9 　2021年中は、3.7.9で。2022年になったら3.9への移行を準備しましょう。最新は3.10ですが、まだ早い。
 - Java SE 8 JRE　　Minecraft 1.17から　Java 16ベースに移行。さらにJava 17へ行くらしい。この影響でmodのビルド環境に変化があり、対応できていない。
