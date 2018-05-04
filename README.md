# fixline (version 0.01),  Date: May 4, 2018,  Author: tatskoba

(1) コードの説明 (Description of this code)
fixlineは、文の途中で改行された日本語テキストファイルから、文単位を抽出・修復し、取り出すためのコマンドラインで使えるPythonツールです。
fixline is a Python command tool to extract/restore a unit of sentence from Japanese text with line break in the middle of sentence.

PythonとGitHubの練習のために作ってみました。
I just made this code for learning Python and GitHub. 

(2) 使い方（How to use)
usage: python fixline input_file [-e encoding] [-o output_file]

positional arguments:
  input_file

optional arguments:
  -h, --help            show this help message and exit
  -e ENCODING, --encoding ENCODING
                        Encoding of input file. Default is utf-8.
  -o OUTPUT_FILE, --output_file OUTPUT_FILE
                        Path of output file.
  --version             show program's version number and exit

(3) サンプルテキストの説明 (Sample text)
- Sample text: 
  sample/ntt-docomo-2018-3.txt
- Original data source: 
  https://www.nttdocomo.co.jp/corporate/ir/binary/pdf/library/earnings/earnings_release_fy2017_4q.pdf
- How to use fixline: 
  $ python fixline.py sample/ntt-docomo-2018-3.txt -e utf-8 -o sample/output_ntt-docomo-2018-3.txt

(4) 今後の予定 (To Do)
・文抽出精度の改善。できれば、ルール方式から機械学習方式への切り替え。
  Improvement of accuracy in extracting sentences. Maybe, from rule-based to machine learning.
・日本語以外の言語への対応
  Will expand to other languages (English, Chinese, ...) in addition to Japanese.  
・バグFIX
  Bug fix, but don't know if it exists.

