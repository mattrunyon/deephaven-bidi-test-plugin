import json
from deephaven.table_listener import listen
from deephaven.plugin.object import Exporter, ObjectType, BidiObjectBase

NAME = "test.plugin"


def create_pt_plugin(pt):
    return PluginObject(pt)


class PluginObject(BidiObjectBase):
    def __init__(self, pt):
        BidiObjectBase.__init__(self)
        self.pt = pt
        self.pt_listener = listen(pt.table, self.listener)
        self.msg = None

    def start(self):
        self.pt_listener.start()

    def stop(self):
        self.pt_listener.stop()

    def handle_message(self, msg: bytes, objects: list[object]):
        payload = json.loads(msg.decode())
        print(payload)
        key = payload.get('key')
        if key is not None:
            if self.pt.get_constituent(key) is not None:
                print("Partitioned table has a constituent for key:", key)

    def listener(self, update, _):
        # Sometimes the reference is None. Race condition?
        # I think the listener is triggered before the client establishes a connection, so there's no ExportCollector
        # Maybe reference needs to return a default w/ a -1 index to indicate something is up
        added = [getattr(self.reference(t), 'index', None) for t in update.added().get('__CONSTITUENT__', [])]
        removed = [getattr(self.reference(t), 'index', None) for t in update.removed().get('__CONSTITUENT__', [])]
        self.send_message(json.dumps({
            "added": added,
            "removed": removed
        }))

    def to_bytes(self, exporter):
        return json.dumps({
            "tables": [exporter.reference(t).index for t in self.pt.constituent_tables]
        }).encode()


class PluginType(ObjectType):
    @property
    def name(self) -> str:
        return NAME

    def is_type(self, object) -> bool:
        return isinstance(object, PluginObject)

    def to_bytes(self, exporter: Exporter, obj: PluginObject) -> bytes:
        return obj.to_bytes(exporter)