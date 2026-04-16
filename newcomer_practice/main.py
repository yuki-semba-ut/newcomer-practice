import urllib.request
import gzip
import os
from Bio.PDB import FastMMCIFParser, NeighborSearch, Selection

# --- 1. urllib.request を使って 1alk.cif.gz を取得 ---
pdb_id = "1alk"
url = f"https://files.rcsb.org/download/{pdb_id}.cif.gz"
filename = f"{pdb_id}.cif.gz"

if not os.path.exists(filename):
    print(f"Downloading {url}...")
    urllib.request.urlretrieve(url, filename)

# --- 2. 1alk.cif.gz の構造情報を取り込み ---
# FastMMCIFParser を使用。gzファイルなので gzip モジュールで開きます。
parser = FastMMCIFParser(QUIET=True)
with gzip.open(filename, "rt") as f:
    struc = parser.get_structure(pdb_id, f)

# --- 3. struc の中で 「Chain A」かつ「残基名がPO4」に該当する残基を取得 ---
po4_resid = None
for model in struc:
    if 'A' in model:
        chain_a = model['A']
        for residue in chain_a:
            if residue.get_resname() == 'PO4':
                po4_resid = residue
                break
    if po4_resid:
        break

if po4_resid is None:
    print("Error: PO4 residue not found in Chain A.")
    exit()

# --- 4. NeighborSearchを使った近傍探索 ---
# 探索対象となる全原子のリストを作成
all_atoms = Selection.unfold_entities(struc, 'A') 
ns = NeighborSearch(all_atoms)

# PO4_resid のすべての原子から5.0A以内に存在する残基(level="R")をセットとして取得
nearby_residues = set()
for atom in po4_resid:
    # 探索レベルを 'R' (Residue) に設定
    neighbors = ns.search(atom.get_coord(), 5.0, level='R')
    nearby_residues.update(neighbors)

# --- 5. 結果の書き出し ---
# 水分子(HOH)やPO4自身を除外して、指定の書式で表示
water_resnames = ['HOH', 'WAT', 'H2O']

# 残基番号順にソートして表示（課題では順不同OKですが、見やすさのため）
for res in sorted(nearby_residues, key=lambda x: x.id[1]):
    resname = res.get_resname()
    residue_no = res.id[1]
    
    # 水分子以外、かつアミノ酸残基（PO4自身を除外）を判定
    # 一般的にアミノ酸は3文字の名称。PO4や水を除外する条件
    if resname not in water_resnames and resname != 'PO4':
        print(f"{resname}-{residue_no}")