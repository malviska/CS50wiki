import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage



def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"(.+)\.md$", r'<a href="/wiki/\1">\1</a>', filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content, overwrite):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
      if not overwrite:
        raise NameError
      else:
          default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None


def markdown_parser(full):
    """
    Retrieves the body of the full markdown
    """
    formatedBatch = re.sub(r"^([\w][^\n]+)", r'<p>\1</p>\n', full,flags=re.M)
    formatedBatch = re.sub(r"\[([^\n]+?)\]\(([^\n]+?)\)", r'<a href="\2">\1</a>', formatedBatch)
    formatedBatch = re.sub(r"\*\*([^\n]+?)\*\*", r"<b>\1</b>", formatedBatch)
    formatedBatch = re.sub(r"### ([^\n]+)", r"<h3>\1</h3>", formatedBatch)
    formatedBatch = re.sub(r"## ([^\n]+)", r"<h2>\1</h2>", formatedBatch)
    formatedBatch = re.sub(r"# ([^\n]+)", r"<h1>\1</h1>", formatedBatch)
    formatedBatch = re.sub(r'\* ([^\n]+)', r'<li>\1</li>', formatedBatch)
    formatedBatch = re.sub(r'\n+?','', formatedBatch,flags=re.M)
    formatedBatch = re.sub(r'([^</li>]+)<li>', r'\1<ul><li>', formatedBatch)
    formatedBatch = re.sub(r'</li>([^<li>]+)', r'</li></ul>\1', formatedBatch)
    return formatedBatch

def list_similar_entrys(value):
    """
    List all entrys that had passed value as a substring
    """
    _, filenames = default_storage.listdir("entries")
    name_entrys = list(sorted(re.sub(r'\.md$', '', filename)
                   for filename in filenames if filename.endswith('.md')))
    similars = list(match for match in name_entrys if re.search(value, match))
    if len(similars) == 0:
        return ['No entry match']
    return list(re.sub(r'(.+)', r'<a href="/wiki/\1">\1</a>', similar)
                for similar in similars)