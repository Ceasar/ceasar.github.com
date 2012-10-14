import jinja2
import jinja2.ext
import markdown


class MarkdownExtension(jinja2.ext.Extension):
    """Markdown filter for Jinja2."""
    tags = set(['markdown'])

    def __init__(self, environment):
        super(MarkdownExtension, self).__init__(environment)
        environment.extend(
                    markdowner=markdown.Markdown(extensions=['codehilite',
                                                             'toc'])
                    )

    def parse(self, parser):
        lineno = parser.stream.next().lineno
        body = parser.parse_statements(
                                       ['name:endmarkdown'],
                                       drop_needle=True
                                       )
        return jinja2.nodes.CallBlock(
                               self.call_method('_markdown_support'),
                               [],
                               [],
                               body).set_lineno(lineno)

    def _markdown_support(self, caller):
        """Helper callback."""
        return self.environment.markdowner.convert(caller()).strip()
