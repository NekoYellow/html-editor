import unittest
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../src"))

from myhtml.node import HtmlNode


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


if __name__ == '__main__':  
        unittest.main()