from hashlib import sha512

import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from model.parser import MyHtmlParser
from model.node import HtmlNode
from model.tree_visitor import TreeVisitor
from model.html_visitor import HtmlVisitor
from model.spellcheck_visitor import SpellcheckVisitor


class HtmlOpError(ValueError):
    pass


class Html:
    """Wraps a html file"""
    
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
        if self.id2node.get(self._tag2id(tag), None) != None:
            raise HtmlOpError(f"tag {tag} is reserved")
        if self.id2node.get(id, None) != None:
            raise HtmlOpError(f"id {id} already exists")
        if self.id2node.get(target, None) == None:
            raise HtmlOpError(f"target {target} does not exist")
        tar = self.id2node[target]
        if self.parent.get(tar, None) == None:
            raise HtmlOpError(f"cannot insert before target {target}")

        node = HtmlNode(tag, id)
        if text != "":
            text_node = HtmlNode(text)
            text_node.is_text = True
            node.add_child(text_node)
        self.parent[tar].add_child(node, self.parent[tar].children.index(tar))
        self.id2node[node.id] = node
        self.parent[node] = self.parent[tar]
    
    def append(self, tag, id, text, target):
        if self.id2node.get(self._tag2id(tag), None) != None:
            raise HtmlOpError(f"tag {tag} is reserved")
        if self.id2node.get(id, None) != None:
            raise HtmlOpError(f"id {id} already exists")
        if self.id2node.get(target, None) == None:
            raise HtmlOpError(f"target {target} does not exist")

        node = HtmlNode(tag, id)
        if text != "":
            text_node = HtmlNode(text)
            text_node.is_text = True
            node.add_child(text_node)
        self.id2node[target].add_child(node)
        self.id2node[node.id] = node
        self.parent[node] = self.id2node[target]
    
    def append_(self, node, target): # undo delete
        target.add_child(node)
        self.id2node[node.id] = node
        self.parent[node] = target
    
    def remove(self, target):
        if self.id2node.get(target, None) == None:
            raise HtmlOpError(f"target {target} does not exist")
        tar = self.id2node[target]
        self.parent[tar].del_child(tar)
        self.id2node.pop(target)
        self.parent.pop(tar)
    
    def find(self, target):
        if self.id2node.get(target, None) == None:
            raise HtmlOpError(f"target {target} does not exist")
        node = self.id2node[target]
        return node, self.parent[node]
    
    def update_id(self, oldid, newid):
        if self.id2node.get(oldid, None) == None:
            raise HtmlOpError(f"target {oldid} does not exist")
        tar = self.id2node[oldid]
        tar.id = newid
        self.id2node[newid] = tar
        self.id2node.pop(oldid)
    
    def update_text(self, target, text):
        if self.id2node.get(target, None) == None:
            raise HtmlOpError(f"target {target} does not exist")
        tar = self.id2node[target]
        if len(tar.children) == 0 or not tar.children[0].is_text:
            raise HtmlOpError(f"target {target} does not have text")
        if text == "":
            tar.children.pop(0)
        else:
            tar.children[0].tag = text
    
    def get_text_of(self, target):
        if self.id2node.get(target, None) == None:
            raise HtmlOpError(f"target {target} does not exist")
        tar = self.id2node[target]
        if len(tar.children) == 0 or not tar.children[0].is_text:
            raise HtmlOpError(f"target {target} does not have text")
        return tar.children[0].tag
    
    def as_tree(self):
        visitor = TreeVisitor()
        self.root.accept(visitor)
        return visitor.get_content()
    
    def as_text(self, indent):
        visitor = HtmlVisitor(indent)
        self.root.accept(visitor)
        return visitor.get_content()
    
    def spell_check(self):
        visitor = SpellcheckVisitor()
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
