"""Thành viên 6 - Kiểm thử toàn bộ chương trình."""
import os, sys, tempfile, unittest
from fractions import Fraction
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from solver import giai_pt_bac_1, giai_pt_tong_quat, MOT_NGHIEM, VO_NGHIEM, VO_SO_NGHIEM
from validators import doc_so, dinh_dang_so
from steps import tao_loi_giai
from history import luu_lich_su, doc_lich_su, them_muc

F = Fraction


class TestSolver(unittest.TestCase):
    def test_mot_nghiem(self):
        self.assertEqual(giai_pt_bac_1(F(2), F(-4)), (MOT_NGHIEM, F(2)))

    def test_vo_nghiem(self):
        self.assertEqual(giai_pt_bac_1(F(0), F(5))[0], VO_NGHIEM)

    def test_vo_so_nghiem(self):
        self.assertEqual(giai_pt_bac_1(F(0), F(0))[0], VO_SO_NGHIEM)

    def test_tong_quat(self):
        # 3x + 2 = x + 8  ->  x = 3
        self.assertEqual(giai_pt_tong_quat(F(3), F(2), F(1), F(8)), (MOT_NGHIEM, F(3)))
        # 2x + 1 = 2x + 5 -> vô nghiệm
        self.assertEqual(giai_pt_tong_quat(F(2), F(1), F(2), F(5))[0], VO_NGHIEM)


class TestValidators(unittest.TestCase):
    def test_doc_so(self):
        self.assertEqual(doc_so("1,5"), F(3, 2))
        self.assertEqual(doc_so("3/4"), F(3, 4))
        self.assertEqual(doc_so("", "c", mac_dinh=0), F(0))
        with self.assertRaises(ValueError):
            doc_so("abc")
        with self.assertRaises(ValueError):
            doc_so("")

    def test_dinh_dang(self):
        self.assertEqual(dinh_dang_so(F(6, 2)), "3")
        self.assertIn("≈", dinh_dang_so(F(1, 3)))


class TestSteps(unittest.TestCase):
    def test_loi_giai(self):
        self.assertIn("x = 3", tao_loi_giai(F(3), F(2), F(1), F(8))[-1])
        self.assertIn("VÔ NGHIỆM", tao_loi_giai(F(0), F(5), F(0), F(0))[-1])


class TestHistory(unittest.TestCase):
    def test_luu_doc(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = os.path.join(tmp, "ls.json")
            self.assertEqual(doc_lich_su(p), [])
            luu_lich_su(["a", "b"], p)
            self.assertEqual(doc_lich_su(p), ["a", "b"])

    def test_them_muc_gioi_han(self):
        ds = them_muc(["x", "y"], "z", toi_da=2)
        self.assertEqual(ds, ["z", "x"])


if __name__ == "__main__":
    unittest.main()
