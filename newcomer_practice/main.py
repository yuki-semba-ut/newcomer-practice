import argparse
import gzip
import os

from Bio.PDB import FastMMCIFParser, NeighborSearch, Selection


def main():
    parser = argparse.ArgumentParser(description="課題F: PDB近傍探索ツール")
    parser.add_argument(
        "-i", "--input", type=str, required=True, help="解析する.cif.gzファイルへのパス"
    )
    parser.add_argument(
        "-l", "--limit", type=float, default=5.0, help="探索距離 (オングストローム)"
    )
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Error: {args.input} が見つかりません。")
        return

    # 課題Eのロジック開始
    pdb_id = "target"  # 表示用
    parser_pdb = FastMMCIFParser(QUIET=True)

    with gzip.open(args.input, "rt") as f:
        struc = parser_pdb.get_structure(pdb_id, f)

    po4_resid = None
    for model in struc:
        if "A" in model:
            chain_a = model["A"]
            for residue in chain_a:
                if residue.get_resname() == "PO4":
                    po4_resid = residue
                    break
        if po4_resid:
            break

    if po4_resid is None:
        print("PO4 residue not found.")
        return

    all_atoms = Selection.unfold_entities(struc, "A")
    ns = NeighborSearch(all_atoms)

    nearby_residues = set()
    for atom in po4_resid:
        # -l で指定した距離(args.limit)を使って検索
        neighbors = ns.search(atom.get_coord(), args.limit, level="R")
        nearby_residues.update(neighbors)

    water_resnames = ["HOH", "WAT", "H2O"]
    print(f"--- 検索結果 (距離: {args.limit}A) ---")
    for res in sorted(nearby_residues, key=lambda x: x.id[1]):
        resname = res.get_resname()
        if resname not in water_resnames and resname != "PO4":
            print(f"{resname}-{res.id[1]}")


if __name__ == "__main__":
    main()
