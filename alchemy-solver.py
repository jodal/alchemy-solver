#! /usr/bin/env python

from lxml.etree import fromstring
import pygraphviz
import sys

class Solution(object):
    def __init__(self):
        self.graph = pygraphviz.AGraph(directed=True)
        self.id_to_name = {}

    @property
    def elements(self):
        return self.id_to_name.values()

    def add_elements(self, filename):
        for entry in self._get_xml(filename).xpath('//entry'):
            self.graph.add_node(entry.text,
                color='lightblue2', style='filled')
            self.id_to_name[entry.attrib['id']] = entry.text

    def add_relations(self, filename):
        for entry in self._get_xml(filename).xpath('//entry'):
            child = self.id_to_name[entry.attrib['id']]
            for parents in entry.findall('parents'):
                parents = [self.id_to_name[p.attrib['id']] for p in parents]
                combination = ' + '.join(parents)
                for parent in parents:
                    self.graph.add_edge(parent, combination)
                self.graph.add_edge(combination, child)

    def _get_xml(self, filename):
        with open(filename) as filehandle:
            return fromstring(filehandle.read())

    def process_command(self, command):
        if command == '--full':
            self.save_full_graph()
        elif command == '--all':
            self.save_full_graph()
            for element in self.elements:
                self.save_element_graph(element)
        else:
            self.save_element_graph(command)

    def save_full_graph(self):
        self._save_graph(self.graph, 'solutions/FULL.png')

    def save_element_graph(self, element):
        filename = 'solutions/%s.png' % (
            element.replace(' ', '_').replace('!', ''))
        graph = self._get_predecessor_graph(element)
        graph.get_node(element).attr['color'] = 'green'
        self._save_graph(graph, filename)
        graph.get_node(element).attr['color'] = 'lightblue2'

    def _save_graph(self, graph, filename):
        graph.draw(filename, prog='dot')
        print '%s generated' % filename

    def _get_predecessor_graph(self, element):
        try:
            child = self.graph.get_node(element)
        except KeyError:
            sys.exit('Element "%s" not found' % element)
        nodes = []
        nodes_to_visit = [child]
        while nodes_to_visit:
            child = nodes_to_visit.pop(0)
            if child in nodes:
                continue
            nodes.append(child)
            nodes_to_visit.extend(self.graph.predecessors(child))
        return self.graph.subgraph(nbunch=nodes)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit('Usage: %s ( --full | --all | ELEMENT )' % sys.argv[0])

    solution = Solution()
    solution.add_elements('input/en_us.xml')
    solution.add_relations('input/library.xml')
    solution.process_command(sys.argv[1])