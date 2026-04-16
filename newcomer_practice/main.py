import argparse
import gzip
import os


def main():
    # 1. 引数の設定
    parser = argparse.ArgumentParser(description="課題F: PDBデータの解析")
    parser.add_argument(
        "-i",
        "--input",
        type=str,
        required=True,
        help="入力ファイルパス (pdb_seqres.txt.gz)",
    )
    parser.add_argument(
        "-l", "--limit", type=int, default=100, help="残基数のカットオフ値"
    )

    args = parser.parse_args()

    # 2. 課題E-1のロジック（例：残基数の割合を計算）
    # ここでは、指定されたファイルを開いて処理する流れを記述します
    if not os.path.exists(args.input):
        print(f"Error: {args.input} が見つかりません。")
        return

    count_below_limit = 0
    total_count = 0

    # gzipファイルを開いて解析するロジック（課題Eの内容に合わせて調整してください）
    with gzip.open(args.input, "rt") as f:
        # ここに、課題E-1で作成した「残基数を数えて割合を出す」ロジックを入れます
        # 以下は実装のヒント（疑似コード）です
        for line in f:
            if line.startswith(">"):
                total_count += 1
                # 例：ヘッダーから残基数を取得して args.limit と比較する処理など
                pass

    print(f"ファイル: {args.input}")
    print(f"カットオフ値 (-l): {args.limit}")
    print(f"結果: 残基数{args.limit}以下の割合を表示します（ここに計算結果）")


if __name__ == "__main__":
    main()
