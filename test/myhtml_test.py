import unittest
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../src"))

from model.node import HtmlNode
from model.myhtml import Html, HtmlOpError


class HtmlNodeTestCase(unittest.TestCase):
    def testTag(self):
        node = HtmlNode("A")
        self.assertEqual(node.tag, "A")
    
    def testId(self):
        node = HtmlNode("A")
        self.assertEqual(node.id, None)
        node = HtmlNode("A", "B")
        self.assertEqual(node.id, "B")
        
    def testChildren(self):
        nodes = [HtmlNode(str(i)) for i in range(1, 11)]
        self.assertEqual(nodes[0].children, [])
        nodes[0].add_child(nodes[1])
        self.assertEqual(nodes[0].children, [nodes[1]])
        nodes[0].add_child(nodes[2])
        self.assertEqual(nodes[0].children, [nodes[1], nodes[2]])
        nodes[0].del_child(nodes[1])
        self.assertEqual(nodes[0].children, [nodes[2]])

    def testStr(self):
        node = HtmlNode("A", "B")
        self.assertEqual(str(node), "A#B")
        node = HtmlNode("A")
        self.assertEqual(str(node), "A")


# Tree structure for testing
# t0#i0
# ├── t11#i11
# │   └── t21#i21
# └── t12#i12
class HtmlTestCase(unittest.TestCase):
    def testSet(self):
        tree = Html()
        tree.set("<t0 id=i0><t11 id=i11><t21 id=i21></t21></t11><t12 id=i12></t12></t0>")
        ref = HtmlNode("t0", "i0")
        ref.add_child(HtmlNode("t11", "i11"))
        ref.add_child(HtmlNode("t12", "i12"))
        ref.children[0].add_child(HtmlNode("t21", "i21"))
        self.assertTrue(self.cmp_tree(tree.root, ref))
        
    def testInsertSimple(self):
        tree = Html()
        tree.set("<t0 id=i0><t11 id=i11><t21 id=i21></t21></t11><t12 id=i12></t12></t0>")
        tree.insert("t115", "i115", "", "i12")
        ref = HtmlNode("t0", "i0")
        ref.add_child(HtmlNode("t11", "i11"))
        ref.add_child(HtmlNode("t115", "i115"))
        ref.add_child(HtmlNode("t12", "i12"))
        ref.children[0].add_child(HtmlNode("t21", "i21"))
        self.assertTrue(self.cmp_tree(tree.root, ref))
    
    def testInsertWithText(self):
        tree = Html()
        tree.set("<t0 id=i0><t11 id=i11><t21 id=i21></t21></t11><t12 id=i12></t12></t0>")
        tree.insert("t20", "i20", "sample-text", "i21")
        ref = HtmlNode("t0", "i0")
        ref.add_child(HtmlNode("t11", "i11"))
        ref.add_child(HtmlNode("t12", "i12"))
        ref.children[0].add_child(HtmlNode("t20", "i20"))
        ref.children[0].add_child(HtmlNode("t21", "i21"))
        ref.children[0].children[0].add_child(HtmlNode("sample-text"))
        ref.children[0].children[0].children[0].is_text = True
        self.assertTrue(self.cmp_tree(tree.root, ref))
    
    def testInsertFail(self):
        tree = Html()
        tree.set("<t0 id=i0><t11 id=i11><t21 id=i21></t21></t11><t12 id=i12></t12></t0>")
        self.assertRaises(HtmlOpError, lambda : tree.insert("html", "i", "", "i0"))
        self.assertRaises(HtmlOpError, lambda : tree.insert("t", "i", "", "i99"))
    
    def testAppend(self):
        tree = Html()
        tree.set("<t0 id=i0><t11 id=i11><t21 id=i21></t21></t11><t12 id=i12></t12></t0>")
        tree.append("t22", "i22", "", "i11")
        ref = HtmlNode("t0", "i0")
        ref.add_child(HtmlNode("t11", "i11"))
        ref.add_child(HtmlNode("t12", "i12"))
        ref.children[0].add_child(HtmlNode("t21", "i21"))
        ref.children[0].add_child(HtmlNode("t22", "i22"))
        self.assertTrue(self.cmp_tree(tree.root, ref))
    
    def testAppendFail(self):
        tree = Html()
        tree.set("<t0 id=i0><t11 id=i11><t21 id=i21></t21></t11><t12 id=i12></t12></t0>")
        self.assertRaises(HtmlOpError, lambda : tree.append("t", "i", "", "t0"))
    
    def testRemove(self):
        tree = Html()
        tree.set("<t0 id=i0><t11 id=i11><t21 id=i21></t21></t11><t12 id=i12></t12></t0>")
        tree.remove("i12")
        ref = HtmlNode("t0", "i0")
        ref.add_child(HtmlNode("t11", "i11"))
        ref.children[0].add_child(HtmlNode("t21", "i21"))
        self.assertTrue(self.cmp_tree(tree.root, ref))
    
    def testRemoveFail(self):
        tree = Html()
        tree.set("<t0 id=i0><t11 id=i11><t21 id=i21></t21></t11><t12 id=i12></t12></t0>")
        self.assertRaises(HtmlOpError, lambda : tree.remove("i"))
    
    def testFind(self):
        tree = Html()
        tree.set("<t0 id=i0><t11 id=i11><t21 id=i21></t21></t11><t12 id=i12></t12></t0>")
        self.assertTrue(tree.find("i21") == (tree.root.children[0].children[0], tree.root.children[0]))

    def testFindFail(self):
        tree = Html()
        tree.set("<t0 id=i0><t11 id=i11><t21 id=i21></t21></t11><t12 id=i12></t12></t0>")
        self.assertRaises(HtmlOpError, lambda : tree.find("i99"))
    
    def testEditId(self):
        tree = Html()
        tree.set("<t0 id=i0><t11 id=i11><t21 id=i21></t21></t11><t12 id=i12></t12></t0>")
        tree.update_id("i0", "i00")
        ref = HtmlNode("t0", "i00")
        ref.add_child(HtmlNode("t11", "i11"))
        ref.add_child(HtmlNode("t12", "i12"))
        ref.children[0].add_child(HtmlNode("t21", "i21"))
        self.assertTrue(self.cmp_tree(tree.root, ref))
    
    def testEditIdFail(self):
        tree = Html()
        tree.set("<t0 id=i0><t11 id=i11><t21 id=i21></t21></t11><t12 id=i12></t12></t0>")
        self.assertRaises(HtmlOpError, lambda : tree.update_id("i99", "i9"))
        self.assertRaises(HtmlOpError, lambda : tree.update_id("i11", "i0"))
    
    def testEditText(self):
        tree = Html()
        tree.set("<t0 id=i0><t11 id=i11><t21 id=i21>A bb ccc</t21></t11><t12 id=i12></t12></t0>")
        tree.update_text("i21", "Xxx yy z")
        ref = Html()
        ref.set("<t0 id=i0><t11 id=i11><t21 id=i21>Xxx yy z</t21></t11><t12 id=i12></t12></t0>")
        self.assertTrue(self.cmp_tree(tree.root, ref.root))

    def testEditTextFail(self):
        tree = Html()
        tree.set("<t0 id=i0><t11 id=i11><t21 id=i21>A bb ccc</t21></t11><t12 id=i12></t12></t0>")
        self.assertRaises(HtmlOpError, lambda : tree.update_text("i0", "TT"))
        self.assertRaises(HtmlOpError, lambda : tree.update_text("i99", "TT"))

    def cmp_tree(self, src, tgt):
        if str(src) != str(tgt):
            return False
        if len(src.children) != len(tgt.children):
            return False
        res = True
        for s, t in zip(src.children, tgt.children):
            res &= self.cmp_tree(s, t)
        return res


if __name__ == '__main__':  
    unittest.main()
