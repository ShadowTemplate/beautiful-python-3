import abc

from typing import Optional


class VolumeController:  # Receiver
    
    def __init__(self, min_volume: int, max_volume: int):
        self.min_volume = min_volume
        self.max_volume = max_volume
        self.curr_volume = (max_volume + min_volume) // 2
        
    def raise_volume(self, increase: int) -> None:
        assert increase >= 0
        self.curr_volume = min(self.curr_volume + increase, self.max_volume)
        
    def decrease_volume(self, decrease: int) -> None:
        assert decrease >= 0
        self.curr_volume = max(self.curr_volume - decrease, self.min_volume)
        
    def boost_volume(self) -> None:
        self.curr_volume = self.max_volume
        
    def mute_volume(self) -> None:
        self.curr_volume = self.min_volume
        
    def __repr__(self):
        return "Volume: {}".format(self.curr_volume)


class VolumeCommand(abc.ABC):  # (abstract generic) Command
    
    def __init__(self, receiver: VolumeController):
        self.receiver = receiver
        
    @abc.abstractmethod
    def do_action(self) -> None:
        pass


class UndoableVolumeCommand(VolumeCommand):  # (abstract) Decorator
    
    def __init__(self, command: VolumeCommand):
        super().__init__(command.receiver)
        self.command = command

    @abc.abstractmethod
    def undo_action(self) -> None:
        pass


class SingleUndoCommand(UndoableVolumeCommand):  # ConcreteDecorator

    def __init__(self, command: VolumeCommand):
        super().__init__(command)
        self.prev_state: Optional[int] = None

    def do_action(self) -> None:
        self.prev_state = self.receiver.curr_volume
        self.command.do_action()
    
    def undo_action(self) -> None:
        if self.prev_state == None:
            raise RuntimeError("Unable to undo action.")
        assert isinstance(self.prev_state, int)
        self.receiver.curr_volume = self.prev_state
        self.prev_state = None

    
class RaiseVolumeCommand(VolumeCommand):  # ConcreteCommand
    
    def __init__(self, receiver: VolumeController, increment: int):
        super().__init__(receiver)
        self.increment = increment
        
    def do_action(self) -> None:
        self.receiver.raise_volume(self.increment)
        if self.receiver.curr_volume == self.receiver.max_volume:
            print("Attention: volume set to MAX.")


class DecreaseVolumeCommand(VolumeCommand):  # ConcreteCommand
    
    def __init__(self, receiver: VolumeController, decrement: int):
        super().__init__(receiver)
        self.decrement = decrement
        
    def do_action(self) -> None:
        self.receiver.decrease_volume(self.decrement)
        if self.receiver.curr_volume == self.receiver.min_volume:
            print("Attention: volume set to min.")


class BoostVolumeCommand(VolumeCommand):  # ConcreteCommand
    
    def __init__(self, receiver: VolumeController):
        super().__init__(receiver)
        
    def do_action(self) -> None:
        self.receiver.boost_volume()
        print("Attention: volume set to MAX.")


class MuteVolumeCommand(VolumeCommand):  # ConcreteCommand

    def __init__(self, receiver: VolumeController):
        super().__init__(receiver)
        
    def do_action(self) -> None:
        self.receiver.mute_volume()
        print("Attention: volume set to min.")
        

class GUIButton:  # Invoker
    
    def __init__(self, label: str, command: VolumeCommand):
        self.label = label
        self.command = command
        
    def on_click(self) -> None:
        print("Clicked: {}".format(self.label))
        self.command.do_action()
        
    def __repr__(self):
        return self.label
    

class UndoableGUIButton(GUIButton):  # Invoker
    
    def __init__(self, label: str, command: UndoableVolumeCommand):
        super().__init__(label, command)
        
    def cancel(self) -> None:
        assert isinstance(self.command, UndoableVolumeCommand)
        print("Canceled: {}".format(self.label))
        self.command.undo_action()
        
    def __repr__(self):
        return "U({})".format(self.label)


class VolumeControlGUI:  # Client
    
    def __init__(self):
        self.buttons = []
        self.last_index = None
        
    def add_button(self, button: GUIButton) -> None:
        self.buttons.append(button)
        
    def click(self, i: int) -> None:
        self.buttons[i].on_click()
        self.last_index = i
        
    def cancel(self) -> None:
        if self.last_index == None or self.last_index >= len(self.buttons):
            raise RuntimeError("Unable to cancel action.")
        
        last_button = self.buttons[self.last_index]
        if isinstance(last_button, UndoableGUIButton):
            last_button.cancel()
            self.last_button = None
        else:
            print("Unable to undo {}".format(last_button))
        
    def __repr__(self):
        return "GUI buttons: {}".format(self.buttons)


def main():
    volume_controller = VolumeController(0, 100)
    volume_controller_gui = VolumeControlGUI()
    
    add_30_command = RaiseVolumeCommand(volume_controller, 30)
    add_30_button = UndoableGUIButton("+30", SingleUndoCommand(add_30_command))
    volume_controller_gui.add_button(add_30_button)
    
    sub_30_command = DecreaseVolumeCommand(volume_controller, 30)
    sub_30_button = UndoableGUIButton("-30", SingleUndoCommand(sub_30_command))
    volume_controller_gui.add_button(sub_30_button)
    
    boost_command = BoostVolumeCommand(volume_controller)
    boost_button = GUIButton("MAX", boost_command)
    volume_controller_gui.add_button(boost_button)
    
    mute_command = MuteVolumeCommand(volume_controller)
    mute_button = GUIButton("min", mute_command)
    volume_controller_gui.add_button(mute_button)
    
    print(volume_controller_gui)
    # GUI buttons: [U(+30), U(-30), MAX, min]
    print(volume_controller)
    # Volume: 50
    volume_controller_gui.click(0)
    # Clicked: +30
    print(volume_controller)
    # Volume: 80
    volume_controller_gui.click(0)
    # Clicked: +30
    # Attention: volume set to MAX.
    print(volume_controller)
    # Volume: 100
    volume_controller_gui.cancel()
    # Canceled: +30
    print(volume_controller)
    # Volume: 80
    volume_controller_gui.click(3)
    # Clicked: min
    # Attention: volume set to min.
    print(volume_controller)
    # Volume: 0
    

if __name__ == "__main__":
    main()
