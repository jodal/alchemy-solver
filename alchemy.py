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

    def save_graph(self, element=None):
        if element is None:
            filename = 'solutions/FULL.png'
            graph = self.graph
        else:
            filename = 'solutions/%s.png' % (
                element.replace(' ', '_').replace('!', ''))
            graph = self.get_predecessor_graph(element)
            graph.get_node(element).attr['color'] = 'green'
        graph.draw(filename, prog='dot')
        print '%s generated' % filename
        if element is not None:
            graph.get_node(element).attr['color'] = 'lightblue2'

    def get_predecessor_graph(self, element):
        try:
            child = self.graph.get_node(element)
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
        return self.graph.subgraph(nbunch=nodes)

    def process_command(self, command):
        if command == 'full':
            self.save_graph()
        elif command == 'all':
            self.save_graph()
            for element in self.get_elements():
                self.save_graph(element=element)
        else:
            self.save_graph(element=command)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit('Usage: %s ( full | all | ELEMENT )' % sys.argv[0])

    solution = Solution()
    solution.add_elements('input/en_us.xml')
    solution.add_relations('input/library.xml')
    solution.process_command(sys.argv[1])
