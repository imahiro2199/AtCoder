# RUN_ALL_TEST_CASES

## 概要
テストケースが記載された `.txt` を読み込み、

### 入力ファイル形式
- ソースコード
    - `./[question].xx` 
    - 詳細は[使用方法](#使用方法)を参照
- テストケース
    - 以下の内容が書かれた `./[TEST_CASE_HOME]/[question].txt` を入力とする。
        ```txt
        入力例 1
        [空行]
        出力例 1
        [空行]
        入力例 2
        [空行]
        出力例 2
        [空行]
        …
        入力例 N
        [空行]
        出力例 N
        [空行]
        ```
- `[TEST_CASE_HOME]` は `config.py` で設定できる。デフォルトは `answer` 。

## 実行環境
- Python (3.X.X)
- 実行するコードの動作環境

## 使用方法
### テストケースの実行
1. `RUN_ALL_TEST_CASES` と同階層に[`LIB`](../LIB/) を配置する
    ```
    ├─LIB
    └─RUN_ALL_TEST_CASES
    ```
1. ソースコードとテストケースが保存されたフォルダを含むディレクトリへ移動する
    - e.g.,
        ```
        . (Current Directory)
        │  a.cpp
        │  b.cpp
        │  c.cpp
        └─answer # if [TEST_CASE_HOME] = 'answer'
               a.txt
               b.txt
               c.txt
        ```
1. 以下を実行する
    ```shell
    python (RUN_ALL_TEST_CASESまでのパス/)run_all_test_cases.py [question] [lang]
    ```
    - `[question]`: 実行したいテストケースとそのソースファイル名
        - e.g., `[question]` = `a`
            - テストケース：`./answer/a.txt`
            - ソースファイル名： `a.cpp`
    - `[lang]`: 実行したいソースコードの実行環境の指定
        - [ソースコードの実行環境の設定](#ソースコードの実行環境の設定)にて設定
        - 指定されなかった場合は、 `config.py` の `DEFAULT_LANG` が設定される

### 現在確認できている対応していないテストケース
- 対話式のテストケース
    - 対応予定なし
- 想定解が複数あるテストケース
    - 対応不可
- 誤差を許容するテストケース
    - 未対応、目視で確認してください

### ソースコードの実行環境の設定
`config.py` の `commands(lang, run_question, build_path)` に Terminal に打ち込むコマンドを設定する。
`BUILD_FOLDER` にて実行ファイルや一時ファイルを保存するフォルダを設定できる。  
- `commands(lang, run_question, build_path)` の引数
    - lang
        - `run_all_test_cases.py` の第二引数
    - run_question
        - `run_all_test_cases.py` の第一引数
    - build_path
        - `"./[BUILD_FOLDER]/"` (Windows: `".\\[BUILD_FOLDER]\\"`)
- 設定項目
    - `if(elif) lang == "[lang]"`
        - `run_all_test_cases.py` の第二引数にて指定する `[lang]` の判定文  
            この判定文の中に以下の2つの変数を設定する
    - `compile_commands`
        - コンパイルなど、テストケースを実行する前に行う処理をまとめたコマンド  
            リスト (`[xx, yy, ...]`) で設定(複数コマンド設定可能)
    - `run_command`
        - テストケースを実行する際のコマンド  
            `str` 型で設定
- 設定例  
注) `PS_CNCT` = `"\\"` (Windows), `"/"` (Mac, Linux)
    - `c++` の場合
        - 実行コマンド例
            ```shell
            g++ -o ./[BUILD_FOLDER]/[question] .[question].cpp # コンパイル
            [BUILD_FOLDER]/[question].exe # 実行
            [テストケースの入力] # 入力
            ```
        - 実行コマンド例に対する `config.py` の設定
            ```python
            if  (lang == "c++"): # or elif (lang == "c++"):
                compile_commands = ['g++ -o ' + build_path + run_question + ' .' + PS_CNCT + run_question + '.cpp']
                run_command      = build_path + run_question + '.exe'
            ```
    - `python` の場合
        - 実行コマンド例
            ```shell
            python [question].py # 実行
            [テストケースの入力] # 入力
            ```
        - 実行コマンド例に対する `config.py` の設定
            ```python
            elif(lang == "python"): # or elif (lang == "python"):
                compile_commands = []
                run_command      = 'python ' + run_question + '.py'
            ```
### その他設定
`config.py` にて以下の設定が可能
- `TLE_SECOND`
    - タイムアウト時間(sec)
- テストケースのファイル名 `[question]` が(小文字)、実行ファイル名 `[question]` が大文字のときの対処
    - commands()内で以下のようにコメントアウトを外す
        ```diff
        # Uncomment if your source code file name is uppercase letter.
        - # run_question.upper()
        + run_question.upper()
        ```
    - 実行時の `[question]` は小文字で指定

## テスト環境
- Windows PowerShell
    - 5.1.19041.1682
- Python
    - 3.10.0
