from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
import requests


class NPMSearch(Extension):

    def __init__(self):
        super().__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        items = []

        packages = event.query.split(" ")[1]
        query = "https://api.npms.io/v2/search?q={}".format(packages)
        response = requests.get(query).json()

        for i in range(10):
            items.append(ExtensionResultItem(icon='images/icon.png',
                                             name=response["results"][i]["package"]["name"],
                                             description=response["results"][i]["package"]["description"],
                                             on_enter=HideWindowAction()))

        return RenderResultListAction(items)

if __name__ == '__main__':
    NPMSearch().run()
