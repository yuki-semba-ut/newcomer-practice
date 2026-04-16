import argparse
import gzip
import os


def main():
    parser = argparse.ArgumentParser(description="課題F: PDBデータの解析")
    parser.add_argument(
        "-i", "--input", type=str, required=True, help="入力ファイルパス"
    )
    parser.add_argument(
        "-l", "--limit", type=int, default=100, help="残基数のカットオフ値"
    )
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Error: {args.input} が見つかりません。")
        return

    # --- ここに実際の計算ロジックを入れる ---
    count_below = 0
    total = 0

    with gzip.open(args.input, "rt") as f:
        for line in f:
            if line.startswith(">"):
                total += 1
                # ヘッダー行から残基数を抽出する（例: length=123 の部分を抜き出す）
                # 課題E-1で書いたコードをここに貼り付けてください
                try:
                    length = int(line.split("length=")[1].split()[0])
                    if length <= args.limit:
                        count_below += 1
                except (IndexError, ValueError):
                    continue

    if total > 0:
        ratio = (count_below / total) * 100
        print(f"ファイル: {args.input}")
        print(f"カットオフ値 (-l): {args.limit}")
        print(
            f"結果: 残基数{args.limit}以下の割合は {ratio:.2f}% です ({count_below}/{total})"
        )
    else:
        print("データが見つかりませんでした。")


if __name__ == "__main__":
    main()
