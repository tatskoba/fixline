#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os.path
import codecs
import re
 
# 引数を取得する
def getargs():

    import argparse

    parser = argparse.ArgumentParser(
            prog="fixline", # プログラム名
            usage="python fixline input_file [-e encoding] [-o output_file]", #プログラムの利用方法
            description="description", #「optional arguments」の前に表示される説明文
            epilog = "end", #「optional arguments」後に表示される文字列
            add_help = True #[-h],[--help]オプションをデフォルトで追加するか
            )

    # 引数の追加
    parser.add_argument('input_file') # 入力ファイル
    parser.add_argument("-e", "--encoding", #オプション引数
                        help="Encoding of input file. Default is utf-8.", #引数の説明
                        required = False, #引数の省略を不可にするか
                        type = str)
    parser.add_argument("-o", "--output_file", #オプション引数
                        help="Path of output file.", #引数の説明
                        required = False, #引数の省略を不可にするか
                        type = str)
    parser.add_argument('--version', action='version', version='%(prog)s 0.01') # version

    # 引数の解析
    args = parser.parse_args() 

    # エンコーディング指定がない時の対処
    if not args.encoding:
        args.encoding = u'utf-8'
    if not args.output_file:
        args.output_file = u''

    return [args.input_file, args.encoding, args.output_file]


# 文単位を取得する
def getline(buf):

    # ---- 行の特徴配列を初期化 -------
    f1 = []
    f2 = []
    f3 = []
    f4 = []
    f5 = []
    f6 = []

    # ---- 加工した行の配列を初期化 -------
    mod_line = []

    # ---- 行の特徴取得 -------
    for line in buf:

        # 文頭と文末の空白と改行コードを除去して作業用変数textにコピー
        text = line
        for i in range(0, len(line)):  # 前方から探索
            if (not line[i] == u' ') and (not line[i] == u'　'):
                text = line[i:-1]
                break 
        for i in range(len(text)-1, 0, -1):  # 後方から探索
            if (not text[i] == u' ') and (not text[i] == u'　'):
                text = text[:i+1]
                break 
        mod_line.append(text)   # textを配列にも保持しておく

        # (1) 空行
        if len(text) == 0:
            #print(u'空行: ' + text)
            f1.append(1)
            f2.append(0)
            f3.append(0)
            f4.append(0)
            f5.append(0)
            f6.append(0)
            continue
        else:
            f1.append(0)

        # (2) 見出し行の特徴
        if text[0] in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', u'①', u'②', u'③', u'④', u'⑤', u'⑥', u'⑦', u'⑧', u'⑨', u'⓪', u'１', u'２', u'３', u'４', u'５', u'６', u'７', u'８', u'９', u'０', u'（', u"(", u"＜", u"<", u"《", u"≪", u"【", u"［", u"[", u"○" ]:
            #print(u'1見出し行: ' + text)
            f2.append(1)
        else:
            match = re.search(r"\([0-9]\)", text)
            if match and match.start() == 0:
                #print(u'2見出し行: ' + text)
                f2.append(1)
            else:
                f2.append(0)

        # (3) 記述部の特徴
        if text.find(u"、") > 1 or len(text) > 25:
            #print(u'3記述部の特徴: ' + text)
            f3.append(1)
        else:
            f3.append(0)

        # (4) 文末に句点（。）がある
        if text[-1:] == u"。" or text[-1:] == u"｡":
            #print(u'4文末の句点: ' + text)
            f4.append(1)
        else:
            f4.append(0)

        # (5) 文中（文末より前）に句点（。）がある
        if text[:-1].find(u"。") > 0 or text[:-1].find(u"｡") > 0:
            #print(u'5文中の句点: ' + text)
            f5.append(1)
        else:
            f5.append(0)

        # (6) 注釈文の特徴
        pos = text.find(u"※")
        if pos == 0 and text[1].isnumeric():
            #print(u'6注釈行: ' + text)
            f6.append(1)
        else:
            f6.append(0)

    # ---- 行のタイプ判別 -------
    # 行の特徴ベクトル取得
    feature = []
    for i in range(0,len(buf)):
        #sys.stdout.write("feature : " + str(f1[i]) + str(f2[i]) + str(f3[i]) + str(f4[i]) + str(f5[i]) + str(f6[i]) + "\n")
        #sys.stdout.write("feature : " + buf[i])
        feature.append(str(f1[i]) + str(f2[i]) + str(f3[i]) + str(f4[i]) + str(f5[i]) + str(f6[i]))

    # 行の特徴ベクトルを使い、文抽出ルールを生成
    line_rule = []
    for i in range(0,len(feature)):
        #print(feature[i])

        if feature[i] == "100000":
            # ルール：出力しない
            line_rule.append("NO_OUTPUT")
        elif feature[i] == "010000":
            # ルール：見出し行とする
            line_rule.append("COMPLETE")
        elif feature[i] == "011000": # 見出し行、記述部の特徴
            # ルール：記述部とする（文頭）
            line_rule.append("START")
        elif feature[i] == "011100": # 見出し行、記述部の特徴、文末に句点
            # ルール：記述部とする（文末）
            line_rule.append("END")
        elif feature[i] == "000100": # 文末に句点
            # ルール：記述部とする（文末）
            line_rule.append("END")
        elif feature[i] == "000101": # 文末に句点、注釈文
            # ルール：注釈部とする（文末）
            line_rule.append("END")
        elif feature[i] == "001000": # 記述部の特徴
            # ルール：記述部とする
            line_rule.append("BODY")
        elif feature[i] == "001010": # 記述部の特徴、文中に句点
            # ルール：記述部とする（文分割が必要）
            line_rule.append("SPLIT")
        elif feature[i] == "001011": # 注釈部、文中に句点、記述部の特徴
            # ルール：注釈部とする（文分割が必要）
            line_rule.append("SPLIT")
        elif feature[i] == "001100": # 記述部の特徴、文末に句点
            # ルール：記述部とする（文末）
            line_rule.append("END")
        elif feature[i] == "001101": # 注釈部、文末に句点
            # ルール：注釈部とする（文末）
            line_rule.append("END")
        else:
            # ルール：記述部とする
            line_rule.append("BODY")

    # 文抽出ルールに従い、文単位を取得
    sent = []
    mem = ''
    for i in range(0,len(mod_line)):
        line = mod_line[i]
        #print("IN : " + line) 

        if line_rule[i] == "COMPLETE":
           if len(mem) > 0:
               sent.append(mem)
               mem = ''
           sent.append(line)
           #print("COMPLETE : " + line) 

        elif line_rule[i] == "START":
           mem = mem + line  # STARTではあるがもしmemがあれば連結しておく

        elif line_rule[i] == "END":
           sent.append(mem + line)
           #print("END : " + mem + line) 
           mem = ''

        elif line_rule[i] == "BODY":
           mem = mem + line

        elif line_rule[i] == "SPLIT":
           mem = mem + line

           sents = []
           if mem.find(u"。") > 0:
               sents = mem.split(u"。")
           elif mem.find(u"｡") > 0:
               sents = mem.split(u"｡")

           for i in range(0, len(sents)-1):
               sent.append(sents[i] + u"。")
               #print("SPLIT : " + sents[i]) 
           if len(sents) > 1:
               mem = sents[-1]

    if len(mem) > 0:
        sent.append(mem)
        #print("LAST : " + sents[i]) 

    return sent

# fixlineの本体
def fixline():

    # 入力ファイルの行データ
    buf = []

    # 引数から入力ファイルのパス、入力ファイルのエンコーディング指定、出力ファイルのパスを取得する
    ret = getargs()

    input_file = ret[0]
    coding = ret[1]
    output_file = ret[2]

    # 入力ファイルをオープン
    fi = codecs.open(input_file, 'r', coding)
 
    # 指定があれば、出力ファイルをオープン
    if len(output_file) > 0:
        fo = codecs.open(output_file, 'w', coding)
        output_on = True
    else:
        output_on = False

    # 入力ファイルを読み込む
    for line in fi:
        # バッファに入力ファイルの行をセット
        buf.append(line)

    # 入力ファイルをクローズ
    fi.close()

    # 文単位を取得する
    sent = getline(buf)

    # 出力ファイルに文単位の取得結果を書き出す
    for line in sent:
        if output_on:
            fo.write(line + "\n")   # ファイル出力
        else:
            print(line)  # 標準出力

    # 出力ファイルをクローズ
    if output_on:
        fo.close()
        print(" ****** fixline created the output file \"" + output_file + "\" ****** ")

# main
if __name__ == '__main__':
    fixline()
