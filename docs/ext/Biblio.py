import re

from collections    import defaultdict
from typing         import List, Dict, Any, Tuple

from docutils               import nodes
from docutils.parsers.rst   import Directive, directives

from sphinx                 import addnodes
from sphinx.directives      import ObjectDescription
from sphinx.domains         import Domain, Index
from sphinx.util.docutils   import SphinxDirective


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

    classes = {
        'year':         ['book-issue-year'],
        'volume':       ['book-issue-volume'],
        'fascicle':     ['book-issue-fascicle'],
        'part':         ['book-issue-part'],
        'punctuation':  ['book-issue-punctuation'],
        'title':        ['book-issue-title'],
        'language':     ['book-issue-language'],
        'series':       ['book-issue-series'],
        'filename':     ['book-issue-filename']
    }

    languages_dict = {
        'ENG' : 'English',
        'RUS' : 'Russian'
    }

    def __init__(self
                , year:          str
                , language:      str
                , edition:       int = 1
                , series:        str = ''
                , volume:        str = ''
                , volume_name:   str = ''
                , part:          int = 0
                , part_name:     str = ''
                , fascicle:      int = 0
                , fascicle_name: str = ''
                , links:         Dict[str, str] = {}):
        self.year          = year
        self.language      = language
        self.edition       = edition
        self.series        = series
        self.volume        = volume
        self.volume_name   = volume_name
        self.part          = part
        self.part_name     = part_name
        self.fascicle      = fascicle
        self.fascicle_name = fascicle_name
        self.links         = links

    @classmethod
    def init_from_raw(cls, raw_source: List[str]):
        raw = {
            'year':          '',
            'language':      '',
            'edition':       '',
            'series':        '',
            'volume':        '',
            'volume_name':   '',
            'part':          '',
            'part_name':     '',
            'fascicle':      '',
            'fascicle_name': '',
            'links':         {}
        }

        lexer = {
            'year':          re.compile(r'^\:year\:\s+(\d{4})'),
            'language':      re.compile(r'^\:language\:\s+([A-Za-z]{3})'),
            'edition':       re.compile(r'^\:edition\:\s+(\d+)'),
            'series':        re.compile(r'^\:series\:\s+(.*?)$'),
            'volume':        re.compile(r'\:volume\:\s+(\w+)'),
            'volume_name':   re.compile(r'^\:volume_name\:\s+(.*?)$'),
            'part':          re.compile(r'\:part\:\s(\w+)'),
            'part_name':     re.compile(r'^\:part_name\:\s+(.*?)$'),
            'fascicle':      re.compile(r'\:fascicle\:\s(\w+)'),
            'fascicle_name': re.compile(r'^\:fascicle_name\:\s+(.*?)$'),
            'links':         re.compile(r'^\:link\s+(\w+)\:\s+(.*)$')
        }

        for line in raw_source:
            match_links = lexer['links'].match(line)
            if match_links: # not unique fields
                raw['links'][match_links.group(1)] = match_links.group(2)
            else:           # unique fields
                for field in raw:
                    match = lexer[field].match(line)
                    if match:
                        if raw[field] == '':
                            if not match.group(1) == '':
                                raw[field] = match.group(1)
                        else:
                            raise ParseError("Issue: field duplication " + field)

        if raw['part'] == '':
            raw['part'] = 0
        
        if raw['fascicle'] == '':
            raw['fascicle'] = 0

        return Issue(raw['year']
                    , raw['language']
                    , int(raw["edition"])
                    , raw['series']
                    , raw["volume"]
                    , raw["volume_name"]
                    , int(raw["part"])
                    , raw["part_name"]
                    , int(raw["fascicle"])
                    , raw["fascicle_name"]
                    , raw['links'])

    def build_issue_title_prefix_node(self) -> nodes.Node:
        prefix_node = nodes.inline()

        if self.volume != '':
            prefix_node += nodes.inline(text=', Volume {}'.format(self.volume)
                                       , classes=self.classes['volume'])

        if self.fascicle != 0:
            prefix_node += nodes.inline(text=', Fascicle {}'.format(self.fascicle)
                                       , classes=self.classes['fascicle'])

        if self.part != 0:
            prefix_node += nodes.inline(text=', Part {}'.format(self.part)
                                       , classes=self.classes['part'])

        prefix_node += nodes.inline(text=":"
                                   , classes=self.classes['punctuation'])

        return prefix_node

    def build_issue_title(self) -> str:
        issue_title = ''

        if self.part_name != '':
            issue_title = self.part_name
        elif self.fascicle_name != '':
            issue_title = self.fascicle_name
        elif self.volume_name != '':
            issue_title = self.volume_name

        return issue_title

    def build_issue_title_node(self) -> nodes.Node:
        issue_title_node = nodes.inline(
            text=self.build_issue_title(), classes=self.classes['title'])

        issue_title_node += nodes.inline(text=" - ",
                                         classes=self.classes['punctuation'])

        return issue_title_node

    def build_file_component(self) -> str:
        file_component_str = '({}.{})'.format(self.year, int_to_roman(int(self.edition)))
        if self.volume != '':
            file_component_str += '.V{}'.format(self.volume)
        if self.fascicle != 0:
            file_component_str += '.F{}'.format(self.fascicle)
        if self.part != 0:
            file_component_str += '.P{}'.format(self.part)

        issue_title = self.build_issue_title()

        if not issue_title == '':
            issue_title = re.compile(r'\s').sub('_', issue_title)
            file_component_str += '.{}'.format(issue_title)

        file_component_str += '.[{}]'.format(self.language.upper())

        return file_component_str

    def build_language_node(self) -> nodes.Node:
        language_string = self.language.upper()

        if language_string in self.languages_dict:
            language_string = self.languages_dict[language_string]

        return nodes.inline(text=' ({})'.format(language_string)
                           , classes=self.classes['language'])

    def build_link_node(self, link) -> nodes.Node:
        reference = nodes.reference(
            '', '', internal=False, refuri=self.links[link])
        reference += nodes.strong(link, link)
        return reference

    def build_node(self) -> nodes.Node:
        issue_node = nodes.paragraph()

        issue_node += nodes.strong(text=self.year, classes=self.classes['year'])
        issue_node += self.build_issue_title_prefix_node()
        issue_node += self.build_issue_title_node()
        issue_node += nodes.inline(text='%s edition' % (int_to_roman(int(self.edition))))
        issue_node += self.build_language_node()
        
        if not self.series == '':
            issue_node += nodes.inline(text=' | ', classes=self.classes['punctuation'])
            issue_node += nodes.inline(text=self.series, classes=self.classes['series'])

        info_bullet_list = nodes.bullet_list(bullet='*')

        if len(self.links) > 0:
            link_item = nodes.list_item()
            link_par = nodes.paragraph()

            for link_name in self.links:
                link_par += self.build_link_node(link_name)
                link_par += nodes.inline(text=' ')

            link_item += link_par
            info_bullet_list += link_item

        file_name_item = nodes.list_item()
        file_name_item += nodes.paragraph(
            text=self.build_file_component(), classes=self.classes['filename'])
        info_bullet_list += file_name_item

        issue_node += info_bullet_list
        return issue_node

class Author:

    classes = {
        'author': ['book-author']
    }

    def __init__(self
                , id:          int
                , first_name:  str
                , last_name:   str
                , middle_name: str = ''):
        self.id = 'author-%s' % id      # str
        self.first_name = first_name    # str
        self.last_name = last_name      # str
        self.middle_name = middle_name  # str

    @classmethod
    def init_from_raw(cls, id: int, raw: str):
        name_parts = raw.split()
        if len(name_parts) == 2:
            return cls(id, name_parts[0], name_parts[1])
        elif len(name_parts) == 3:
            return cls(id, name_parts[0], name_parts[2], name_parts[1])
        else:
            raise ParseError('Author: cannot parse raw string')

    def get_full_name(self) -> str:
        result = 'author-' + self.first_name
        if not self.middle_name == '':
            result += self.middle_name
        return result + self.last_name

    def get_displayable_name(self) -> str:
        displayable_name = self.first_name
        if self.middle_name == '':
            displayable_name += ' {}'.format(self.last_name)
        else:
            displayable_name += ' {} {}'.format(self.middle_name, self.last_name)

        return displayable_name

    def build_file_component(self) -> str:
        file_component = ''

        rus_match = re.compile(r'[А-Я]').match(self.first_name.upper())
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

    def build_node(self) -> nodes.Node:
        author_paragraph = nodes.paragraph()
        author_paragraph += nodes.target('', '', ids=[self.id])
        author_paragraph += nodes.inline(text=self.get_displayable_name(),
                                         classes=self.classes['author'])
        return author_paragraph



class Book:

    classes = {
        'authors': ['book-authors-title'],
        'issues': ['book-issues-title'],
    }

    def __init__(self
                , title:              str
                , authors:            List["Author"]
                , id:                 int
                , issues:             List["Issue"] = []
                , subtitle:           str = ''
                , title_localized:    str = ''
                , subtitle_localized: str = ''
                , tags:               List[str] = []):
        self.title              = title
        self.authors            = authors
        self.id                 = 'book-%s' % id
        self.issues             = issues
        self.subtitle           = subtitle
        self.title_localized    = title_localized
        self.subtitle_localized = subtitle_localized
        self.tags               = tags

    def build_node_authors(self) -> nodes.Node:
        authors_node = nodes.paragraph(text='Authors'
                                      , classes=self.classes['authors'])

        authors_bullet_list = nodes.bullet_list(bullet='-')
        for a in self.authors:
            author_list_item = nodes.list_item()
            author_list_item += a.build_node()
            authors_bullet_list += author_list_item

        authors_node += authors_bullet_list
        return authors_node

    def build_node_issues(self) -> nodes.Node:
        issues_node = nodes.paragraph(text='Issues', classes=self.classes['issues'])

        issues_bullet_list = nodes.bullet_list(bullet='-')
        for i in sorted(self.issues, key=lambda issue: issue.year):
            issue_list_item = nodes.list_item()
            issue_list_item += i.build_node()
            issues_bullet_list += issue_list_item

        issues_node += issues_bullet_list
        return issues_node

    def build_folder_title(self) ->str:
        authors_part = []
        for author in self.authors:
            if len(authors_part) > 3:
                break

            authors_part.append(author.build_file_component())

        authors_str = ','.join(authors_part)
        title_str = re.compile(r'[ :\\/]').sub('_', self.title)
        return '{}-{}'.format(authors_str, title_str)

    def build_node(self) -> nodes.Node:
        book_topic = nodes.topic(classes=['book-topic'])
        book_topic += nodes.target('', '', ids=[self.id])
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
        authors_list_item += self.build_node_authors()
        book_left_bullet_list += authors_list_item

        book_right_bullet_list = nodes.bullet_list(bullet='*')

        issues_list_item = nodes.list_item()
        issues_list_item += self.build_node_issues()
        book_right_bullet_list += issues_list_item

        root_hlist = addnodes.hlist()
        root_hlist += addnodes.hlistcol('', book_left_bullet_list)
        root_hlist += addnodes.hlistcol('', book_right_bullet_list)
        book_topic += root_hlist
        
        return book_topic


class BookDirective(SphinxDirective):

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
            author = Author.init_from_raw(target_id, author_raw)
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
        tags = [x.strip() for x in self.options.get('tags', '').split(',')]

        book = Book(self.arguments[0], self.parse_authors(), self.env.new_serialno('book'),
            self.parse_issues(), 
            subtitle=subtitle, title_localized=title_localized, 
            subtitle_localized=subtitle_localized, tags=tags)

        athenaeum = self.env.get_domain('athenaeum')
        athenaeum.add_book(book)

        book_node = book.build_node()

        return [book_node]

class AuthorIndex(Index):
    name = 'author'
    localname = 'Author Index'
    shortname = 'Authors'

    def generate(self, docnames=None):
        content = defaultdict(list)

        authors = self.domain.data['authors']

        for name, dispname, typ, docname, anchor, prio, a_id  in authors:
            content[dispname[0].lower()].append(
                (dispname, 0, docname, anchor, '', '', typ))

        for k in content:
            content[k].sort()
        content = sorted(content.items())

        return content, True

class BookAllIndex(Index):
    name = 'all_books'
    localname = 'Book Index'
    shortname = 'Books'

    def generate(self, docnames=None):
        content = defaultdict(list)

        books = self.domain.data['books']

        for name, dispname, typ, docname, anchor, prio, authors, series, _ in books:
            desc_list = []
            for a in authors:
                desc_list.append(a.last_name)
            desc = ', '.join(desc_list)
            content[dispname[0].lower()].append(
                (dispname, 0, docname, anchor, desc, '', typ))

        content = sorted(content.items())

        return content, True

class SeriesIndex(Index):
    name = 'series'
    localname = 'Series Index'
    shortname = 'Series'

    def generate(self, docnames=None):
        content = defaultdict(list)

        domain_series = self.domain.data['series']

        for name, dispname, typ, docname in domain_series:
            content[dispname[0].lower()].append(
                (dispname, 0, docname, '', '', '', typ))

        content = sorted(content.items())

        return content, True

class TagsIndex(Index):
    name = 'tags'
    localname = 'Tags Index'
    shortname = 'Tags'

    def generate(self, docnames=None):
        content = defaultdict(list)

        domain_tags = self.domain.data['tags']

        for name, dispname, typ, docname in domain_tags:
            content[dispname[0].lower()].append(
                (dispname, 0, docname, '', '', '', typ))

        content = sorted(content.items())

        return content, True


def author_book_list_generator(self, docnames=None):
    content = defaultdict(list)

    books = self.domain.data['books']

    for name, dispname, typ, docname, anchor, prio, authors, series, _ in books:
        found = False
        for auth in authors:
            if auth.last_name == self.magic_author.last_name \
                and auth.first_name == self.magic_author.first_name:
                found = True

        if found:
            desc_list = []
            for a in authors:
                desc_list.append(a.last_name)
            desc = ', '.join(desc_list)
            content[dispname[0].lower()].append(
                (dispname, 0, docname, anchor, desc, '', typ))

    content = sorted(content.items())

    return content, True

def series_book_generator(self, docnames=None):
    content = defaultdict(list)
    books = self.domain.data['books']

    for name, dispname, typ, docname, anchor, prio, authors, series, _ in books:
        if self.magic_series in series:
            desc_list = []
            for a in authors:
                desc_list.append(a.last_name)
            desc = ', '.join(desc_list)
            content[dispname[0].lower()].append(
                (dispname, 0, docname, anchor, desc, '', typ))

    content = sorted(content.items())

    return content, True

def tags_book_generator(self, docnames=None):
    content = defaultdict(list)
    books = self.domain.data['books']

    for name, dispname, typ, docname, anchor, prio, authors, series, tags in books:
        
        if self.magic_tag in tags:
            desc_list = []
            for a in authors:
                desc_list.append(a.last_name)
            desc = ', '.join(desc_list)
            content[dispname[0].lower()].append(
                (dispname, 0, docname, anchor, desc, '', typ))

    content = sorted(content.items())

    if self.magic_tag == 'C++':
        pass #raise Exception(len(content))


    return content, True

class Athenaeum(Domain):
    name = 'athenaeum'
    label = 'Athenaeum of useful books'
    roles = {}
    directives = {
        'book' : BookDirective
    }
    indices = [
        AuthorIndex,
        BookAllIndex,
        SeriesIndex,
        TagsIndex
    ]
    initial_data = {
        'books': [],
        'authors': [],
        'series': [],
        'tags': []
    }

    def get_full_qualified_name(self, node: nodes.Element) -> str:
        book_title = node.arguments[0].strip().replace(' ', '')
        return '{}-{}'.format(self.name, book_title)

    def add_author(self, author: "Author") -> None:
        name = author.get_full_name()
        anchor = author.id # must be empty
        # docname should be replaced with generated name

        exists = next((x for x in self.data['authors'] if
                       x[0] == name), False)

        if not exists:
            a_id = len(self.data['authors'])

            author_generator = type('authors_%s_generator' % a_id
                        , (Index, )
                        , {'magic_author': author
                        , 'name': 'author_%s' % a_id
                        , 'localname': '{} {}'.format(author.last_name, author.first_name)
                        , 'shortname': author.last_name
                        , 'generate': author_book_list_generator
                        ,})

            self.indices.append(author_generator)

            self.data['authors'].append(
                (name, author.get_displayable_name(), 'Author', 'athenaeum-author_%s' % a_id, anchor, 0, a_id))

    def add_series(self, series:str) -> None:
        name = series.replace(' ', '_')

        exists = next((x for x in self.data['series'] if x[1] == series), False)

        if not exists:

            s_id = len(self.data['series'])

            series_generator = type('series_%s_generator' % s_id
                                    , (Index, )
                                    , {'magic_series': series
                                        , 'name': 'series_%s' % s_id
                                        , 'localname': series
                                        , 'shortname': series
                                        , 'generate': series_book_generator
                                        ,})

            self.indices.append(series_generator)
            self.data['series'].append((name, series, 'Series', 'athenaeum-series_%s' % s_id))

    def add_tag(self, tag:str) -> None:
        if tag == '':
            return

        name = tag.replace(' ', '_')

        exists = next((x for x in self.data['tags'] if x[1] == tag), False)

        if not exists:
            t_id = len(self.data['tags'])

            tags_generator = type('tags_%s_generator' % t_id
                                    , (Index, )
                                    , {'magic_tag': tag
                                        , 'name': 'tag_%s' % t_id
                                        , 'localname': tag
                                        , 'shortname': tag
                                        , 'generate': tags_book_generator
                                        ,})

            self.indices.append(tags_generator)
            self.data['tags'].append(
                (name, tag, 'Tag', 'athenaeum-tag_%s' % t_id))

    def add_book(self, book: "Book") -> None:
        for a in book.authors:
            self.add_author(a)

        for i in book.issues:
            if not i.series == '':
                self.add_series(i.series)

        for t in book.tags:
            self.add_tag(t)
        
        authors_last_names = []
        for a in book.authors:
            authors_last_names.append(a.last_name)
        
        authors_str = '.'.join(authors_last_names)
        name = '{}.{}.{}'.format('book', book.title, authors_str)

        exists = next((x for x in self.data['books'] if
                       x[0] == name), False)

        if not exists:
            series = []
            for i in book.issues:
                if i.series != '':
                    series.append(i.series)

            self.data['books'].append(
                (name, book.title, 'Book', self.env.docname, book.id, 1, book.authors, series, book.tags))


def setup(app: "Sphinx") -> Dict[str, Any]:
    app.add_domain(Athenaeum)

    return {
        'version': '1.0',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
