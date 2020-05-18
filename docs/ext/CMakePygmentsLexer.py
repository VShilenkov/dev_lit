import os
import re
from typing import Any, Dict

# Override much of pygments' CMakeLexer.
# We need to parse CMake syntax definitions, not CMake code.

# For hard test cases that use much of the syntax below, see
# - module/FindPkgConfig.html (with "glib-2.0>=2.10 gtk+-2.0" and similar)
# - module/ExternalProject.html (with http:// https:// git@; also has command options -E --build)
# - manual/cmake-buildsystem.7.html (with nested $<..>; relative and absolute paths, "::")

from pygments.lexers import CMakeLexer
from pygments.token import Name, Operator, Punctuation, String, Text, Comment,\
                           Generic, Whitespace, Number, Keyword, Literal
from pygments.lexer import bygroups, include, RegexLexer
from sphinx.highlighting import lexers

# Notes on regular expressions below:
# - [\.\+-] are needed for string constants like gtk+-2.0
# - Unix paths are recognized by '/'; support for Windows paths may be added if needed
# - (\\.) allows for \-escapes (used in manual/cmake-language.7)
# - $<..$<..$>..> nested occurrence in cmake-buildsystem
# - Nested variable evaluations are only supported in a limited capacity. Only
#   one level of nesting is supported and at most one nested variable can be present.

CMakeLexer.tokens["root"] = [
  (r'\b(\w+)([ \t]*)(\()', bygroups(Name.Function, Text, Name.Function), '#push'),     # fctn(
  (r'\(', Name.Function, '#push'),
  (r'\)', Name.Function, '#pop'),
  (r'\[', Punctuation, '#push'),
  (r'\]', Punctuation, '#pop'),
  (r'[|;,.=*\-]', Punctuation),
  (r'\\\\', Punctuation),                                   # used in commands/source_group
  (r'[:]', Operator),
  (r'[<>]=', Punctuation),                                  # used in FindPkgConfig.cmake
  (r'\$<', Operator, '#push'),                              # $<...>
  (r'<[^<|]+?>(\w*\.\.\.)?', Name.Variable),                # <expr>
  (r'(\$\w*\{)([^\}\$]*)?(?:(\$\w*\{)([^\}]+?)(\}))?([^\}]*?)(\})',  # ${..} $ENV{..}, possibly nested
    bygroups(Operator, Name.Tag, Operator, Name.Tag, Operator, Name.Tag, Operator)),
  (r'([A-Z]+\{)(.+?)(\})', bygroups(Operator, Name.Tag, Operator)),  # DATA{ ...}
  (r'[a-z]+(@|(://))((\\.)|[\w.+-:/\\])+', Name.Attribute),          # URL, git@, ...
  (r'/\w[\w\.\+-/\\]*', Name.Attribute),                    # absolute path
  (r'/', Name.Attribute),
  (r'\w[\w\.\+-]*/[\w.+-/\\]*', Name.Attribute),            # relative path
  (r'[A-Z]((\\.)|[\w.+-])*[a-z]((\\.)|[\w.+-])*', Name.Builtin), # initial A-Z, contains a-z
  (r'@?[A-Z][A-Z0-9_]*', Name.Constant),
  (r'[a-z_]((\\;)|(\\ )|[\w.+-])*', Name.Builtin),
  (r'[0-9][0-9\.]*', Number),
  (r'(?s)"(\\"|[^"])*"', String),                           # "string"
  (r'\.\.\.', Name.Variable),
  (r'<', Operator, '#push'),                                # <..|..> is different from <expr>
  (r'>', Operator, '#pop'),
  (r'\n', Whitespace),
  (r'[ \t]+', Whitespace),
  (r'#.*\n', Comment),
  #  (r'[^<>\])\}\|$"# \t\n]+', Name.Exception),            # fallback, for debugging only
]

class CMakeCodeLexer(RegexLexer):
    name = 'CMakeCode'
    aliases = ['cmake_code']

    tokens = {
        'root': [
            include('bracket_comment'),
            include('line_comment'),
            include('command_invocation'),
            include('new_line'),
            include('space')
        ],
        'bracket_comment': [
            (r'(?s)(#\[(=*)\[.*?\]\2\])', bygroups(Comment.Multiline, None))
        ],
        'line_comment': [
            (r'#.*\n', Comment.Single)
        ],
        'space': [
            (r'[ \t]+', Whitespace)
        ],
        'new_line': [
            (r'\n', Whitespace)
        ],
        'escape_sequence': [
            (r'\\([^A-Za-z0-9]|[trn])', String.Escape)
        ],
        'command_invocation' :[
            (r"""(?ix)([ \t]*)(
                break|cmake_host_system_information|cmake_minimum_required
                |cmake_parse_arguments|cmake_policy|configure_file|continue
                |else|elseif|endforeach|endfunction|endif|endmacro|endwhile
                |execute_process|file|find_file|find_library|find_package
                |find_path|find_programforeach|function|get_cmake_property
                |get_directory_property|get_filename_component|get_property
                |if|include|include_guard|list|macro|mark_as_advanced
                |math|message|option|return|separate_arguments|set
                |set_directory_properties|set_property|site_name
                |string|unset|variable_watch|while|add_compile_definitions
                |add_compile_options|add_custom_command|add_custom_target
                |add_definitions|add_dependencies|add_executable|add_library
                |add_link_options|add_subdirectory|add_test|aux_source_directory
                |build_command|create_test_sourcelist|define_property
                |enable_language|enable_testing|export|fltk_wrap_ui
                |get_source_file_property|get_target_property|get_test_property
                |include_directories|include_external_msproject
                |include_regular_expression|install|link_directories
                |link_libraries|load_cache|project|remove_definitions
                |set_source_files_properties|set_target_properties
                |set_tests_properties|source_group|target_compile_definitions
                |target_compile_features|target_compile_options
                |target_include_directories|target_link_directories
                |target_link_libraries|target_link_options
                |target_precompile_headers|target_sources|try_compile|try_run
                |build_name|exec_program|export_library_dependencies
                |install_files|install_programs|install_targets|load_command
                |make_directory|output_required_files|qt_wrap_cpp|qt_wrap_ui
                |remove|subdir_depends|subdirs|use_mangled_mesa|utility_source
                |variable_requires|write_file)([ \t]*)(\()""", bygroups(Whitespace,
                                                         Name.Function.Magic, Whitespace, Punctuation), 'argument_list'),
            (r'([ \t]*)([A-Za-z_][A-Za-z0-9_]*)([ \t]*)(\()', bygroups(Whitespace,
                                            Name.Function, Whitespace, Punctuation), 'argument_list')
        ],
        'argument_list' :[
            include('bracket_comment'),
            include('line_comment'),
            include('bracket_argument'),
            include('generator_convenience'),
            include('quoted_argument'),
            include('unquoted_argument'),
            include('new_line'),
            include('space'),
            (r'\)', Punctuation, '#pop'),
        ],
        'bracket_argument': [
            (r'(?s)(\[(=*)\[)(.*?)(\](\2)\])',
             bygroups(Punctuation, None, String.Backtick, Punctuation, None)),
        ],
        'generator_convenience': [
            (r'\$<', Operator, 'ge_operator'),
        ],
        'ge_operator': [
            (r'\$<', Operator, '#push'),
            (r'[^:,> ]+', Operator.Word),
            (r'\:', Operator, 'ge_argument'),
            (r'>', Operator, '#pop')
        ],
        'ge_argument': [
            include('generator_convenience'),
            include('quoted_argument'),
            include('unquoted_primitives'),
            (r'[^,>]', Text),
            (r',', Operator),
            (r'>', Operator, '#pop:2')
        ],
        'variable_convenience': [
            (r'\b(WIN32|UNIX)\b', Name.Variable),
            (r'(\$)((?:ENV|CACHE)?)(\{)', bygroups(
                Punctuation, Name.Class, Punctuation), 'variable_name'),
        ],
        'variable_name': [
            include('variable_convenience'),
            (r'[a-zA-Z0-9/_.+-]', Name.Variable),
            (r'\}', Punctuation, '#pop')
        ],
        'quoted_argument': [
            (r'"', String.Double, 'quoted_element')
        ],
        'quoted_element': [
            include('unquoted_primitives'),
            (r'(?s)(\\\"|[^\"])', String.Double),
            (r'\"', String.Double, '#pop'),
        ],
        'paths': [
            (r'(?:(~?\/)([\w.+-/\\]*))|(?:((?:\\\\\?\\)?[a-zA-Z]+\:)(?:[\\\/]([\w.+-/\\]*)))', Name.Attribute),
            (r'\w[\w\.\+-]*/[\w.+-/\\]*', Name.Attribute),
            (r'\s\.\.?\s', Name.Attribute),
            (r'(?<=[\\\/])\*', Name.Attribute),
            (r"""(?x)(\b\w[\w\-\+\.]*|(?<=[>}\*])|\*)\.(cpp|hpp|tar|txt|in|sh
            |png|gz|h)\b""", Name.Attribute),
        ],
        'numbers': [
            (r'\b[0-9][0-9\.]*\b', Number),
        ],
        'options': [
            (r'(?<!\w|\\)-([A-Za-z0-9][A-Za-z0-9-_]*|-[A-Za-z0-9-_]+)', Keyword.Type),
            #(r'(?<!\w)/([A-Za-z0-9][A-Za-z0-9-_\+\:\;]*)', Keyword.Type) windows command options
        ],
        'literals' : [
            (r'\b[A-Z][A-Z0-9_]*\b', Keyword.Declaration),  # uppercase
            (r'[a-z_]((\\;)|(\\ )|[\w.+-])*', Literal), # lowercase
            (r'[A-Z]((\\.)|[\w.+-])*[a-z]((\\.)|[\w.+-])*', Literal), #initial Capital
            (r'(::?|=)', Operator),
        ],
        'unquoted_primitives' : [
            include('variable_convenience'),
            include('escape_sequence'),
            include('paths'),
            include('numbers'),
            include('options'),
        ],
        'unquoted_argument' : [
            include('keywords'),
            include('keyword_constants'),
            include('unquoted_primitives'),
            include('literals')
        ],
        'keyword_constants' :
        [
            (r"""(?ix)\b(On|Off|True|False|SHA1|OWNER_READ|OWNER_WRITE
                        |OWNER_EXECUTE|GROUP_READ|GROUP_WRITE|GROUP_EXECUTE
                        |WORLD_READ|WORLD_WRITE|WORLD_EXECUTE|SETUID|SETGID)\b""", Keyword.Constant),
            
        ],
        'keywords' : [
            (r"""(?x) \b(PUBLIC|PRIVATE|INTERFACE|COMMAND|TARGET|PROPERTY|SHARED
                |IMPORTED|PROPERTIES|UNKNOWN|OBJECT|STATIC|ALIAS|REQUIRED
                |POST_BUILD|BYPRODUCTS|WORKING_DIRECTORY|DEPENDS|OUTPUT
                |MAIN_DEPENDENCY|RESULT_VARIABLE|FATAL_ERROR|NOT|OUTPUT_VARIABLE
                |REGEX|MATCH|DIRECTORY|PATH|NAME|NAME_WE|EXT|RELATIVE_PATH
                |ESCAPE_QUOTES|COPY|DESTINATION|WRITE|FILE_PERMISSIONS
                |FILES_MATCHING|EXCLUDE|PATTERN|PERMISSIONS|APPEND|GENERATE
                |INPUT|CONDITION|CONTENT|STRINGS|GLOB_RECURSE|RELATIVE|DOWNLOAD
                |EXPECTED_HASH|HTTPHEADER|REPLACE)\b """, Keyword.Reserved),
            (r'\s@ONLY\b', Keyword.Reserved)
        ]

    }

def setup(app: "Sphinx") -> Dict[str, Any]:
    cmake_code_lexer = CMakeCodeLexer()
    lexers['CMakeCode'] = cmake_code_lexer
    lexers['cmake_code'] = cmake_code_lexer
    return {
        'version': '1.0',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
