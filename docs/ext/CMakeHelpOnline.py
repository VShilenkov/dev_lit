from re import sub
from typing import Any, Dict, List, Tuple, Type
from docutils import nodes
from docutils.nodes import Element, Node, TextElement, system_message
from requests.utils import requote_uri
from sphinx import addnodes
from sphinx.util.docutils import ReferenceRole

class CMakeRole(ReferenceRole):
    cmake_help_base_url = "https://cmake.org/cmake/help/latest/"

    def get_entry_name(self) -> str:
        target_components = self.target.split()
        return '[CMake]; %s' % target_components[0]

    def get_reference_class(self) -> List[str]:
        return ['cmake_unknown']

    def build_uri(self) -> str:
        return self.cmake_help_base_url

    def build_title(self) -> str:
        return self.title

    def run(self) -> Tuple[List[Node], List[system_message]]:
        target_id = 'index-%s' % self.env.new_serialno('index')
        
        entries = [('single', self.get_entry_name(), target_id, '', None)]

        index = addnodes.index(entries=entries)
        target = nodes.target('', '', ids=[target_id])
        self.inliner.document.note_explicit_target(target)

        refuri = self.build_uri()
        reference_class = self.get_reference_class()
        reference = nodes.reference('', '', internal=False, 
                                    refuri=refuri, 
                                    classes=['cmake'] + reference_class)

        title = ''
        if self.has_explicit_title:
            title = self.title
        else:
            title = self.build_title()
        
        reference += nodes.strong(title, title)

        return [index, target, reference], []

class CMakeCommandRole(CMakeRole):
    def get_entry_name(self) -> str:
        command_name = sub("(\w]+)\(.*", "\\1", self.target.lower())
        return 'Command [CMake]; %s' % command_name
    
    def get_reference_class(self) -> List[str]:
        return ['cmake_command']

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

class CMakeVariableEnvironmentRole(CMakeRole):
    def get_entry_name(self) -> str:
        return 'Environment variable [CMake]; %s' % self.target.upper()
    
    def get_reference_class(self) -> List[str]:
        return ['cmake_env_variable']

    def build_uri(self) -> str:
        variable_environment_url = self.cmake_help_base_url + "envvar/"
        variable_environment_name = self.target.upper()
        return variable_environment_url + variable_environment_name + ".html"

    def build_title(self) -> str:
        return self.title.upper()


class CMakeGeneratorRole(CMakeRole):
    def get_entry_name(self) -> str:
        return 'Generator [CMake]; %s' % self.target
    
    def get_reference_class(self) -> List[str]:
        return ['cmake_generator']

    def build_uri(self) -> str:
        generator_url =  self.cmake_help_base_url + "generator/"
        generator_name = requote_uri(self.target)
        return generator_url + generator_name + ".html#generator:" + generator_name

    def build_title(self) -> str:
        return self.title

class CMakeVariableRole(CMakeRole):
    def get_entry_name(self) -> str:
        return 'Variable [CMake]; %s' % self.target.upper()
    
    def get_reference_class(self) -> List[str]:
        return ['cmake_variable']

    def build_uri(self) -> str:
        variable_url =  self.cmake_help_base_url + "variable/"
        variable_name = self.target.upper()
        return variable_url + variable_name + ".html#variable:" + variable_name

    def build_title(self) -> str:
        return self.title.upper()

class CMakeModuleRole(CMakeRole):
    def get_entry_name(self) -> str:
        return 'Module [CMake]; %s' % self.target
    
    def get_reference_class(self) -> List[str]:
        return ['cmake_module']

    def build_uri(self) -> str:
        module_url =  self.cmake_help_base_url + "module/"
        module_name = self.target
        return module_url + module_name + ".html"

    def build_title(self) -> str:
        return self.title

class CMakePropertyGlobalRole(CMakeRole):
    def get_entry_name(self) -> str:
        return 'Property/Global [CMake]; %s' % self.target.upper()
    
    def get_reference_class(self) -> List[str]:
        return ['cmake_property']

    def build_uri(self) -> str:
        property_global_url = self.cmake_help_base_url + "prop_gbl/"
        property_global_name = self.target.upper()
        return property_global_url + property_global_name + ".html#prop_gbl:" + property_global_name

    def build_title(self) -> str:
        return self.title.upper()

class CMakePropertySourceFileRole(CMakeRole):
    def get_entry_name(self) -> str:
        return 'Property/Source File [CMake]; %s' % self.target.upper()
    
    def get_reference_class(self) -> List[str]:
        return ['cmake_property_source_file']

    def build_uri(self) -> str:
        property_source_file_url = self.cmake_help_base_url + "prop_sf/"
        property_source_file_name = self.target.upper()
        return property_source_file_url + property_source_file_name + ".html#prop_sf:" + property_source_file_name

    def build_title(self) -> str:
        return self.title.upper()


class CMakePropertyTargetRole(CMakeRole):
    def get_entry_name(self) -> str:
        return 'Property/Target [CMake]; %s' % self.target.upper()
    
    def get_reference_class(self) -> List[str]:
        return ['cmake_property']

    def build_uri(self) -> str:
        property_target_url = self.cmake_help_base_url + "prop_tgt/"
        target_property_name = self.target.upper()
        target_property_name_escaped = target_property_name.replace(r"""_<CONFIG>""", '_CONFIG')
        return property_target_url + target_property_name_escaped + ".html#prop_tgt:" + target_property_name

    def build_title(self) -> str:
        title = self.title.upper()
        return title

class CMakeManualRole(CMakeRole):
    def manual_name(self) -> str:
        return sub(r"([a-zA-Z0-9_-]+)\.([0-9])","\\1", self.target.split()[0].lower())

    def manual_section(self) -> str:
        return sub(r"([a-zA-Z0-9_-]+)\.([0-9])","\\2", self.target.split()[0].lower())

    def get_entry_name(self) -> str:
        return 'Manual [CMake]; %s(%s)' % (self.manual_name(), self.manual_section())

    def get_reference_class(self) -> List[str]:
        return ['cmake_manual']

    def build_uri(self) -> str:
        manual_url = self.cmake_help_base_url + "manual/"
        target = self.target.split()
        uri = manual_url + target[0].lower() + ".html"
        if len(target) > 1:
            uri += "#" + target[1]
        return uri

    def build_title(self) -> str:
        return '%s(%s)' % (self.manual_name(), self.manual_section())

class CMakeReleaseRole(CMakeRole):
    def get_entry_name(self) -> str:
        return 'Release [CMake]; %s' % self.target.split()[0]
    
    def get_reference_class(self) -> List[str]:
        return ['cmake_release']

    def build_uri(self) -> str:
        release_url = self.cmake_help_base_url + "release/"
        return release_url + self.target.split()[0] + ".html"

    def build_title(self) -> str:
        title = self.title
        title = title.split()
        if len(title) == 1:
            return 'CMake.' + title[0]
        else:
            if title[1] == '<':
                return "CMake." + title[0] + "-"
            elif title[1] == '>':
                return "CMake." + title[0] + "+"


custom_docroles = {
    'cmake:command': CMakeCommandRole(),
    #'cpack_gen':  CMakeXRefRole(),
    'cmake:variable:env': CMakeVariableEnvironmentRole(),
    'cmake:generator':  CMakeGeneratorRole(),
    #'guide':      CMakeXRefRole(),
    'cmake:variable': CMakeVariableRole(),
    'cmake:module': CMakeModuleRole(),
    #'policy':     CMakeXRefRole(),
    #'prop_cache': CMakeXRefRole(),
    #'prop_dir':   CMakeXRefRole(),
    'cmake:prop_gbl': CMakePropertyGlobalRole(),
    #'prop_inst':  CMakeXRefRole(),
    'cmake:prop_sf':    CMakePropertySourceFileRole(),
    #'prop_test':  CMakeXRefRole(),
    'cmake:prop_tgt': CMakePropertyTargetRole(),
    'cmake:manual': CMakeManualRole(),
    'cmake:release': CMakeReleaseRole()
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
