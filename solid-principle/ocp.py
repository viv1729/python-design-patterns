"""
    @author      : Vivek Anand
    @create date : Mon, Jan 17, 2022, 21:35
    @modify date : Mon, Jan 17, 2022, 22:45
    @description : [description]
"""

from enum import Enum

class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3

class Size(Enum):
    SMALL = 1
    MEDIUM = 2
    LARGE = 3
    
class Product():
    def __init__(self, name, color, size) -> None:
        self.name = name
        self.color = color
        self.size = size
        
    
# let's say we need to filter product by color
class FilterProduct:
    def filter_by_color(self, products, color):
        for p in products:
            if p.color == color:
                yield p
        
    # now let's say, later, we want to filter products by size too and hence add the following method
    # this violated the open-closed principle as we have modified the class rather than extending it
    # since these filter addition can keep on going, say filter by both color and size, filter by color or size 
    def filter_by_size(self, products, size):
        for p in products:
            if p.size == size:
                yield p
                
                
    def filter_by_size_and_color(self, products, size, color):
        for p in products:
            if p.size == size and p.color == color:
                yield p
        
        
    # this also causes state space explosion
    # 2 features -> 3 possible filter method with and
    # 3 features -> 7 possible filter method with and
    

# Apart from Design-patterns there are Enterprise patterns and one of those is Specification which we need here  
# Specification will be a base class that determines if a particular item satisfies as particular criteria 
class BaseSpecification:
    def is_satisfied(self, item):
        pass
    
    # support & for creating specs, this overloads "&" not "and" 
    # we need this __and__ in BaseSpecification coz we will be applying it on BaseSpecification classes like ColorSpecification, SizeSpecification
    def __and__(self, other):
        return AndSpecification(self, other)
    
    
# base class that takes items and the spec to filter upon
class BaseFilter:
    def filter(self, items, spec):
        pass

# now if we want to filter by some critera(s), we simply extend these classes
class ColorSpecification(BaseSpecification):
    def __init__(self, color) -> None:
        self.color = color
    
    def is_satisfied(self, item):
        return item.color == self.color
    

class SizeSpecification(BaseSpecification):
    def __init__(self, size) -> None:
        self.size = size
            
    def is_satisfied(self, item):
        return item.size == self.size


# And Specification
class AndSpecification(BaseSpecification):
    def __init__(self, *args) -> None:
        self.specs = args

    # return true only if all specs are satisfied for the item
    def is_satisfied(self, item):
        return all(map(
            lambda spec: spec.is_satisfied(item), self.specs 
        ))


class Filter(BaseFilter):
    # why we are defining filter here and not in BaseFilter?
    # that's coz it will allow us to implement different types of filtering 
    # for e.g. we are assuming items to be iterable which might not always hold and in that case we will extend BaseFilter to handle it
    def filter(self, items, spec):
        for item in items:
            if spec.is_satisfied(item):
                yield item
                
             
if __name__ == "__main__":
    apple = Product("Apple", Color.GREEN, Size.SMALL)
    tree = Product("Tree", Color.GREEN, Size.LARGE)
    house = Product("House", Color.BLUE, Size.LARGE)
    
    products = [apple, tree, house]

    
    # old approach
    fp = FilterProduct()
    print('Green products (old approach): ')
    for p in fp.filter_by_color(products, Color.GREEN):
        print(f'\t{p.name} is green')
        
    
    # new approach
    fp_new = Filter()
    green_spec = ColorSpecification(Color.GREEN)
    
    print('\nGreen products (new approach): ')
    for p in fp_new.filter(products, green_spec):
        print(f'\t{p.name} is green')
        
    
    # combining filters
    green_and_large_spec = AndSpecification(green_spec, SizeSpecification(Size.LARGE))
    
    print('\nGreen and Large products (new approach): ')
    for p in fp_new.filter(products, green_and_large_spec):
        print(f'\t{p.name} is green and large')
        
        
    # combining filters using & operator
    green_and_large_spec2 = green_spec & SizeSpecification(Size.LARGE)
    
    print('\nGreen and Large products (new approach): ')
    for p in fp_new.filter(products, green_and_large_spec2):
        print(f'\t{p.name} is green and large')
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        
    
