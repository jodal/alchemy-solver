#! /usr/bin/env python

from lxml.etree import fromstring
import pygraphviz
import sys

class AlchemySolver(object):
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

    def process_command(self, command, element=None):
        if command == '--list':
            return '\n'.join(self._get_element_list())
        elif command == '--game':
            return self._save_game_graph()
        elif command in ('--full', '--from', '--to'):
            if element is None:
                sys.exit('Error: Missing element name or "all"\n%s' % (
                    get_usage()))
            elif element not in self.elements + ['all']:
                sys.exit('Error: Unknown element name "%s"\n%s' % (
                    element, get_usage()))
            elif command == '--full':
                return '\n'.join(self._save_full_element_graph(element))
            elif command == '--from':
                return '\n'.join(self._save_derived_element_graph(element))
            elif command == '--to':
                return '\n'.join(self._save_deriving_element_graph(element))
        else:
            sys.exit('Error: Unknown command "%s"\n%s' % (
                command, get_usage()))

    def _get_element_list(self):
        basic = ['water', 'fire', 'earth', 'air']
        derived = sorted(self.elements)
        for element in basic:
            derived.remove(element)
        return basic + derived

    def _save_game_graph(self):
        return self._save_graph(self.graph, 'solutions/game.png')

    def _get_elements(self, element):
        if element == 'all':
            return self.elements
        else:
            return [element]

    def _save_full_element_graph(self, element):
        for element in self._get_elements(element):
            graph = self._get_predecessor_graph(element)
            yield self._process_graph('full_', element, graph)

    def _save_derived_element_graph(self, element):
        for element in self._get_elements(element):
            graph = self._get_successor_graph(element)
            yield self._process_graph('from_', element, graph)

    def _save_deriving_element_graph(self, element):
        for element in self._get_elements(element):
            graph = self._get_immediate_predecessor_graph(element)
            yield self._process_graph('to_', element, graph)

    def _process_graph(self, prefix, element, graph):
        filename = 'solutions/%s%s.png' % (
            prefix, element.replace(' ', '_').replace('!', ''))
        graph.get_node(element).attr['color'] = 'green'
        result = self._save_graph(graph, filename)
        graph.get_node(element).attr['color'] = 'lightblue2'
        return result

    def _save_graph(self, graph, filename):
        graph.draw(filename, prog='dot')
        return '%s generated' % filename

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

def get_usage():
    return """
Usage:
    %(c)s ( --list | --game )
    %(c)s ( --full | --from | --to ) ( ELEMENT | all )
    """.strip() % {'c': sys.argv[0]}

if __name__ == '__main__':
    if len(sys.argv) not in (2, 3):
        sys.exit(get_usage())

    alchemy_solver = AlchemySolver()
    alchemy_solver.add_elements('input/en_us.xml')
    alchemy_solver.add_relations('input/library.xml')
    print alchemy_solver.process_command(*sys.argv[1:3])
