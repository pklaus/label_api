import imp
import os

MAIN_MODULE = "__init__"

class PluginNotFoundError(NameError):
    pass

def get_plugins(plugin_folder):
    plugins = []
    possible_plugins = os.listdir(plugin_folder)
    for i in possible_plugins:
        location = os.path.join(plugin_folder, i)
        if os.path.isdir(location) and (MAIN_MODULE + ".py") in os.listdir(location):
            name = i
            info = imp.find_module(MAIN_MODULE, [location])
        elif not os.path.isdir(location) and location.endswith(".py"):
            name = i.rpartition(".py")[0]
            info = imp.find_module(name, [plugin_folder])
        else:
            continue
        plugins.append({"name": name, "info": info})
    return plugins

def get_plugin_by_name(plugin_name, plugin_folder):
    for plugin in get_plugins(plugin_folder):
        if plugin['name'] == plugin_name:
            return load_plugin(plugin)
    raise PluginNotFoundError()

def load_plugin(plugin):
    try:
        return imp.load_module(plugin["name"], *plugin["info"])
    finally:
        fp = plugin["info"][0]
        if fp: fp.close()
