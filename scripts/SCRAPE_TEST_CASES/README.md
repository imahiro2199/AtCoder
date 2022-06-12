# SCRAPE_TEST_CASES

## 概要
AtCoder のコンテストページにアクセスし、入力例と出力例をscrapeして`.txt`で出力する。

### 出力ファイル形式
以下の内容を `./[TEST_CASE_HOME]/[question].txt` に出力する。
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
- `[question]` はスクレイプ対象のページの最後の `_` 以降の文字列を小文字にしたものになる。  
    取得に失敗した場合は適当な番号に置き換えられる。
    - e.g., `https://atcoder.jp/contests/abcXXX/tasks/abcXXX_a` → `[question]` = `a`

### ログイン情報の保存
暗号化して `SCRAPE_TEST_CASES/cfg/*` に保存する。
- 出力先パスは `config.py` で設定できるが、保存先を変更したい場合はデフォルトの出力先で必要ファイルを生成後、読み込み先(`KEY_PATH`, `USERNAME_PATH`, `PASSWORD_PATH`)を設定し各ファイルを移動することを推奨。
- 取扱いに注意すること。
- `config.py` の `USERNAME`, `PASSWORD` に直接書き込むこともできる、、、

## 必要環境
- Python (3.X.X)
    - PyCrypto
        ```shell
        pip install pycrypto
        ```
    - Requests
        ```shell
        pip install requests
        ```
    - BeautifulSoup4
        ```shell
        pip install beautifulsoup4
        ```

## 使用方法
### テストケースのスクレイピング
1. `SCRAPE_TEST_CASES` と同階層に[`LIB`](../LIB/) を配置する
    ```
    ├─LIB
    └─SCRAPE_TEST_CASES
    ```
1. テストケースを保存したいディレクトリへ移動
1. 以下を実行する
    ```shell
    python (SCRAPE_TEST_CASESまでのパス/)scrape_test_cases.py [url]
    ```
    - `[url]`: テストケースを取得したいコンテストのトップページ
        - e.g., `https://atcoder.jp/contests/abcXXX`
        - 指定しない場合、`https://atcoder.jp/contests/[カレントディレクトリのフォルダ名]` が設定される。
    - ログイン情報の取得に必要なファイルが存在しない場合は最初にログイン情報を保存するプログラムが実行される。

### ログイン情報の更新/再生成
- ログイン情報を更新/再生成したい場合は、以下を実行する。
    ```shell
    python (SCRAPE_TEST_CASESまでのパス/)login_control.py
    ```

## 動作前提
コンテストのトップページが `https://atcoder.jp/contests/abcXXX` の場合
- `https://atcoder.jp/contests/abcXXX/tasks` の `tbody` タグ内に各問題ページのリンクが記載されている
- 各問題ページについて、class が `lang-ja` の `span` タグ内の `pre` タグに入出力例が記載されている
- 入出力例以外は `var` タグが使用されている

## テスト環境
- Windows PowerShell
    - 5.1.19041.1682
- Python
    - 3.10.0
