#! /usr/bin/env python

from lxml.etree import fromstring
import pygraphviz

class Element(object):
    def __init__(self, name):
        self.name = name
        self.made_of = []
        self.part_of = []

    def __str__(self):
        return self.name

    def add_parents(self, a, b):
        self.made_of.append((a, b))
        a.part_of.append(self)
        b.part_of.append(self)

    def get_part_of_pairs(self):
        result = []
        for child in self.part_of:
            for parents in child.made_of:
                if self in parents:
                    result.append((parents, child))
        return result

def get_elements():
    with open('en_us.xml') as f:
        elements = {}
        for e in fromstring(f.read()).xpath('//entry'):
            elements[e.attrib['id']] = Element(e.text)
        return elements

def add_relations(elements):
    with open('library.xml') as f:
        entries = fromstring(f.read()).xpath('//entry')
        for entry in entries:
            element = elements[entry.attrib['id']]
            for parents in entry.findall('parents'):
                pair = []
                for parent in parents.findall('parent'):
                    pair.append(elements[parent.attrib['id']])
                element.add_parents(*pair)

def get_full_solution_as_digraph(elements):
    graph = pygraphviz.AGraph(name='full_solution', directed=True)
    graph.add_nodes_from([e.name for e in elements.values()],
        color='lightblue2', style='filled')
    for product in elements.values():
        for (factor_a, factor_b) in product.made_of:
            combination = '%s + %s' % (factor_a, factor_b)
            graph.add_edge(factor_a, combination)
            graph.add_edge(factor_b, combination)
            graph.add_edge(combination, product)
    return graph

if __name__ == '__main__':
    elements = get_elements()
    add_relations(elements)
    print get_full_solution_as_digraph(elements).to_string()
