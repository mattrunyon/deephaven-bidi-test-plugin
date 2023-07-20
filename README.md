# Deephaven Bidi Test Plugin

This plugin emits events when the partitions in a partitioned table change. The example code here creates a ticking table with 13 possible partitions, but tailed to 10 rows so there are always partitions ticking in/out.

## Build

To create your build / development environment:

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip setuptools build
```

To build:

```sh
python -m build --wheel
```

produces the wheel into `dist/`.

## Use

```python
from deephaven import time_table

t = time_table("PT1S").update("X = ii % 13").tail(10)
partition_table = t.partition_by("X")
pt_plugin = create_pt_plugin(partition_table) # Listener will start automatically

# Stop listener
# pt_plugin.stop()

# Restart listener
# pt_plugin.start()
```

Recommend using with the dashboard-object-viewer JS plugin. That plugin will log `Object fetched: JsWidget` to the browser console when `pt_plugin` is created.
You can then save as a global temp variable in the JS console and use the following.

```js
temp1.addEventListener(dh.Widget.EVENT_MESSAGE, ({ detail }) => console.log(detail));
temp1.sendMessage("Hello");
```
