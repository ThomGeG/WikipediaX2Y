from queue import Queue
from urllib.request import urlopen
from html.parser import HTMLParser

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
                if key == "href" and value.startswith("/wiki/"):
                    self.links.append(value[6:])

    def get_links(self, link):
        self.links = []
        self.feed(urlopen(self.base_url + link).read().decode("utf-8"))
        return self.links

if __name__ == "__main__":

    source_page      = "Hearthstone_(video_game)"
    destination_page = "Autism"

    parser = LinkParser()

    queue = Queue()
    queue.put(Path(source_page))

    while not queue.empty():
        cur_path = queue.get()
        print("Processing: " + cur_path.get_current_page())

        for next_page in parser.get_links(cur_path.get_current_page()):

            if next_page is destination_page:
                complete_path = cur_path.spawn_child(next_page)
                print("Found it after: " + complete_path.get_size() + " links.\n\t" + complete_path.to_string)
                break

            if not cur_path.has_visited(next_page):
                queue.put(cur_path.spawn_child(next_page))
