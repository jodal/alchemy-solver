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

    def process_command(self, argv):
        command = argv[1]
        if command == '--list':
            basic = ['water', 'fire', 'earth', 'air']
            derived = sorted(self.elements)
            for element in basic:
                derived.remove(element)
            for element in basic + derived:
                print element
        elif command == '--full':
            self.save_full_graph()
        elif command == '--all':
            self.save_full_graph()
            for element in self.elements:
                self.save_element_graph(element)
                self.save_derived_element_graph(element)
                self.save_deriving_element_graph(element)
        elif command == '--from':
            self.save_derived_element_graph(argv[2])
        elif command == '--to':
            self.save_derived_element_graph(argv[2])
        else:
            self.save_element_graph(command)

    def save_full_graph(self):
        self._save_graph(self.graph, 'solutions/FULL.png')

    def _process_graph(self, prefix, element, graph):
        filename = 'solutions/%s%s.png' % (
            prefix, element.replace(' ', '_').replace('!', ''))
        graph.get_node(element).attr['color'] = 'green'
        self._save_graph(graph, filename)
        graph.get_node(element).attr['color'] = 'lightblue2'

    def save_element_graph(self, element):
        graph = self._get_predecessor_graph(element)
        self._process_graph('', element, graph)

    def save_derived_element_graph(self, element):
        graph = self._get_successor_graph(element)
        self._process_graph('from_', element, graph)

    def save_deriving_element_graph(self, element):
        graph = self._get_immediate_predecessor_graph(element)
        self._process_graph('to_', element, graph)

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

    def _get_successor_graph(self, element):
        try:
            target = self.graph.get_node(element)
        except KeyError:
            sys.exit('Element "%s" not found' % element)
        nodes = [target]
        nodes_to_visit = self.graph.successors(target)
        nodes.extend(nodes_to_visit)
        for product in nodes_to_visit:
            nodes.extend(self.graph.predecessors(product))
            nodes.extend(self.graph.successors(product))
        return self.graph.subgraph(nbunch=nodes)

    def _get_immediate_predecessor_graph(self, element):
        try:
            target = self.graph.get_node(element)
        except KeyError:
            sys.exit('Element "%s" not found' % element)
        nodes = [target]
        parents = self.graph.predecessors(target)
        grandparents = []
        for combo in parents:
            grandparents.extend(self.graph.predecessors(combo))
        nodes.extend(parents)
        nodes.extend(grandparents)
        return self.graph.subgraph(nbunch=nodes)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit('Usage: %s [ --list | --full | --all | --from ELEMENT | --to ELEMENT | ELEMENT ]' % sys.argv[0])

    solution = Solution()
    solution.add_elements('input/en_us.xml')
    solution.add_relations('input/library.xml')
    solution.process_command(sys.argv)
