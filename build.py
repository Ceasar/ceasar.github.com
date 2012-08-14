import collections
import functools
import glob
import os
import sys
import time

import markdown
import jinja2
from jinja2 import Environment, FileSystemLoader, TemplateSyntaxError
from jinja2.ext import Extension
from hamlish_jinja import HamlishExtension
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


STATIC_URL = os.getcwd()
TEMPLATE_DIR = "./templates"


class MarkdownExtension(Extension):
    """Markdown filter for Jinja2."""
    tags = set(['markdown'])

    def __init__(self, environment):
        super(MarkdownExtension, self).__init__(environment)
        environment.extend(
                    markdowner=markdown.Markdown(extensions=['codehilite', 'toc'])
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


def retry(exceptions, tries=5, delay=0.25):
    """Retry the decorated function using an exponential backoff strategy.
    If the function does not complete successfully after the specified number
    of tries, the block exception is re-raised."""
    def wrapper(func):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            mtries, mdelay = tries, delay
            while mtries > 0:
                try:
                    return func(*args, **kwargs)
                except exceptions, e:
                    print "%s" % e
                    waited = mdelay
                    while waited > 0:
                        msg = 'Retrying in {0} seconds...\r'.format(waited)
                        sys.stdout.write(msg)
                        sys.stdout.flush()
                        time.sleep(1)
                        waited -= 1
                    sys.stdout.write("\r%s\r" % (' ' * len(msg)))
                    mdelay += mdelay
                    mtries -= 1
                    if mtries == 0:
                        raise e
        return wrapped
    return wrapper


class JinjaEventHandler(FileSystemEventHandler):

    EXTENSIONS = ['.html', 'haml']

    def __init__(self, template_dir, extensions=None, rules=None):
        """Initialize a new JinjaEventHandler.
        
        Parameters:
            * template_dir - The directory where the templates are located
            * extensions - A list of extensions to the jinja Environment
            * rules - A dictionary that matches up template_names to extra
            data to pass to the template in the form of a dictionary.

        Templates are compiled to the current working directory. (e.g., if
        one has templates/index.html, index.html will be in the cwd, and if
        one has templates/blog/foo.html, blog/foo.html will be created in the
        cwd.)

        All templates, no matter what their extension, are converted to html.

        Templates that begin with an underscore or end with an extension not
        listed in self.EXTENSIONS are ignored.

        If for whatever reason an error occurs, the compiler will attempt
        to recompile the templates using an exponential backing-off strategy.
        """
        loader = FileSystemLoader(searchpath=template_dir)
        if extensions is None:
            extensions = []
        self.env = Environment(loader=loader, extensions=extensions)
        self.env.hamlish_enable_div_shortcut = True
        self.rules = rules

        # Build on init
        self.build(STATIC_URL=STATIC_URL)

    def build_template(self, template_name, **kwargs):
        """Compile a template."""
        print "Compiling %s..." % template_name
        template = self.env.get_template(template_name)
        path = "/".join(template_name.split("/")[:-1]) + "/"
        if not os.path.exists(path):
            os.makedirs(path)
        # Coerce haml files to html files
        if not template_name.endswith('.html'):
            template_name = template_name.split('.')[0] + ".html"
        with open(template_name, "w") as f:
            if template_name in self.rules:
                kwargs.update(self.rules[template_name])
            f.write(template.render(**kwargs))

    def build_post(self, title):
        print "Compiling %s..." % title
        template = self.env.get_template("_post.html")
        with open("./templates/" + title) as r:
            post = r.read()
        title = title.split('.')[0] + ".html"
        with open(title, "w") as f:
            f.write(template.render(post=post))

    @retry(TemplateSyntaxError, tries=float('inf'), delay=5)
    def build(self, **kwargs):
        """Step through each file inside of templates and build it."""
        for path, _, filenames in os.walk('./templates'):
            try:
                # Nested templates will come out as './templates/blog', but
                # we want to compile to 'blog', so trim the first two pieces
                # out if they exist.
                path = "/".join(path.split('/')[2:])
            except IndexError:
                pass
            for filename in filenames:
                if filename.endswith(".md"):
                    self.build_post(filename)
                    continue
                if not any(filename.endswith(ext) for ext in self.EXTENSIONS):
                    continue
                # Ignore any templates whose name begin with an underscore
                # This lets us ignore abstract templates, eg "base.html"
                if not filename.startswith("_"):
                    if path:
                        self.build_template("%s/%s" % (path, filename))
                    else:
                        self.build_template("%s" % (filename))

    def on_modified(self, event):
        """Rebuild the templates if anything changes."""
        super(JinjaEventHandler, self).on_modified(event)
        self.build(STATIC_URL=STATIC_URL)


def watch(event_handler, watched_dir):
    """Watch a directory for changes and notify the event_handler on change."""
    observer = Observer()
    observer.schedule(event_handler, path=watched_dir, recursive=True)
    observer.start()
    print "Watching %s for changes..." % watched_dir
    print "Press Ctrl+C to stop."
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    print "Process killed"
    return 0


Post = collections.namedtuple('Post', ['name', 'href'])


def get_posts():
    """Get all the posts, minus the index."""
    for filename in glob.glob("./*.html"):
        href = filename.split("/")[-1]
        name = href.split(".")[0].replace("_", " ")
        if not name == "index":
            yield Post(name, href)


def main(argv):
    rules = {
        'index.html': {
            'posts': list(get_posts())
        }
    }
    event_handler = JinjaEventHandler(TEMPLATE_DIR,
                                      extensions=[
                                          MarkdownExtension,
                                          HamlishExtension,
                                      ],
                                      rules=rules,
                                      )
    return watch(event_handler, TEMPLATE_DIR)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
