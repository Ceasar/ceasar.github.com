import collections
import glob
import os

import staticjinja

from extensions import MarkdownExtension

Post = collections.namedtuple('Post', ['name', 'href'])


def index():
    """Get all the posts, minus the index."""
    posts = []
    filenames = glob.glob("./*html")
    for filename in filenames:
        _, tail = os.path.split(filename)
        name, _ = tail.split(".")
        name = name.replace("_", " ")
        if not name == "index":
            posts.append(Post(name, tail))
    return {'posts': posts}


def get_contents(filename):
    with open(filename) as f:
        return {'post': f.read()}


def build_post(env, filename, **kwargs):
    """
    Render a file using "_post.html".
    """
    template = env.get_template("_post.html")
    _, tail = os.path.split(filename)
    title, _ = tail.split('.')
    template.stream(**kwargs).dump(title + ".html")


if __name__ == "__main__":
    staticjinja.main(extensions=[
        MarkdownExtension,
    ], contexts=[
        ('index.html', index),
        ('.*.md', get_contents),
    ], rules=[
        ('.*.md', build_post),
    ])
