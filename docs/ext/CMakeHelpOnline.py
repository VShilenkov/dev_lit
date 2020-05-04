from re import sub
from typing import Any, Dict, List, Tuple, Type
from docutils import nodes
from docutils.nodes import Element, Node, TextElement, system_message
from sphinx import addnodes
from sphinx.util.docutils import ReferenceRole

class CMakeRole(ReferenceRole):
    cmake_help_base_url = "https://cmake.org/cmake/help/latest/"

    def get_entry_name(self) -> str:
        return 'CMAKE_UNKNOWN; CMAKE_UNKNOWN %s'
    
    def get_reference_class(self) -> str:
        return 'cmake_unknown'

    def build_uri(self) -> str:
        return self.cmake_help_base_url

    def build_title(self) -> str:
        return self.title

    def run(self) -> Tuple[List[Node], List[system_message]]:
        target_id = 'index-%s' % self.env.new_serialno('index')
        entries = [('single', self.get_entry_name() % self.target, target_id, '', None)]

        index = addnodes.index(entries=entries)
        target = nodes.target('', '', ids=[target_id])
        self.inliner.document.note_explicit_target(target)

        refuri = self.build_uri()
        reference_class = self.get_reference_class()
        reference = nodes.reference('', '', internal=False, refuri=refuri, classes=['cmake', reference_class])

        title = ''
        if self.has_explicit_title:
            title = self.title
        else:
            title = self.build_title()
        
        reference += nodes.strong(title, title)

        return [index, target, reference], []

class CMakeCommandRole(CMakeRole):
    def get_entry_name(self) -> str:
        return 'CMAKE_COMMAND; CMAKE_COMMAND %s'
    
    def get_reference_class(self) -> str:
        return 'cmake_command'

    def build_uri(self) -> str:
        # list(APPEND)
        # list() command <list>
        # list(APPEND) sub-command <list>
        command_url = self.cmake_help_base_url + "command/"
        command_name = self.target.lower()
        command_name = sub("\(\)", "", command_name)
        return command_url + command_name + ".html#command:" + command_name

    def build_title(self) -> str:
        command_name = sub("\(\)", "", self.title.lower())
        return command_name + '()'

class CMakeVariableRole(CMakeRole):
    def get_entry_name(self) -> str:
        return 'CMAKE_VARIABLE; CMAKE_VARIABLE %s'
    
    def get_reference_class(self) -> str:
        return 'cmake_variable'

    def build_uri(self) -> str:
        variable_url =  self.cmake_help_base_url + "variable/"
        variable_name = self.target.upper()
        return variable_url + variable_name + ".html#variable:" + variable_name

    def build_title(self) -> str:
        return self.title.upper()

class CMakeModuleRole(CMakeRole):
    def get_entry_name(self) -> str:
        return 'CMAKE_MODULE; CMAKE_MODULE %s'
    
    def get_reference_class(self) -> str:
        return 'cmake_module'

    def build_uri(self) -> str:
        module_url =  self.cmake_help_base_url + "module/"
        module_name = self.target
        return module_url + module_name + ".html"

    def build_title(self) -> str:
        return self.title

class CMakePropertyGlobalRole(CMakeRole):
    def get_entry_name(self) -> str:
        return 'CMAKE_PROPERTY_GLOBAL; CMAKE_PROPERTY_GLOBAL %s'
    
    def get_reference_class(self) -> str:
        return 'cmake_property'

    def build_uri(self) -> str:
        property_global_url = self.cmake_help_base_url + "prop_gbl/"
        property_global_name = self.target.upper()
        return property_global_url + property_global_name + ".html#prop_gbl:" + property_global_name

    def build_title(self) -> str:
        return self.title.upper()

class CMakePropertyTargetRole(CMakeRole):
    def get_entry_name(self) -> str:
        return 'CMAKE_PROPERTY_TARGET; CMAKE_PROPERTY_TARGET %s'
    
    def get_reference_class(self) -> str:
        return 'cmake_property'

    def build_uri(self) -> str:
        property_target_url = self.cmake_help_base_url + "prop_tgt/"
        target_property_name = self.target.upper()
        return property_target_url + target_property_name + ".html#prop_tgt:" + target_property_name

    def build_title(self) -> str:
        return self.title.upper()

class CMakeManualRole(CMakeRole):
    def get_entry_name(self) -> str:
        return 'CMAKE_MANUAL; CMAKE_MANUAL %s'
    
    def get_reference_class(self) -> str:
        return 'cmake_manual'

    def build_uri(self) -> str:
        manual_url = self.cmake_help_base_url + "manual/"
        manual_name = self.target.lower()
        return manual_url + manual_name + ".html"

    def build_title(self) -> str:
        title = self.title.lower()
        title = sub(r"\.([0-9])","(\\1)", title)
        return title

custom_docroles = {
    'cmake:command': CMakeCommandRole(),
    #'cpack_gen':  CMakeXRefRole(),
    #'envvar':     CMakeXRefRole(),
    #'generator':  CMakeXRefRole(),
    #'guide':      CMakeXRefRole(),
    'cmake:variable': CMakeVariableRole(),
    'cmake:module': CMakeModuleRole(),
    #'policy':     CMakeXRefRole(),
    #'prop_cache': CMakeXRefRole(),
    #'prop_dir':   CMakeXRefRole(),
    'cmake:prop_gbl': CMakePropertyGlobalRole(),
    #'prop_inst':  CMakeXRefRole(),
    #'prop_sf':    CMakeXRefRole(),
    #'prop_test':  CMakeXRefRole(),
    'cmake:prop_tgt': CMakePropertyTargetRole(),
    'cmake:manual' : CMakeManualRole()
}  # type: Dict[str, RoleFunction]

def setup(app: "Sphinx") -> Dict[str, Any]:
    from docutils.parsers.rst import roles

    for rolename, func in custom_docroles.items():
        roles.register_local_role(rolename, func)

    return {
        'version': '1.0',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }