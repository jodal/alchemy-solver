#! /usr/bin/env python

from lxml.etree import fromstring

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

def print_as_digraph(elements):
    print 'digraph G {'
    for element in elements.values():
        for (a, b) in element.made_of:
            print '  "%s + %s" [color=lightblue2, style=filled];' % (a, b)
            print '  "%s" -> "%s + %s";' % (a, a, b)
            print '  "%s" -> "%s + %s";' % (b, a, b)
            print '  "%s + %s" -> "%s";' % (a, b, element)
    print '}'

if __name__ == '__main__':
    elements = get_elements()
    add_relations(elements)
    print_as_digraph(elements)
