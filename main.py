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

class NPMSearch(Extension):

    def __init__(self):
        super().__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())

class ItemEnterEventListener(EventListener):

    def on_event(self, event, extension):
        # event is instance of ItemEnterEvent

        data = event.get_data()

        # do additional actions here...
        webbrowser.open_new_tab(data['url'])

        return RenderResultListAction([])


class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        items = []

        packages = event.query.split(" ")[1]
        query = "https://api.npms.io/v2/search?q={}".format(packages)
        response = requests.get(query).json()


        for i in range(clamp(9, 0, len(response["results"]))):
            data = {'url': response["results"][i]["package"]["links"]["npm"]}
            items.append(ExtensionResultItem(icon='images/icon.png',
                                             name=response["results"][i]["package"]["name"] + "@" + response["results"][i]["package"]["version"],
                                             description=response["results"][i]["package"]["description"],
                                             on_enter=ExtensionCustomAction(data, keep_app_open=False)))

        return RenderResultListAction(items)

if __name__ == '__main__':
    NPMSearch().run()
