import abc

from typing import List


class MenuConsumation(abc.ABC):  # (abstract) Component
    
    @abc.abstractmethod
    def get_price(self) -> float:
        pass
    
    def __repr__(self) -> str:
        return "{} ({} $)".format(self.__class__.__name__, self.get_price())
    

class CheeseBurger(MenuConsumation):  # ConcreteComponent
    
    def get_price(self) -> float:
        return 2.5
    

class FrenchFries(MenuConsumation):  # ConcreteComponent
    
    def get_price(self) -> float:
        return 2.0


class ConsumationWithExtra(MenuConsumation):  # (abstract) Decorator
    
    def __init__(self, consumation: MenuConsumation):
        self.consumation = consumation
    
    def get_price(self) -> float:
        return self.consumation.get_price()
    
    def __repr__(self) -> str:
        return "{} + {}".format(repr(self.consumation), super().__repr__())
    

class ExtraMaionnaise(ConsumationWithExtra):  # ConcreteDecorator

    def __init__(self, consumation: MenuConsumation):
        super().__init__(consumation)
        
    def get_price(self) -> float:
        return super().get_price() + 0.7
    

class ExtraKetchup(ConsumationWithExtra):  # ConcreteDecorator
    
    def __init__(self, consumation: MenuConsumation):
        super().__init__(consumation)
        
    def get_price(self) -> float:
        return super().get_price() + 0.6
    

class ShopClient:
    
    def __init__(self) -> None:
        self.order: List[MenuConsumation] = []
        
    def add_consumation(self, consumation: MenuConsumation) -> None:
        self.order.append(consumation)
    
    def print_order(self) -> None:
        print("Order: {}".format(self.order))
        
    def print_total(self) -> None:
        print("Total: {} $".format(sum([c.get_price() for c in self.order])))
        

def main() -> None:
    shop = ShopClient()
    shop.add_consumation(ExtraMaionnaise(FrenchFries()))
    shop.add_consumation(ExtraMaionnaise(ExtraKetchup(CheeseBurger())))
    shop.print_order()
    # Order: [FrenchFries (2.0 $) + ExtraMaionnaise (2.7 $), CheeseBurger 
    # (2.5 $) + ExtraKetchup (3.1 $) + ExtraMaionnaise (3.8 $)]
    shop.print_total()
    # Total: 6.5 $


if __name__ == "__main__":
    main()
