from deephaven.plugin import Registration

from .plugin import create_pt_plugin, PluginType

__version__ = "0.1.0"


class PluginRegistration(Registration):
    @classmethod
    def register_into(cls, callback: Registration.Callback) -> None:
        callback.register(PluginType)
