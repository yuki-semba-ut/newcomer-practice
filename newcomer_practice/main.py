import argparse
import gzip
import os
import urllib.request

def main():
    # 1. 引数の設定（課題Fの要件）
    parser = argparse.ArgumentParser(description='課題F: PDBデータの集計ツール')
    parser.add_argument('-i', '--input', type=str, required=True, help='入力ファイルパス (例: pdb_seqres.txt.gz)')
    parser.add_argument('-l', '--limit', type=int, default=100, help='残基数のカットオフ値 (デフォルト: 100)')
    args = parser.parse_args()

    # 2. ファイルの存在確認とダウンロード（あなたのコードのロジック）
    # ※もし -i で指定したファイルがなくても、指定の名前でダウンロードを試みます
    filename = args.input
    if not os.path.exists(filename):
        url = "https://files.wwpdb.org/pub/pdb/derived_data/pdb_seqres.txt.gz"
        print(f"{filename} が見つからないため、ダウンロードを開始します...")
        urllib.request.urlretrieve(url, filename)

    # 3. 集計ロジック（あなたのコードを引数対応に調整）
    allrecords = 0
    count = 0
    print(f"データを集計中... (カットオフ値: {args.limit})")

    with gzip.open(filename, 'rt', encoding='utf-8') as f:
        for line in f:
            if line.startswith('>'):
                allrecords += 1
                parts = line.split()
                for part in parts:
                    if part.startswith('length:'):
                        # あなたの書いたロジック
                        length = int(part.split(':')[1])
                        # 固定の 100 ではなく args.limit を使う
                        if length <= args.limit:
                            count += 1
                        break

    # 4. 結果の表示
    if allrecords > 0:
        percentage = (count / allrecords) * 100
        print("-" * 30)
        print(f"対象ファイル      : {filename}")
        print(f"全レコード数      : {allrecords:,} 件")
        print(f"残基数{args.limit}以下の数 : {count:,} 件")
        print(f"存在比率          : {percentage:.2f} %")
    else:
        print("レコードが見つかりませんでした。")

if __name__ == "__main__":
    main()