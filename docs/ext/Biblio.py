import re

from collections import defaultdict
from typing import List, Dict, Any, Tuple

from docutils import nodes
from docutils.parsers.rst import Directive, directives

from sphinx import addnodes
from sphinx.directives import ObjectDescription
from sphinx.domains import Domain, Index
from sphinx.util.docutils import SphinxDirective


class BiblioItem(Directive):

    def run(self) -> List[nodes.Node]:
        # n = nodes.paragraph(text="babla")
        # node_list = [n]
        # p = nodes.paragraph(text="pipin")
        # node_list.append(p)
        # pp = nodes.literal(text="literal")

        # node_list.append(pp)
        # pl = nodes.literal(text="literal2")
        # node_list.append(pl)
        # item = nodes.list_item()
        # item += nodes.Text("pipsku")
        # reference = nodes.reference('', '', internal=False, refuri="http://example.com", classes=['test'])
        # reference += nodes.strong("exmpls", "exm")
        # node_list.append(reference)
        # node_list.append(item)

        content = []

        para = nodes.paragraph()
        description = (
                '(The original entry is located in %s, line %d and can be found ' %
                ("filename", 11))
        para += nodes.Text(description, description)

        # Create a reference
        newnode = nodes.reference('', '', internal=False, refuri="http://example.com", classes=['test'])
        innernode = nodes.emphasis('here', 'here')
        newnode.append(innernode)
        para += newnode
        para += nodes.Text('.)', '.)')

        content.append(para)

        return content


class MyDirective(Directive):
    """
        Adding bullet list and references
    """

    def run(self):
        my_nodes = nodes.bullet_list(bullet='*')
        for text, ref in [('Text Item 1', 'https://link/to/somewhere'),
                          ('Text Item 2', 'https://link/to/somewhere_else')]:
            item = nodes.list_item()
            para = nodes.paragraph(text=text)
            refnode = nodes.reference('', '', internal=False, refuri=ref)
            innernode = nodes.emphasis("link", "link")
            refnode.append(innernode)
            para += refnode
            item += para
            # Magic happens
            my_nodes.append(item)
        return [my_nodes]


def int_to_roman(input):
    """ Convert an integer to a Roman numeral. """

    if not isinstance(input, type(1)):
        raise TypeError("expected integer, got %s" % type(input))
    if not 0 < input < 4000:
        raise ValueError("Argument must be between 1 and 3999")
    ints = (1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1)
    nums = ('M', 'CM', 'D', 'CD', 'C', 'XC', 'L', 'XL', 'X', 'IX', 'V', 'IV', 'I')
    result = []
    for i in range(len(ints)):
        count = int(input / ints[i])
        result.append(nums[i] * count)
        input -= ints[i] * count
    return ''.join(result)

class ParseError(Exception):
    pass


class Issue:

    def __init__(self, year, language, edition=1, series='', volume=0, 
                 volume_name='', part=0, part_name='', fascicle=0,
                 fascicle_name='', links: Dict[str, str] = {}):
        self.year = year
        self.language = language
        self.edition = edition
        self.series = series
        self.volume = volume
        self.volume_name = volume_name
        self.part = part
        self.part_name = part_name
        self.fascicle = fascicle
        self.fascicle_name = fascicle_name
        self.links = links

    @classmethod
    def init_from_raw(cls, raw_source: List[str]):
        raw = {
            'year': '',
            'language': '',
            'edition': '',
            'series': '',
            'volume': '',
            'volume_name': '',
            'part': '',
            'part_name': '',
            'fascicle' : '',
            'fascicle_name': '',
            'links' : {}
        }
        lexer = {
            'year': re.compile(r'^\:year\:\s+(\d{4})'),
            'language': re.compile(r'^\:language\:\s+([A-Za-z]{3})'),
            'edition': re.compile(r'^\:edition\:\s+(\d+)'),
            'series' : re.compile(r'^\:series\:\s+(.*?)$'),
            'volume' : re.compile(r'\:volume\:\s+(\w+)'),
            'volume_name' : re.compile(r'^\:volume_name\:\s+(.*?)$'),
            'part' : re.compile(r'\:part\:\s(\w+)'),
            'part_name' : re.compile(r'^\:part_name\:\s+(.*?)$'),
            'fascicle' : re.compile(r'\:fascicle\:\s(\w+)'),
            'fascicle_name' : re.compile(r'^\:fascicle_name\:\s+(.*?)$'),
            'links' : re.compile(r'^\:link\s+(\w+)\:\s+(.*)$')
        }

        for line in raw_source:
            match_links = lexer['links'].match(line)
            if match_links:
                raw['links'][match_links.group(1)] = match_links.group(2)
                continue

            for field in ['year', 'language', 'edition', 'series', 'volume', 
            'volume_name', 'part', 'part_name', 'fascicle', 'fascicle_name']:
                match = lexer[field].match(line)
                if match:
                    if raw[field] == '':
                        if not match.group(1) == '':
                            raw[field] = match.group(1)
                    else:
                        raise ParseError("Field duplication " + field)
            
        return Issue(raw['year'], raw['language'], raw["edition"], raw['series']
             , raw["volume"], raw["volume_name"], raw["part"], raw["part_name"]
             , raw["fascicle"], raw["fascicle_name"], raw['links'])

    def build_issue_title(self) -> str:
        issue_title = ''

        if not self.part_name == '':
            issue_title = self.part_name
        elif not self.fascicle_name == '':
            issue_title = self.fascicle_name
        elif not self.volume_name == '':
            issue_title = self.volume_name

        return issue_title

    def build_file_component(self) -> str:
        file_component_str = '({}.{})'.format(self.year, int_to_roman(int(self.edition)))
        if not (self.volume == 0 or self.volume == ''):
            file_component_str += '.V{}'.format(self.volume)
        if not (self.fascicle == 0 or self.fascicle == ''):
            file_component_str += '.F{}'.format(self.fascicle)
        if not (self.part == 0 or self.part == ''):
            file_component_str += '.P{}'.format(self.part)

        issue_title = self.build_issue_title()

        if not issue_title == '':
            p = re.compile(r'\s')
            issue_title = p.sub('_', issue_title)
            file_component_str += '.{}'.format(issue_title)

        file_component_str += '.[{}]'.format(self.language.upper())

        return file_component_str

    def build_node(self) -> nodes.Node:
        issue_node = nodes.paragraph()
        issue_node += nodes.strong(text=self.year, classes=['book-issue-year'])
        if not (self.volume == 0 or self.volume == ''):
            issue_node += nodes.inline(text= ', Volume {}'.format(self.volume), classes=['book-issue-volume'])

        if not (self.fascicle == 0 or self.fascicle == ''):
            issue_node += nodes.inline(text= ', Fascicle {}'.format(self.fascicle), classes=['book-issue-fascicle'])

        if not (self.part == 0 or self.part == ''):
            issue_node += nodes.inline(text= ', Part {}'.format(self.part), classes=['book-issue-part'])


        issue_node += nodes.inline(text=":", classes=['book-issue-punctuation'])

        issue_title = self.build_issue_title()

        if not issue_title == '':
            issue_node += nodes.inline(text=issue_title, classes=['book-issue-title'])

        issue_node += nodes.inline(text=" - ", classes=['book-issue-punctuation'])

        issue_node += nodes.inline(text='%s edition' % (int_to_roman(int(self.edition))))

        language_string = self.language
        if self.language.upper() == 'ENG':
            language_string = 'English'
        elif self.language.upper() == 'RUS':
            language_string = 'Russian'

        issue_node += nodes.inline(text=' ({})'.format(language_string), classes=['book-issues-language'])

        if not self.series == '':
            issue_node += nodes.inline(text=' | ', classes=['book-issues-punctuation'])
            issue_node += nodes.inline(text=self.series, classes=['book-issues-series'])

        info_bullet_list = nodes.bullet_list(bullet='*')

        for link_name in self.links:
            link_item = nodes.list_item()
            link_par = nodes.paragraph()
            reference = nodes.reference('', '', internal=False, refuri=self.links[link_name])
            reference += nodes.strong(link_name,link_name)
            link_par += reference
            link_item += link_par
            info_bullet_list += link_item

        file_name_item = nodes.list_item()
        file_name_item += nodes.paragraph(text=self.build_file_component(), classes=['book-issue-filename'])
        info_bullet_list += file_name_item

        issue_node += info_bullet_list
        return issue_node

class Author:

    def __init__(self, first_name: str, last_name:str, target_id:int, middle_name=''):
        self.first_name = first_name
        self.last_name = last_name
        self.target_id = target_id
        self.middle_name = middle_name

    @classmethod
    def init_from_raw(cls, raw: str, target_id: int):
        name_parts = raw.split()
        if len(name_parts) == 2:
            return cls(name_parts[0], name_parts[1], target_id)
        elif len(name_parts) == 3:
            return cls(name_parts[0], name_parts[2], target_id, name_parts[1])
        else:
            raise ValueError('Cannot parse raw string')

    def build_file_component(self) -> str:
        file_component = ''
        rus_detect = re.compile(r'[А-Я]')
        rus_match = rus_detect.match(self.first_name.upper())
        if rus_match:
            if self.middle_name == '':
                file_component = '{}.{}'.format(
                    self.last_name, self.first_name[0])
            else:
                file_component = '{}.{}.{}.'.format(
                    self.last_name, self.first_name[0], self.middle_name[0])
        else:
            if self.middle_name == '':
                file_component = '{}.{}'.format(
                    self.first_name, self.last_name)
            else:
                file_component = '{}.{}.{}'.format(
                    self.first_name, self.middle_name[0], self.last_name)
        return file_component


    def get_id(self) -> str:
        result = self.first_name[0].upper()
        if not self.middle_name == '':
            result += self.middle_name[0].upper()
        return result + self.last_name

    def build_node(self) -> List[nodes.Node]:
        author_str = self.first_name
        if self.middle_name == '':
            author_str += ' {}'.format(self.last_name)
        else:
            author_str += ' {} {}'.format(self.middle_name, self.last_name)

        author_target = nodes.target('','', ids=['author-%s' % self.target_id])
        author_paragraph = nodes.paragraph()
        author_paragraph += author_target
        author_paragraph += nodes.inline(text=author_str, classes=['book-author'])


        fake = nodes.inline('','') # FIXME

        return [author_paragraph, fake]



class Book:

    def __init__(self, title: str, authors: List["Author"],
                 issues: List["Issue"] = [], subtitle: str = '', title_localized: str = '',
                 subtitle_localized: str = '', tags: List[str] = []):
        self.title = title
        self.authors = authors
        self.issues = issues
        self.subtitle = subtitle
        self.title_localized = title_localized
        self.subtitle_localized = subtitle_localized
        self.tags = tags

    def add_issue(self, issue: "Issue"):
        self.issues.append(issue)

    def build_node_authors(self) -> Tuple[nodes.Node, List[nodes.Node]]:
        authors_node = nodes.paragraph(text='Authors', classes=['book-authors-title'])
        authors_bullet_list = nodes.bullet_list(bullet='-')
        targets = []
        for a in self.authors:
            author_list_item = nodes.list_item()
            n, t = a.build_node()
            author_list_item += n
            targets.append(t)
            authors_bullet_list += author_list_item

        authors_node += authors_bullet_list
        return (authors_node, targets)

    def build_node_issues(self) -> nodes.Node:
        issues_node = nodes.paragraph(text='Issues', classes=['book-issues-title'])
        issues_bullet_list = nodes.bullet_list(bullet='-')
        for i in self.issues:
            issue_list_item = nodes.list_item()
            issue_list_item += i.build_node()
            issues_bullet_list += issue_list_item

        issues_node += issues_bullet_list
        return issues_node

    def build_folder_title(self) ->str:
        authors_part = []
        authors_count = 0
        for author in self.authors:
            if authors_count >= 3:
                break

            authors_part.append(author.build_file_component())

        authors_str = ','.join(authors_part)
        p = re.compile(r'[ :\\/]')
        title_str = p.sub('_', self.title)
        return '{}-{}'.format(authors_str, title_str)



    def build_node(self) -> Tuple[nodes.Node, List[nodes.Node]]:
        book_topic = nodes.topic(classes=['book-topic'])

        book_title = nodes.paragraph(text=self.title, classes=['book-title'])
        if not self.subtitle == '':
            book_title += nodes.inline(text=': ', classes=['book-punctuation'])
            book_title += nodes.inline(text=self.subtitle, classes=['book-subtitle'])

        book_topic += book_title

        if not self.title_localized == '':
            book_title_localized = nodes.paragraph(text=self.title_localized, classes=['book-title-localized'])

            if not self.subtitle_localized == '':
                book_title_localized += nodes.inline(text=': ', classes=['book-punctuation'])
                book_title_localized += nodes.inline(text=self.subtitle_localized, classes=['book-subtitle-localized'])

            book_topic += book_title_localized

        book_tags = nodes.paragraph(classes=['book-tags-container'])

        first_space = True
        for t in self.tags:
            if first_space:
                first_space = False
            if not first_space:
                book_tags += nodes.inline(text=' ', classes=['book-punctuation'])
            book_tags += nodes.inline(text=t.strip(), classes=['book-tag'])
        
        book_topic += book_tags

        book_folder_component = nodes.paragraph(text=self.build_folder_title(), classes=['book-file-component'])
        book_topic += book_folder_component

        book_left_bullet_list = nodes.bullet_list(bullet='*')

        authors_list_item = nodes.list_item()
        authors = self.build_node_authors()
        authors_list_item += authors[0]
        book_left_bullet_list += authors_list_item

        book_right_bullet_list = nodes.bullet_list(bullet='*')

        issues_list_item = nodes.list_item()
        issues_list_item += self.build_node_issues()
        book_right_bullet_list += issues_list_item

        root_hlist = addnodes.hlist()
        root_hlist += addnodes.hlistcol('', book_left_bullet_list)
        root_hlist += addnodes.hlistcol('', book_right_bullet_list)
        book_topic += root_hlist
        
        return (book_topic, authors[1])


class BookNode(SphinxDirective):

    has_content = True
    required_arguments = 1
    final_argument_whitespace = True
    option_spec = {
        'subtitle': directives.unchanged,
        'title_localized': directives.unchanged,
        'subtitle_localized': directives.unchanged,
        'authors': directives.unchanged_required,
        'tags': directives.unchanged
    }

    def parse_authors(self) -> List["Author"]:
        author_list = []
        for author_raw in self.options.get('authors').split(','):
            target_id = self.env.new_serialno('author')
            author = Author.init_from_raw(author_raw, target_id)
            author_list.append(author)

        return author_list

    def parse_issues(self) -> List["Issue"]:
        raw_container = []
        collecting = False
        raw = []

        for line in self.content:
            line = line.strip()

            if line == '':
                continue

            if line == ':issue:':
                collecting = True
                if len(raw) > 0:
                    raw_container.append(raw)
                    raw = []
                continue

            if collecting:
                raw.append(line)

        if len(raw) > 0:
            raw_container.append(raw)

        issue_list = []
        for raw_list in raw_container:
            issue = Issue.init_from_raw(raw_list)
            issue_list.append(issue)

        return issue_list

    def run(self) -> List[nodes.Node]:
        subtitle = self.options.get('subtitle', '')
        title_localized = self.options.get('title_localized', '')
        subtitle_localized = self.options.get('subtitle_localized', '')
        tags = self.options.get('tags', '').split(',')

        book = Book(self.arguments[0], self.parse_authors(), self.parse_issues(), 
            subtitle=subtitle, title_localized=title_localized, 
            subtitle_localized=subtitle_localized, tags=tags)

        athenaeum = self.env.get_domain('athenaeum')
        athenaeum.add_book(book)

        book_node = book.build_node()
        retlist = [book_node[0]] + book_node[1]

        return retlist

class AuthorIndex(Index):
    name = 'author'
    localname = 'Author Index'
    shortname = 'Authors'

    def generate(self, docnames=None):
        content = defaultdict(list)

        authors = self.domain.data['authors']

        for name, dispname, typ, docname, anchor, _ in authors:
            content[dispname[0].lower()].append(
                (dispname, 0, docname, anchor, docname, '', typ))

        content = sorted(content.items())

        return content, True


class Athenaeum(Domain):
    name = 'athenaeum'
    label = 'Athenaeum of useful books'
    roles = {}
    directives = {
        'book' : BookNode
    }
    indices = {
        AuthorIndex
    }
    initial_data = {
        'authors': [],  # id -> object
        'books': {},  # id -> object
        'series': [],  # list of series
    }

    def get_full_qualified_name(self, node: nodes.Element) -> str:
        book_title = node.arguments[0].strip().replace(' ', '')
        return '{}-{}'.format(self.name, book_title)

    def add_author(self, author: "Author") -> None:
        name = '{}.{}_{}'.format('author', author.first_name, author.last_name)
        dispname = '{} {}'.format(author.first_name, author.last_name)
        anchor = '{}-{}'.format('author', author.target_id)

        exists = next((x for x in self.data['authors'] if (x[0] == name) and (x[4] == anchor)), False)

        if not exists:
            self.data['authors'].append((name, dispname, 'Author', self.env.docname, anchor, 1))

    def add_book(self, book: "Book") -> None:
        for a in book.authors:
            self.add_author(a)
        
    def get_authors(self):
        for obj in self.data['authors']:
            yield obj


def setup(app: "Sphinx") -> Dict[str, Any]:
    #app.add_directive("biblio", BiblioItem)
    #app.add_directive("my_directive", MyDirective)
    #app.add_directive("book", ParamDirective)

    app.add_domain(Athenaeum)

    return {
        'version': '1.0',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }