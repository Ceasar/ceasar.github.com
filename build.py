import functools
import os
import sys
import time

from jinja2 import Environment, FileSystemLoader, TemplateSyntaxError
from jinja2_hamlpy import HamlPyExtension
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


STATIC_URL = os.getcwd()
TEMPLATE_DIR = "./templates"


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
    def __init__(self, template_dir, extensions):
        loader = FileSystemLoader(searchpath=template_dir)
        if extensions is None:
            extensions = []
        self.env = Environment(loader=loader, extensions=extensions)

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
            f.write(template.render(**kwargs))

    EXTENSIONS = ['.html', 'haml']

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


def main(argv):
    event_handler = JinjaEventHandler(TEMPLATE_DIR,
                                      extensions=[HamlPyExtension]
                                      )
    return watch(event_handler, TEMPLATE_DIR)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
