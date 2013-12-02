# -*- coding: utf-8 -*-
# Natural Language Toolkit: Text Trees
#
# Copyright (C) 2001-2012 NLTK Project
# Author: Edward Loper <edloper@gradient.cis.upenn.edu>
#         Steven Bird <sb@csse.unimelb.edu.au>
#         Peter Ljunglöf <peter.ljunglof@gu.se>
#         Nathan Bodenstab <bodenstab@cslu.ogi.edu> (tree transforms)
# URL: <http://www.nltk.org/>
# For license information, see LICENSE.TXT

"""
Class for representing hierarchical language structures, such as
syntax trees and morphological trees.
"""

import re
import string

# from nltk.grammar import Production, Nonterminal
# from nltk.probability import ProbabilisticMixIn
# from nltk.util import slice_bounds

######################################################################
## Trees
######################################################################


class Tree(list):
    """
    A Tree represents a hierarchical grouping of leaves and subtrees.
    For example, each constituent in a syntax tree is represented by a single Tree.

    A tree's children are encoded as a list of leaves and subtrees,
    where a leaf is a basic (non-tree) value; and a subtree is a
    nested Tree.

    #     >>> from nltk.tree import Tree
    #     >>> print Tree(1, [2, Tree(3, [4]), 5])
    #     (1 2 (3 4) 5)
    #     >>> vp = Tree('VP', [Tree('V', ['saw']),
    #     ...                  Tree('NP', ['him'])])
    #     >>> s = Tree('S', [Tree('NP', ['I']), vp])
    #     >>> print s
    #     (S (NP I) (VP (V saw) (NP him)))
    #     >>> print s[1]
    #     (VP (V saw) (NP him))
    #     >>> print s[1,1]
    #     (NP him)
    #     >>> t = Tree("(S (NP I) (VP (V saw) (NP him)))")
    #     >>> s == t
    #     True
    #     >>> t[1][1].node = "X"
    #     >>> print t
    #     (S (NP I) (VP (V saw) (X him)))
    #     >>> t[0], t[1,1] = t[1,1], t[0]
    #     >>> print t
    #     (S (X him) (VP (V saw) (NP I)))
    #
    # The length of a tree is the number of children it has.
    #
    #     >>> len(t)
    #     2

    Any other properties that a Tree defines are known as node
    properties, and are used to add information about individual
    hierarchical groupings.  For example, syntax trees use a NODE
    property to label syntactic constituents with phrase tags, such as
    "NP" and "VP".

    Several Tree methods use "tree positions" to specify
    children or descendants of a tree.  Tree positions are defined as
    follows:

      - The tree position *i* specifies a Tree's *i*\ th child.
      - The tree position ``()`` specifies the Tree itself.
      - If *p* is the tree position of descendant *d*, then
        *p+i* specifies the *i*\ th child of *d*.

    I.e., every tree position is either a single index *i*,
    specifying ``tree[i]``; or a sequence *i1, i2, ..., iN*,
    specifying ``tree[i1][i2]...[iN]``.

    Construct a new tree.  This constructor can be called in one
    of two ways:

    - ``Tree(node, children)`` constructs a new tree with the
        specified node value and list of children.

    - ``Tree(s)`` constructs a new tree by parsing the string ``s``.
        It is equivalent to calling the class method ``Tree.parse(s)``.
    """
    def __init__(self, node_or_str, children=None):
        if children is None: 
            if not isinstance(node_or_str, basestring):
                raise TypeError("%s: Expected a node value and child list "
                                "or a single string" % type(self).__name__)
            tree = type(self).parse(node_or_str)
            list.__init__(self, tree)
            self.node = tree.node
        elif isinstance(children, basestring):
            raise TypeError("%s() argument 2 should be a list, not a "
                            "string" % type(self).__name__)
        else:
            list.__init__(self, children)
            self.node = node_or_str

    #////////////////////////////////////////////////////////////
    # Comparison operators
    #////////////////////////////////////////////////////////////

    def __eq__(self, other):
        if not isinstance(other, Tree): return False
        return self.node == other.node and list.__eq__(self, other)
    def __ne__(self, other):
        return not (self == other)
    def __lt__(self, other):
        if not isinstance(other, Tree): return False
        return self.node < other.node or list.__lt__(self, other)
    def __le__(self, other):
        if not isinstance(other, Tree): return False
        return self.node <= other.node or list.__le__(self, other)
    def __gt__(self, other):
        if not isinstance(other, Tree): return True
        return self.node > other.node or list.__gt__(self, other)
    def __ge__(self, other):
        if not isinstance(other, Tree): return False
        return self.node >= other.node or list.__ge__(self, other)

    #////////////////////////////////////////////////////////////
    # Disabled list operations
    #////////////////////////////////////////////////////////////

    def __mul__(self, v):
        raise TypeError('Tree does not support multiplication')
    def __rmul__(self, v):
        raise TypeError('Tree does not support multiplication')
    def __add__(self, v):
        raise TypeError('Tree does not support addition')
    def __radd__(self, v):
        raise TypeError('Tree does not support addition')

    #////////////////////////////////////////////////////////////
    # Indexing (with support for tree positions)
    #////////////////////////////////////////////////////////////

    def __getitem__(self, index):
        if isinstance(index, (int, slice)):
            return list.__getitem__(self, index)
        elif isinstance(index, (list, tuple)):
            if len(index) == 0:
                return self
            elif len(index) == 1:
                return self[index[0]]
            else:
                return self[index[0]][index[1:]]
        else:
            raise TypeError("%s indices must be integers, not %s" %
                            (type(self).__name__, type(index).__name__))

    def __setitem__(self, index, value):
        if isinstance(index, (int, slice)):
            return list.__setitem__(self, index, value)
        elif isinstance(index, (list, tuple)):
            if len(index) == 0:
                raise IndexError('The tree position () may not be '
                                 'assigned to.')
            elif len(index) == 1:
                self[index[0]] = value
            else:
                self[index[0]][index[1:]] = value
        else:
            raise TypeError("%s indices must be integers, not %s" %
                            (type(self).__name__, type(index).__name__))

    def __delitem__(self, index):
        if isinstance(index, (int, slice)):
            return list.__delitem__(self, index)
        elif isinstance(index, (list, tuple)):
            if len(index) == 0:
                raise IndexError('The tree position () may not be deleted.')
            elif len(index) == 1:
                del self[index[0]]
            else:
                del self[index[0]][index[1:]]
        else:
            raise TypeError("%s indices must be integers, not %s" %
                            (type(self).__name__, type(index).__name__))

    #////////////////////////////////////////////////////////////
    # Basic tree operations
    #////////////////////////////////////////////////////////////

    def leaves(self):
        """
        Return the leaves of the tree.

            >>> t = Tree("(S (NP (D the) (N dog)) (VP (V chased) (NP (D the) (N cat))))")
            >>> t.leaves()
            ['the', 'dog', 'chased', 'the', 'cat']

        :return: a list containing this tree's leaves.
            The order reflects the order of the
            leaves in the tree's hierarchical structure.
        :rtype: list
        """
        leaves = []
        for child in self:
            if isinstance(child, Tree):
                leaves.extend(child.leaves())
            else:
                leaves.append(child)
        return leaves

    def flatten(self):
        """
        Return a flat version of the tree, with all non-root non-terminals removed.

            >>> t = Tree("(S (NP (D the) (N dog)) (VP (V chased) (NP (D the) (N cat))))")
            >>> print t.flatten()
            (S the dog chased the cat)

        :return: a tree consisting of this tree's root connected directly to
            its leaves, omitting all intervening non-terminal nodes.
        :rtype: Tree
        """
        return Tree(self.node, self.leaves())

    def height(self):
        """
        Return the height of the tree.

            >>> t = Tree("(S (NP (D the) (N dog)) (VP (V chased) (NP (D the) (N cat))))")
            >>> t.height()
            5
            >>> print t[0,0]
            (D the)
            >>> t[0,0].height()
            2

        :return: The height of this tree.  The height of a tree
            containing no children is 1; the height of a tree
            containing only leaves is 2; and the height of any other
            tree is one plus the maximum of its children's
            heights.
        :rtype: int
        """
        max_child_height = 0
        for child in self:
            if isinstance(child, Tree):
                max_child_height = max(max_child_height, child.height())
            else:
                max_child_height = max(max_child_height, 1)
        return 1 + max_child_height

    def treepositions(self, order='preorder'):
        """
            >>> t = Tree("(S (NP (D the) (N dog)) (VP (V chased) (NP (D the) (N cat))))")
            >>> t.treepositions() # doctest: +ELLIPSIS
            [(), (0,), (0, 0), (0, 0, 0), (0, 1), (0, 1, 0), (1,), (1, 0), (1, 0, 0), ...]
            >>> for pos in t.treepositions('leaves'):
            ...     t[pos] = t[pos][::-1].upper()
            >>> print t
            (S (NP (D EHT) (N GOD)) (VP (V DESAHC) (NP (D EHT) (N TAC))))

        :param order: One of: ``preorder``, ``postorder``, ``bothorder``,
            ``leaves``.
        """
        positions = []
        if order in ('preorder', 'bothorder'): positions.append( () )
        for i, child in enumerate(self):
            if isinstance(child, Tree):
                childpos = child.treepositions(order)
                positions.extend((i,)+p for p in childpos)
            else:
                positions.append( (i,) )
        if order in ('postorder', 'bothorder'): positions.append( () )
        return positions

    def subtrees(self, filter=None):
        """
        Generate all the subtrees of this tree, optionally restricted
        to trees matching the filter function.

            >>> t = Tree("(S (NP (D the) (N dog)) (VP (V chased) (NP (D the) (N cat))))")
            >>> for s in t.subtrees(lambda t: t.height() == 2):
            ...     print s
            (D the)
            (N dog)
            (V chased)
            (D the)
            (N cat)

        :type filter: function
        :param filter: the function to filter all local trees
        """
        if not filter or filter(self):
            yield self
        for child in self:
            if isinstance(child, Tree):
                for subtree in child.subtrees(filter):
                    yield subtree

    # def productions(self):
    #     """
    #     Generate the productions that correspond to the non-terminal nodes of the tree.
    #     For each subtree of the form (P: C1 C2 ... Cn) this produces a production of the
    #     form P -> C1 C2 ... Cn.
    #
    #         >>> t = Tree("(S (NP (D the) (N dog)) (VP (V chased) (NP (D the) (N cat))))")
    #         >>> t.productions()
    #         [S -> NP VP, NP -> D N, D -> 'the', N -> 'dog', VP -> V NP, V -> 'chased',
    #         NP -> D N, D -> 'the', N -> 'cat']
    #
    #     :rtype: list(Production)
    #     """
    #
    #     if not isinstance(self.node, basestring):
    #         raise TypeError, 'Productions can only be generated from trees having node labels that are strings'
    #
    #     prods = [Production(Nonterminal(self.node), _child_names(self))]
    #     for child in self:
    #         if isinstance(child, Tree):
    #             prods += child.productions()
    #     return prods

    def pos(self):
        """
        Return a sequence of pos-tagged words extracted from the tree.

            >>> t = Tree("(S (NP (D the) (N dog)) (VP (V chased) (NP (D the) (N cat))))")
            >>> t.pos()
            [('the', 'D'), ('dog', 'N'), ('chased', 'V'), ('the', 'D'), ('cat', 'N')]

        :return: a list of tuples containing leaves and pre-terminals (part-of-speech tags).
            The order reflects the order of the leaves in the tree's hierarchical structure.
        :rtype: list(tuple)
        """
        pos = []
        for child in self:
            if isinstance(child, Tree):
                pos.extend(child.pos())
            else:
                pos.append((child, self.node))
        return pos

    def leaf_treeposition(self, index):
        """
        :return: The tree position of the ``index``-th leaf in this
            tree.  I.e., if ``tp=self.leaf_treeposition(i)``, then
            ``self[tp]==self.leaves()[i]``.

        :raise IndexError: If this tree contains fewer than ``index+1``
            leaves, or if ``index<0``.
        """
        if index < 0: raise IndexError('index must be non-negative')

        stack = [(self, ())]
        while stack:
            value, treepos = stack.pop()
            if not isinstance(value, Tree):
                if index == 0: return treepos
                else: index -= 1
            else:
                for i in range(len(value)-1, -1, -1):
                    stack.append( (value[i], treepos+(i,)) )

        raise IndexError('index must be less than or equal to len(self)')

    def treeposition_spanning_leaves(self, start, end):
        """
        :return: The tree position of the lowest descendant of this
            tree that dominates ``self.leaves()[start:end]``.
        :raise ValueError: if ``end <= start``
        """
        if end <= start:
            raise ValueError('end must be greater than start')
        # Find the tree positions of the start & end leaves, and
        # take the longest common subsequence.
        start_treepos = self.leaf_treeposition(start)
        end_treepos = self.leaf_treeposition(end-1)
        # Find the first index where they mismatch:
        for i in range(len(start_treepos)):
            if i == len(end_treepos) or start_treepos[i] != end_treepos[i]:
                return start_treepos[:i]
        return start_treepos

    # #////////////////////////////////////////////////////////////
    # # Transforms
    # #////////////////////////////////////////////////////////////
    #
    # def chomsky_normal_form(self, factor = "right", horzMarkov = None, vertMarkov = 0, childChar = "|", parentChar = "^"):
    #     """
    #     This method can modify a tree in three ways:
    #
    #       1. Convert a tree into its Chomsky Normal Form (CNF)
    #          equivalent -- Every subtree has either two non-terminals
    #          or one terminal as its children.  This process requires
    #          the creation of more"artificial" non-terminal nodes.
    #       2. Markov (vertical) smoothing of children in new artificial
    #          nodes
    #       3. Horizontal (parent) annotation of nodes
    #
    #     :param factor: Right or left factoring method (default = "right")
    #     :type  factor: str = [left|right]
    #     :param horzMarkov: Markov order for sibling smoothing in artificial nodes (None (default) = include all siblings)
    #     :type  horzMarkov: int | None
    #     :param vertMarkov: Markov order for parent smoothing (0 (default) = no vertical annotation)
    #     :type  vertMarkov: int | None
    #     :param childChar: A string used in construction of the artificial nodes, separating the head of the
    #                       original subtree from the child nodes that have yet to be expanded (default = "|")
    #     :type  childChar: str
    #     :param parentChar: A string used to separate the node representation from its vertical annotation
    #     :type  parentChar: str
    #     """
    #     from treetransforms import chomsky_normal_form
    #     chomsky_normal_form(self, factor, horzMarkov, vertMarkov, childChar, parentChar)
    #
    # def un_chomsky_normal_form(self, expandUnary = True, childChar = "|", parentChar = "^", unaryChar = "+"):
    #     """
    #     This method modifies the tree in three ways:
    #
    #       1. Transforms a tree in Chomsky Normal Form back to its
    #          original structure (branching greater than two)
    #       2. Removes any parent annotation (if it exists)
    #       3. (optional) expands unary subtrees (if previously
    #          collapsed with collapseUnary(...) )
    #
    #     :param expandUnary: Flag to expand unary or not (default = True)
    #     :type  expandUnary: bool
    #     :param childChar: A string separating the head node from its children in an artificial node (default = "|")
    #     :type  childChar: str
    #     :param parentChar: A sting separating the node label from its parent annotation (default = "^")
    #     :type  parentChar: str
    #     :param unaryChar: A string joining two non-terminals in a unary production (default = "+")
    #     :type  unaryChar: str
    #     """
    #     from treetransforms import un_chomsky_normal_form
    #     un_chomsky_normal_form(self, expandUnary, childChar, parentChar, unaryChar)
    #
    # def collapse_unary(self, collapsePOS = False, collapseRoot = False, joinChar = "+"):
    #     """
    #     Collapse subtrees with a single child (ie. unary productions)
    #     into a new non-terminal (Tree node) joined by 'joinChar'.
    #     This is useful when working with algorithms that do not allow
    #     unary productions, and completely removing the unary productions
    #     would require loss of useful information.  The Tree is modified
    #     directly (since it is passed by reference) and no value is returned.
    #
    #     :param collapsePOS: 'False' (default) will not collapse the parent of leaf nodes (ie.
    #                         Part-of-Speech tags) since they are always unary productions
    #     :type  collapsePOS: bool
    #     :param collapseRoot: 'False' (default) will not modify the root production
    #                          if it is unary.  For the Penn WSJ treebank corpus, this corresponds
    #                          to the TOP -> productions.
    #     :type collapseRoot: bool
    #     :param joinChar: A string used to connect collapsed node values (default = "+")
    #     :type  joinChar: str
    #     """
    #     from treetransforms import collapse_unary
    #     collapse_unary(self, collapsePOS, collapseRoot, joinChar)
    #
    # #////////////////////////////////////////////////////////////
    # Convert, copy
    #////////////////////////////////////////////////////////////

    @classmethod
    def convert(cls, tree):
        """
        Convert a tree between different subtypes of Tree.  ``cls`` determines
        which class will be used to encode the new tree.

        :type tree: Tree
        :param tree: The tree that should be converted.
        :return: The new Tree.
        """
        if isinstance(tree, Tree):
            children = [cls.convert(child) for child in tree]
            return cls(tree.node, children)
        else:
            return tree

    def copy(self, deep=False):
        if not deep: return type(self)(self.node, self)
        else: return type(self).convert(self)

    #def _frozen_class(self): return ImmutableTree

    def freeze(self, leaf_freezer=None):
        frozen_class = self._frozen_class()
        if leaf_freezer is None:
            newcopy = frozen_class.convert(self)
        else:
            newcopy = self.copy(deep=True)
            for pos in newcopy.treepositions('leaves'):
                newcopy[pos] = leaf_freezer(newcopy[pos])
            newcopy = frozen_class.convert(newcopy)
        hash(newcopy) # Make sure the leaves are hashable.
        return newcopy

    #////////////////////////////////////////////////////////////
    # Parsing
    #////////////////////////////////////////////////////////////

    @classmethod
    def parse(cls, s, brackets='()', parse_node=None, parse_leaf=None,
              node_pattern=None, leaf_pattern=None,
              remove_empty_top_bracketing=False):
        """
        Parse a bracketed tree string and return the resulting tree.
        Trees are represented as nested brackettings, such as::

          (S (NP (NNP John)) (VP (V runs)))

        :type s: str
        :param s: The string to parse

        :type brackets: str (length=2)
        :param brackets: The bracket characters used to mark the
            beginning and end of trees and subtrees.

        :type parse_node: function
        :type parse_leaf: function
        :param parse_node, parse_leaf: If specified, these functions
            are applied to the substrings of ``s`` corresponding to
            nodes and leaves (respectively) to obtain the values for
            those nodes and leaves.  They should have the following
            signature:

               parse_node(str) -> value

            For example, these functions could be used to parse nodes
            and leaves whose values should be some type other than
            string (such as ``FeatStruct``).
            Note that by default, node strings and leaf strings are
            delimited by whitespace and brackets; to override this
            default, use the ``node_pattern`` and ``leaf_pattern``
            arguments.

        :type node_pattern: str
        :type leaf_pattern: str
        :param node_pattern, leaf_pattern: Regular expression patterns
            used to find node and leaf substrings in ``s``.  By
            default, both nodes patterns are defined to match any
            sequence of non-whitespace non-bracket characters.

        :type remove_empty_top_bracketing: bool
        :param remove_empty_top_bracketing: If the resulting tree has
            an empty node label, and is length one, then return its
            single child instead.  This is useful for treebank trees,
            which sometimes contain an extra level of bracketing.

        :return: A tree corresponding to the string representation ``s``.
            If this class method is called using a subclass of Tree,
            then it will return a tree of that type.
        :rtype: Tree
        """
        if not isinstance(brackets, basestring) or len(brackets) != 2:
            raise TypeError('brackets must be a length-2 string')
        if re.search('\s', brackets):
            raise TypeError('whitespace brackets not allowed')
        # Construct a regexp that will tokenize the string.
        open_b, close_b = brackets
        open_pattern, close_pattern = (re.escape(open_b), re.escape(close_b))
        if node_pattern is None:
            node_pattern = '[^\s%s%s]+' % (open_pattern, close_pattern)
        if leaf_pattern is None:
            leaf_pattern = '[^\s%s%s]+' % (open_pattern, close_pattern)
        token_re = re.compile('%s\s*(%s)?|%s|(%s)' % (
            open_pattern, node_pattern, close_pattern, leaf_pattern))
        # Walk through each token, updating a stack of trees.
        stack = [(None, [])] # list of (node, children) tuples
        for match in token_re.finditer(s):
            token = match.group()
            # Beginning of a tree/subtree
            if token[0] == open_b:
                if len(stack) == 1 and len(stack[0][1]) > 0:
                    cls._parse_error(s, match, 'end-of-string')
                node = token[1:].lstrip()
                if parse_node is not None: node = parse_node(node)
                stack.append((node, []))
            # End of a tree/subtree
            elif token == close_b:
                if len(stack) == 1:
                    if len(stack[0][1]) == 0:
                        cls._parse_error(s, match, open_b)
                    else:
                        cls._parse_error(s, match, 'end-of-string')
                node, children = stack.pop()
                stack[-1][1].append(cls(node, children))
            # Leaf node
            else:
                if len(stack) == 1:
                    cls._parse_error(s, match, open_b)
                if parse_leaf is not None: token = parse_leaf(token)
                stack[-1][1].append(token)

        # check that we got exactly one complete tree.
        if len(stack) > 1:
            cls._parse_error(s, 'end-of-string', close_b)
        elif len(stack[0][1]) == 0:
            cls._parse_error(s, 'end-of-string', open_b)
        else:
            assert stack[0][0] is None
            assert len(stack[0][1]) == 1
        tree = stack[0][1][0]

        # If the tree has an extra level with node='', then get rid of
        # it.  E.g.: "((S (NP ...) (VP ...)))"
        if remove_empty_top_bracketing and tree.node == '' and len(tree) == 1:
            tree = tree[0]
        # return the tree.
        return tree

    @classmethod
    def _parse_error(cls, s, match, expecting):
        """
        Display a friendly error message when parsing a tree string fails.
        :param s: The string we're parsing.
        :param match: regexp match of the problem token.
        :param expecting: what we expected to see instead.
        """
        # Construct a basic error message
        if match == 'end-of-string':
            pos, token = len(s), 'end-of-string'
        else:
            pos, token = match.start(), match.group()
        msg = '%s.parse(): expected %r but got %r\n%sat index %d.' % (
            cls.__name__, expecting, token, ' '*12, pos)
        # Add a display showing the error token itsels:
        s = s.replace('\n', ' ').replace('\t', ' ')
        offset = pos
        if len(s) > pos+10:
            s = s[:pos+10]+'...'
        if pos > 10:
            s = '...'+s[pos-10:]
            offset = 13
        msg += '\n%s"%s"\n%s^' % (' '*16, s, ' '*(17+offset))
        raise ValueError(msg)

    #////////////////////////////////////////////////////////////
    # Visualization & String Representation
    #////////////////////////////////////////////////////////////
    #
    # def draw(self):
    #     """
    #     Open a new window containing a graphical diagram of this tree.
    #     """
    #     from nltk.draw.tree import draw_trees
    #     draw_trees(self)

    def __repr__(self):
        childstr = ", ".join(repr(c) for c in self)
        return '%s(%r, [%s])' % (type(self).__name__, self.node, childstr)

    def __str__(self):
        return self.pprint()

    def pprint(self, margin=70, indent=0, nodesep='', parens='()', quotes=False):
        """
        :return: A pretty-printed string representation of this tree.
        :rtype: str
        :param margin: The right margin at which to do line-wrapping.
        :type margin: int
        :param indent: The indentation level at which printing
            begins.  This number is used to decide how far to indent
            subsequent lines.
        :type indent: int
        :param nodesep: A string that is used to separate the node
            from the children.  E.g., the default value ``':'`` gives
            trees like ``(S: (NP: I) (VP: (V: saw) (NP: it)))``.
        """

        # Try writing it on one line.
        s = self._pprint_flat(nodesep, parens, quotes)
        if len(s)+indent < margin:
            return s

        # If it doesn't fit on one line, then write it on multi-lines.
        if isinstance(self.node, basestring):
            s = '%s%s%s' % (parens[0], self.node, nodesep)
        else:
            s = '%s%r%s' % (parens[0], self.node, nodesep)
        for child in self:
            if isinstance(child, Tree):
                s += '\n'+' '*(indent+2)+child.pprint(margin, indent+2,
                                                  nodesep, parens, quotes)
            elif isinstance(child, tuple):
                s += '\n'+' '*(indent+2)+ "/".join(child)
            elif isinstance(child, basestring) and not quotes:
                s += '\n'+' '*(indent+2)+ '%s' % child
            else:
                s += '\n'+' '*(indent+2)+ '%r' % child
        return s+parens[1]

    def pprint_latex_qtree(self):
        r"""
        Returns a representation of the tree compatible with the
        LaTeX qtree package. This consists of the string ``\Tree``
        followed by the parse tree represented in bracketed notation.

        For example, the following result was generated from a parse tree of
        the sentence ``The announcement astounded us``::

          \Tree [.I'' [.N'' [.D The ] [.N' [.N announcement ] ] ]
              [.I' [.V'' [.V' [.V astounded ] [.N'' [.N' [.N us ] ] ] ] ] ] ]

        See http://www.ling.upenn.edu/advice/latex.html for the LaTeX
        style file for the qtree package.

        :return: A latex qtree representation of this tree.
        :rtype: str
        """
        return r'\Tree ' + self.pprint(indent=6, nodesep='', parens=('[.', ' ]'))

    def _pprint_flat(self, nodesep, parens, quotes):
        childstrs = []
        for child in self:
            if isinstance(child, Tree):
                childstrs.append(child._pprint_flat(nodesep, parens, quotes))
            elif isinstance(child, tuple):
                childstrs.append("/".join(child))
            elif isinstance(child, basestring) and not quotes:
                childstrs.append('%s' % child)
            else:
                childstrs.append('%r' % child)
        if isinstance(self.node, basestring):
            return '%s%s%s %s%s' % (parens[0], self.node, nodesep,
                                    string.join(childstrs), parens[1])
        else:
            return '%s%r%s %s%s' % (parens[0], self.node, nodesep,
                                    string.join(childstrs), parens[1])

