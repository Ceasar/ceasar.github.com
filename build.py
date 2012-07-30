import sys
import time
import glob

from jinja2 import Environment, FileSystemLoader
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


TEMPLATE_DIR = "./templates"


class JinjaEventHandler(FileSystemEventHandler):
    def __init__(self, template_dir):
        loader = FileSystemLoader(searchpath=template_dir)
        self.env = Environment(loader=loader)

    def build_template(self, template_name, **kwargs):
        print "Compiling %s..." % template_name
        template = self.env.get_template(template_name)
        with open(template_name, "w") as f:
            f.write(template.render(**kwargs))

    def build(self):
        templates = glob.glob('./templates/*.html')
        for template in templates:
            name = template.split('/')[-1]
            # Ignore any templates whose name begin with an underscore
            # This lets us ignore abstract templates, eg "base.html"
            if not name.startswith("_"):
                self.build_template(name)

    def on_modified(self, event):
        super(JinjaEventHandler, self).on_modified(event)
        self.build()


def watch(event_handler, watched_dir):
    observer = Observer()
    observer.schedule(event_handler, path=watched_dir)
    observer.start()
    print "Watching %s for changes..." % watched_dir
    print "Press Ctrl+C to stop."
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    print "Process killed"
    observer.join()
    return 0


def main(argv):
    event_handler = JinjaEventHandler(TEMPLATE_DIR)
    return watch(event_handler, TEMPLATE_DIR)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
