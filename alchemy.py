#! /usr/bin/env python

from lxml.etree import fromstring
import pygraphviz

class Solution(object):
    def __init__(self):
        self.graph = pygraphviz.AGraph(directed=True)
        self.id_to_name = {}

    def add_elements(self, filename):
        with open(filename) as filehandle:
            xml = filehandle.read()
        for entry in fromstring(xml).xpath('//entry'):
            self.graph.add_node(entry.text,
                color='lightblue2', style='filled')
            self.id_to_name[entry.attrib['id']] = entry.text

    def add_relations(self, filename):
        with open(filename) as filehandle:
            xml = filehandle.read()
        for entry in fromstring(xml).xpath('//entry'):
            child = self.id_to_name[entry.attrib['id']]
            for parents in entry.findall('parents'):
                parents = [self.id_to_name[p.attrib['id']] for p in parents]
                combination = ' + '.join(parents)
                for parent in parents:
                    self.graph.add_edge(parent, combination)
                self.graph.add_edge(combination, child)

    def save_graph(self, filename):
        self.graph.draw(filename, prog='dot')

if __name__ == '__main__':
    solution = Solution()
    solution.add_elements('en_us.xml')
    solution.add_relations('library.xml')
    solution.save_graph('full_solution.png')
