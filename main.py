from pprint import pprint
from typing import Optional, Set, List, Tuple


class NodeTree(dict):
    @classmethod
    def make_tree(cls, data: List[Tuple[str, str]]):
        """Builds an ordered grouping of Nodes out of a list of tuples
        of the form (parent, name). Returns the last Node.
        """
        tree = cls()

        def _get_or_create_node(node_name: str ):
            result_node = tree.get(node_name, None)
            if result_node is None:
                result_node = Node.make_child(name)
                tree[result_node.name] = result_node
                return result_node
            try:

                result_node.descendants.index(name)
            except ValueError:
                result_node.descendants.append(name)
            return result_node

        for parent, name in data:
            if parent is None:
                _get_or_create_node(name)
            else:
                parent_node = _get_or_create_node(parent)
                tree_node = Node.make_child(name, parent=parent_node.name, ancestors=parent_node.ancestors + [parent])
                tree[tree_node.name] = tree_node
        return tree

    @classmethod
    def parse_tree(cls, node_tree: "NodeTree"):
        """Given any node in a singly-rooted tree, returns a dictionary
        of the form requested in the question
        """

        def _parse_subtree(base_node: "Node"):
            """Actually does the parsing, starting with the node given
            as its root.
            """

            if not base_node.descendants:
                # base case, if there are no children then return an empty dict
                return {}
            sub_result = {}
            for descendant in base_node.descendants:
                sub_result.update({node_tree[descendant].name: _parse_subtree(node_tree[descendant])})
            return sub_result
        temp_result = {}
        for key, value in node_tree.items():
            if value.parent is None:
                temp_result[key] = _parse_subtree(value)
            else:
                root_node_name = value.ancestors[0]
                if root_node_name not in temp_result:
                    temp_result[root_node_name] = _parse_subtree(node_tree[root_node_name])
        return temp_result


class Node(object):
    def __init__(self, name: str, parent: Optional[str] = None, ancestors: Optional[List[str]] = None,
                 descendants: Optional[List[str]] = None, *args, **kwargs):
        if ancestors is None:
            ancestors = []
        if descendants is None:
            descendants = []
        assert isinstance(name, str), 'Node name must be string type'
        assert parent is None or isinstance(parent, str), 'Parent name must be string type'
        self.name = name
        self.parent = parent
        self.ancestors = ancestors
        self.descendants = descendants
        super().__init__(*args, **kwargs)

    @classmethod
    def make_child(cls, node_name, parent: Optional[str] = None, descendants: Optional[List[str]] = None,
                   ancestors: Optional[List[str]] = None, ):
        if ancestors is None:
            ancestors = []
        other = cls(node_name, parent, ancestors=ancestors, descendants=descendants)
        return other

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.name == other.name
        elif isinstance(other, str):
            return self.name == other
        else:
            return NotImplemented

    def __ne__(self, other):
        return not (self == other)

    def __hash__(self):
        return hash(self.name)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


def main(data: List[Tuple[str, str]]):
    tree = NodeTree.make_tree(data)
    return NodeTree.parse_tree(tree)


if __name__ == '__main__':
    source = [
        (None, 'a'),
        (None, 'b'),
        (None, 'c'),
        ('a', 'a1'),
        ('a', 'a2'),
        ('a2', 'a21'),
        ('a2', 'a22'),
        ('b', 'b1'),
        ('b1', 'b11'),
        ('b11', 'b111'),
        ('b', 'b2'),
        ('c', 'c1'),
    ]
    result = main(source)
    pprint(result)
    expected = {
        'a': {'a1': {}, 'a2': {'a21': {}, 'a22': {}}},
        'b': {'b1': {'b11': {'b111': {}}}, 'b2': {}},
        'c': {'c1': {}},
    }

    print(result == expected)

