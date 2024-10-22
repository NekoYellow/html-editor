from hashlib import sha512

import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from model.parser import MyHtmlParser
from model.node import HtmlNode
from model.tree_visitor import TreeVisitor
from model.html_visitor import HtmlVisitor


class Html:
    def __init__(self):
        self.id2node = {} # id -> node
        self.parent = {} # node -> parent
        self.root = HtmlNode("html", None,
                        HtmlNode("head", None,
                            HtmlNode("title", None)
                        ),
                        HtmlNode("body", None)
                    )
        self._get_mappings()

    def set(self, html_str):
        parser = MyHtmlParser()
        parser.feed(html_str)
        self.root = parser.get_tree()
        self._get_mappings()
    
    def insert(self, tag, id, text, target):
        if self.id2node.get(id, None) != None:
            raise ValueError(f"id {id} already exists")
        if self.id2node.get(target, None) == None:
            raise ValueError(f"target {target} does not exist")
        tar = self.id2node[target]
        if self.parent.get(tar, None) == None:
            raise ValueError(f"cannot insert before target {target}")

        node = HtmlNode(tag, id)
        if text != "":
            text_node = HtmlNode(text)
            text_node.is_text = True
            node.add_child(text_node)
        self.parent[tar].add_child(node, self.parent[tar].children.index(node))
    
    def append(self, tag, id, text, target):
        if self.id2node.get(id, None) != None:
            raise ValueError(f"id {id} already exists")
        if self.id2node.get(target, None) == None:
            raise ValueError(f"target {target} does not exist")

        node = HtmlNode(tag, id)
        if text != "":
            text_node = HtmlNode(text)
            text_node.is_text = True
            node.add_child(text_node)
        self.id2node[target].add_child(node)
    
    def append_(self, node, target): # undo delete
        target.add_child(node)
    
    def remove(self, target):
        if self.id2node.get(target, None) == None:
            raise ValueError(f"target {target} does not exist")
        self.parent[target].del_child(target)
    
    def find(self, target):
        if self.id2node.get(target, None) == None:
            raise ValueError(f"target {target} does not exist")
        node = self.id2node[target]
        return node, self.parent[node]
    
    def as_tree(self):
        visitor = TreeVisitor()
        self.root.accept(visitor)
        return visitor.get_content()
    
    def as_text(self):
        visitor = HtmlVisitor()
        self.root.accept(visitor)
        return visitor.get_content()
    
    def _get_mappings(self):
        self.id2node.clear()
        self.parent.clear()
        def dfs(u):
            self.id2node[u.id if u.id != None else self._tag2id(u.tag)] = u
            for v in u.children:
                self.parent[v] = u
                dfs(v)
        dfs(self.root)
    
    def _tag2id(self, t):
        return sha512(t.encode()).hexdigest()
