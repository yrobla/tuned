import tuned.patterns
import tuned.logs
import tuned.utils

log = tuned.logs.get()

class MonitorRepository(tuned.patterns.Singleton):
	def __init__(self):
		super(self.__class__, self).__init__()
		self._loader = tuned.utils.PluginLoader("tuned.monitors", "monitor_", tuned.monitors.Monitor)
		self._monitors = set()

	def create(self, plugin_name):
		log.debug("creating monitor %s" % plugin_name)
		# TODO: exception handling
		monitor_cls = self._loader.load(plugin_name)
		monitor_instance = monitor_cls()
		self._monitors.add(monitor_instance)
		return monitor_instance

	def delete(self, monitor):
		assert type(monitor) is self._loader.interface
		monitor.cleanup()
		self._monitors.remove(monitor)

	def update(self):
		for monitor in self._monitors:
			log.debug("updating %s")
			monitor.update()
