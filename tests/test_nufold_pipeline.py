import csv
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts/nufold"))

from common import (  # noqa: E402
    _write_immutable,
    a3m_query_sequence,
    count_a3m_records,
    parse_usalign,
    pdb_residues,
    read_manifest,
    read_native_positions,
    sha256_file,
    validate_ranked_pdb,
    write_mapped_prediction,
)
from run_batch import input_files_only, prepare_a3m  # noqa: E402


def pdb_atom(serial, atom, residue, chain, resseq, x=1.0):
    atom_field = f" {atom:<3}" if len(atom) < 4 and atom[:1].isalpha() else f"{atom:>4}"
    return (f"ATOM  {serial:5d} {atom_field} {residue:>3} {chain}{resseq:4d}    "
            f"{x:8.3f}{2.0:8.3f}{3.0:8.3f}{1.0:6.2f}{50.0:6.2f}          C  ")


class PipelineHelpersTest(unittest.TestCase):
    def test_frozen_manifest_has_ten_unique_targets(self):
        manifest = ROOT / "data/pilot/rna3d_template_sparse_pilot_v1.csv"
        if not manifest.is_file():
            self.skipTest("frozen pilot manifest is an external dataset and is not committed")
        rows = read_manifest(manifest)
        self.assertEqual(len(rows), 10)
        self.assertEqual(len({row["target_id"] for row in rows}), 10)
        target = next(row for row in rows if row["target_id"] == "9cf2_W")
        self.assertEqual(target["sequence"], "UUAUCCACCAAAGUUAUCGCUUUGGUCAAUUAAUGCAGGUAAGCAACAUCCAGCAAACAGA")

    def test_single_sequence_a3m_is_labeled_by_count_and_query(self):
        target = {"target_id": "toy", "sequence": "ACGU"}
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "toy.a3m"
            count = prepare_a3m(target, "single_sequence", None, out)
            self.assertEqual(count, 1)
            self.assertEqual(count_a3m_records(out), 1)
            self.assertEqual(a3m_query_sequence(out), "ACGU")

    def test_genuine_a3m_requires_matching_query_and_depth(self):
        target = {"target_id": "toy", "sequence": "ACGU"}
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "toy.a3m"
            source.write_text(">query\nACGU\n>hit\nAC-U\n")
            out = root / "staged/toy.a3m"
            self.assertEqual(prepare_a3m(target, "genuine", root, out), 2)
            self.assertEqual(out.read_text(), source.read_text())
            source.write_text(">query\nAAAA\n>hit\nAAAA\n")
            with self.assertRaisesRegex(ValueError, "does not match"):
                prepare_a3m(target, "genuine", root, root / "bad.a3m")
            source.write_text(">query\nACGU\n")
            with self.assertRaisesRegex(ValueError, "at least two"):
                prepare_a3m(target, "genuine", root, root / "single.a3m")

    def test_manifest_validation_rejects_wrong_length(self):
        with tempfile.TemporaryDirectory() as tmp:
            manifest = Path(tmp) / "manifest.csv"
            manifest.write_text("target_id,pdb_id,chain_id,sequence,length,release_date,template_screen_status\ntoy,1abc,A,ACGU,5,2020-01-01,no_historical_hit\n")
            with self.assertRaisesRegex(ValueError, "length does not match"):
                read_manifest(manifest)

    def test_native_map_records_observed_positions_only(self):
        positions = read_native_positions(ROOT / "data/pilot/native_eval/9cf2_W_residue_map.csv")
        self.assertEqual(positions, list(range(4, 62)))
        native = pdb_residues(ROOT / "data/pilot/native_eval/9cf2_W_native_eval.pdb")
        self.assertEqual(len(native), 58)
        self.assertEqual("".join(r["one"] for r in native),
                         "UCCACCAAAGUUAUCGCUUUGGUCAAUUAAUGCAGGUAAGCAACAUCCAGCAAACAGA")

    def test_prediction_mapping_trims_missing_native_positions(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "toy.pdb"
            lines = [pdb_atom(1, "P", "A", "A", 1), pdb_atom(2, "P", "C", "A", 2, 2),
                     pdb_atom(3, "P", "G", "A", 3, 3)]
            source.write_text("\n".join(lines + ["END"]) + "\n")
            self.assertEqual(validate_ranked_pdb(source, 3)["sequence"], "ACG")
            mapped = root / "mapped.pdb"
            self.assertEqual(write_mapped_prediction(source, mapped, "ACG", [2, 3]), 2)
            mapped_residues = pdb_residues(mapped)
            self.assertEqual([r["resseq"] for r in mapped_residues], ["2", "3"])
            self.assertEqual("".join(r["one"] for r in mapped_residues), "CG")

    def test_input_tree_rejects_native_coordinates(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "x.cif.gz").write_bytes(b"native")
            with self.assertRaisesRegex(RuntimeError, "forbidden"):
                input_files_only(root)

    def test_completed_input_file_is_not_overwritten(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "input.fasta"
            _write_immutable(p, ">x\nACGU\n")
            before = sha256_file(p)
            with self.assertRaises(FileExistsError):
                _write_immutable(p, ">x\nAAAA\n")
            self.assertEqual(sha256_file(p), before)

    def test_usalign_parser_returns_metrics_and_coverage(self):
        sample = """Number of residues in common= 58\nRMSD of the common residues= 17.350\nTM-score = 0.2468\n"""
        result = parse_usalign(sample, 58)
        self.assertEqual(result["alignment_residues"], 58)
        self.assertEqual(result["alignment_coverage"], 1.0)
        self.assertEqual(result["tm_score"], 0.2468)
        self.assertEqual(result["rmsd_angstrom"], 17.35)
        with self.assertRaisesRegex(ValueError, "Could not parse"):
            parse_usalign("not USalign output", 58)


if __name__ == "__main__":
    unittest.main()
