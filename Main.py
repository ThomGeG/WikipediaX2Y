from queue import Queue
from urllib.request import urlopen
from html.parser import HTMLParser

BANNED_THINGS = ("Book", "Template_talk", "Wikipedia", "Template", "Special", "File", "Talk", "Portal", "Help", "Category")

class Path():

    def __init__(self, root_link):
        self.history = [root_link]

    def spawn_child(self, link):
        child_path = Path(None)
        child_path.history = self.history + [link]
        return child_path

    def get_current_page(self):
        return self.history[-1]

    def has_visited(self, address):
        return address in self.history

    def get_size(self):
        return len(self.history)

    def to_string(self):
        return ' -> '.join(map(str, self.history))

class LinkParser(HTMLParser):

    base_url = "https://en.wikipedia.org/wiki/"

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for key, value in attrs:
                if (key == "href" and
                    value.startswith("/wiki/") and #We're dealing with a link to something article-like
                    (value[6:].split(":")[0] not in BANNED_THINGS if (":" in value) else True)):

                    self.links.append(value[6:].split("#")[0])

    def get_links(self, link):
        self.links = []
        self.feed(urlopen(self.base_url + link).read().decode("utf-8"))
        return self.links

if __name__ == "__main__":

    source_page      = input("Source wiki: ")
    destination_page = input("Destination wiki: ")

    pages_visited = []

    parser = LinkParser()

    queue = Queue()
    queue.put(Path(source_page))

    while not queue.empty():
        cur_path = queue.get()
        print("Visiting: " + cur_path.get_current_page())

        for next_page in parser.get_links(cur_path.get_current_page()):

            if next_page is destination_page:
                complete_path = cur_path.spawn_child(next_page)
                print("Found it after: " + complete_path.get_size() + " links.\n\t" + complete_path.to_string)
                break

            if next_page not in pages_visited:
                print("Queueing: " + next_page)
                pages_visited.append(next_page)
                queue.put(cur_path.spawn_child(next_page))
