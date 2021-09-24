from DAVE import *


class Balloon(Manager):
    """A balloon is a hot-air balloon with a rope"""

    def __init__(self, scene, name):

        scene._verify_name_available(name)

        super().__init__(scene)
        self._name = name

        self.axis = scene.new_frame(name + '_balloon_body', fixed=[False, False, False, True, True, True])
        self.axis.manager = self

        self._balloon_size = 30

        self._scene._nodes.append(self)

    @property
    def balloon_size(self):
        return self._balloon_size

    @balloon_size.setter
    def balloon_size(self, value):
        self._balloon_size = value

    @property
    def nodes(self):
        return [self.axis]

    def managed_nodes(self):
        return self.nodes

    def creates(self, node: Node):
        return node in self.nodes

    def delete(self):
        with ClaimManagement(self._scene, self):
            for n in self.nodes:
                self._scene.delete(n)

    def depends_on(self) -> list:
        return []

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        super().name = value


# Add the balloon class to the modules that are available when executing code

from DAVE.settings import DAVE_ADDITIONAL_RUNTIME_MODULES
DAVE_ADDITIONAL_RUNTIME_MODULES['Balloon'] = Balloon


def new_balloon(scene, name):
    b = Balloon(scene=scene, name=name)



