from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
import requests
import webbrowser

def clamp(n, smallest, largest): return max(smallest, min(n, largest))

class Inkdrop(Extension):

    def __init__(self):
        super().__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())

class ItemEnterEventListener(EventListener):

    def on_event(self, event, extension):
        # event is instance of ItemEnterEvent

        data = event.get_data()['noteId']

        # do additional actions here...
        webbrowser.open_new_tab('inkdrop://' + data.replace(':', '/'))

        return RenderResultListAction([])


class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        items = []
        prefs = extension.preferences
        noteKeyword = event.query.split(" ")[1]
        url = "http://{}:{}@{}:{}".format(prefs['inkdrop_username'], prefs['inkdrop_password'], prefs['inkdrop_host'], prefs['inkdrop_port'])
        query = url + "/notes?limit=20&keyword={}".format(noteKeyword)
        response = requests.get(query).json()

        for i in range(clamp(9, 0, len(response))):
            print(response[i])
            bookQ = url + "/books"
            res = requests.get(bookQ).json()
            book = [item for item in res if item.get('_id') == response[i]["bookId"]][0]['name']
            data = {'noteId': response[i]["_id"]}
            print(response[i])
            items.append(ExtensionResultItem(icon='images/icon.png',
                                             name=response[i]["title"],
                                             description=book,
                                             on_enter=ExtensionCustomAction(data, keep_app_open=False)))

        return RenderResultListAction(items)

if __name__ == '__main__':
    Inkdrop().run()
