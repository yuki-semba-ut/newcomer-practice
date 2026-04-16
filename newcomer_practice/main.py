import gzip
import urllib.request
import os

url = "https://files.wwpdb.org/pub/pdb/derived_data/pdb_seqres.txt.gz"
filename = "pdb_seqres.txt.gz"

# ファイルが存在しない場合はダウンロードする
if not os.path.exists(filename):
    print(f"{filename} をダウンロードしています...（少し時間がかかります）")
    urllib.request.urlretrieve(url, filename)
    print("ダウンロードが完了しました。")

# ヒント1: 変数の初期化
allrecords = 0
count = 0

print("データを集計中です...")

# ヒント2: gzipファイルを展開しながらテキストモード('rt')で読み込む
with gzip.open(filename, 'rt', encoding='utf-8') as f:
    for line in f:
        # '>'で始まるヘッダー行を見つける
        if line.startswith('>'):
            allrecords += 1
            
            # 前後がスペース区切りであることを利用してリスト化
            parts = line.split()
            
            # 'length:xxx' の部分を探す
            for part in parts:
                if part.startswith('length:'):
                    # ':' で区切って後ろの数字を取得し、整数型(int)に変換
                    length_str = part.split(':')[1]
                    length = int(length_str)
                    
                    # ヒント3: 数字が100以下であるときにcountに1を足す
                    if length <= 100:
                        count += 1
                    
                    # lengthを見つけたら、この行の他の要素は探さなくてよいのでループを抜ける
                    break

# ヒント4: 最後に (count / allrecords * 100) を計算し、print()で表示する
if allrecords > 0:
    percentage = (count / allrecords) * 100
    print("-" * 30)
    print(f"全レコード数 (allrecords) : {allrecords:,} 件")
    print(f"100以下の数  (count)      : {count:,} 件")
    print(f"存在比率                  : {percentage:.2f} %")
else:
    print("レコードが見つかりませんでした。")