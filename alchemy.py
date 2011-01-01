#! /usr/bin/env python

from lxml.etree import fromstring
import pygraphviz
import sys

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

    def get_elements(self):
        return self.id_to_name.values()

    def save_graph(self, filename, child=None):
        if child is None:
            graph = self.graph
        else:
            try:
                child = self.graph.get_node(child)
            except KeyError:
                sys.exit('Element "%s" not found' % child)
            nodes = []
            nodes_to_visit = [child]
            while nodes_to_visit:
                child = nodes_to_visit.pop(0)
                if child in nodes:
                    continue
                nodes.append(child)
                nodes_to_visit.extend(self.graph.predecessors(child))
            graph = self.graph.subgraph(nbunch=nodes)
        graph.draw(filename, prog='dot')
        print '%s generated' % filename

if __name__ == '__main__':
    solution = Solution()
    solution.add_elements('en_us.xml')
    solution.add_relations('library.xml')

    if len(sys.argv) == 2 and sys.argv[1] == 'full':
        solution.save_graph('full_solution.png')
    elif len(sys.argv) == 2 and sys.argv[1] == 'all':
        solution.save_graph('full_solution.png')
        for element in solution.get_elements():
            solution.save_graph('%s_solution.png' % element, child=element)
    elif len(sys.argv) == 2:
        element = sys.argv[1]
        solution.save_graph('%s_solution.png' % element, child=element)
    else:
        print 'Usage: %s ( full | all | ELEMENT )' % sys.argv[0]
