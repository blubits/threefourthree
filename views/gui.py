from .interface import Interface
from .pygletgui import PygletGUI


class GUIInterface(Interface):
	
	def __init__(self):
		super().__init__()

	def run(self):
		self.initialize_event_handlers()
		self.view_events.create(size = 6, initial_value = 3,
								initial_tiles = 8, win_condition = 10)
		self.gui = PygletGUI(self)
		self.gui.run()
		

