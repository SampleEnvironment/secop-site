import re

from docutils import nodes

from sphinx import addnodes
from sphinx.domains.python import PyFunction, PyVariable, PyObject, PyClasslike
from sphinx.util.docutils import ReferenceRole
from sphinx.util.nodes import split_explicit_title

REPO_BASE = 'https://github.com/SampleEnvironment/SECoP/blob/master/'


class Property(PyVariable):
    def handle_signature(self, sig, signode):
        fullname, prefix = PyVariable.handle_signature(self, sig, signode)
        signode.insert(0, addnodes.desc_addname('', 'Property',
                                                addnodes.desc_sig_space()))
        if self.name == 'node-property':
            fullname = 'node:' + fullname
        elif self.name == 'mod-property':
            fullname = 'mod:' + fullname
        return fullname, prefix

    def get_index_text(self, modname, name_cls):
        if self.name == 'node-property':
            return '%s (node property)' % name_cls[0]
        elif self.name == 'mod-property':
            return '%s (module property)' % name_cls[0]
        elif self.name == 'acc-property':
            return '%s (accessible property)' % name_cls[0]
        else:
            return '%s (property)' % name_cls[0]


class Parameter(PyVariable):
    def handle_signature(self, sig, signode):
        fullname, prefix = PyVariable.handle_signature(self, sig, signode)
        signode.insert(0, addnodes.desc_addname('', 'Parameter',
                                                addnodes.desc_sig_space()))
        return fullname, prefix

    def get_index_text(self, modname, name_cls):
        return '%s (parameter)' % name_cls[0]


class BaseClass(PyClasslike):
    def get_index_text(self, modname, name_cls):
        return '%s (base class)' % name_cls[0]


class ErrorClass(PyClasslike):
    def get_index_text(self, modname, name_cls):
        return '%s (error class)' % name_cls[0]


class Feature(PyClasslike):
    def get_index_text(self, modname, name_cls):
        return '%s (feature)' % name_cls[0]


class Command(PyFunction):
    def needs_arglist(self):
        return False

    def handle_signature(self, sig, signode):
        fullname, prefix = PyFunction.handle_signature(self, sig, signode)
        signode.insert(0, addnodes.desc_addname('', 'Command',
                                                addnodes.desc_sig_space()))
        return fullname, prefix

    def get_index_text(self, modname, name_cls):
        return '%s (command)' % name_cls[0]

    def add_target_and_index(self, name_cls, sig, signode):
        PyObject.add_target_and_index(self, name_cls, sig, signode)


class Message(PyVariable):
    def handle_signature(self, sig, signode):
        signode['module'] = signode['class'] = None
        m = re.match(r'^\[(.*?)\] ([^ ]+)(?: ([^ ]+)(?: (.+))?)?$', sig)
        if m is None:
            name = sig
            signode += addnodes.desc_name(name, name)
        else:
            reqtype = m.group(1)
            cls = 'danger' if reqtype == 'request' else 'success'
            signode += addnodes.desc_sig_operator(
                reqtype, reqtype,
                classes=['sd-badge', f'sd-bg-{cls}', f'sd-bg-text-{cls}'])
            signode += addnodes.desc_sig_space()
            name = m.group(2)
            signode += addnodes.desc_name(name, name)
            if spec := m.group(3):
                signode += addnodes.desc_sig_space()
                signode += addnodes.desc_sig_literal_string(spec, spec)
            if data := m.group(4):
                signode += addnodes.desc_sig_space()
                signode += addnodes.desc_sig_literal_string(data, data)
        signode['fullname'] = name
        return name, ''

    def get_index_text(self, modname, name_cls):
        return '%s (protocol message)' % name_cls[0]


class SecopRFC(ReferenceRole):
    def run(self):
        target_id = 'index-%s' % self.env.new_serialno('index')
        entries = [('single', 'SECoP RFC; RFC %s' % self.target,
                    target_id, '', None)]

        index = addnodes.index(entries=entries)
        target = nodes.target('', '', ids=[target_id])
        self.inliner.document.note_explicit_target(target)

        refuri = REPO_BASE + f'rfcs/RFC-{self.target}.rst'
        reference = nodes.reference('', '', internal=False, refuri=refuri)
        if self.has_explicit_title:
            reference += nodes.strong(self.title, self.title)
        else:
            num = self.target.split('-')[0]
            title = f'SECoP RFC {num}'
            reference += nodes.strong(title, title)
        return [index, target, reference], []


def setup(app):
    app.add_directive('node-property', Property)
    app.add_directive('mod-property', Property)
    app.add_directive('acc-property', Property)
    app.add_directive('other-property', Property)
    app.add_directive('parameter', Parameter)
    app.add_directive('command', Command)
    app.add_directive('baseclass', BaseClass)
    app.add_directive('feature', Feature)
    app.add_directive('message', Message)
    app.add_directive('errorclass', ErrorClass)
    app.add_role('secop-rfc', SecopRFC())
    return {'parallel_read_safe': True, 'version': '0.1.0'}
