**Topic of contents**
- [The single-responsibility principle](#the-single-responsibility-principle)
- [The open–closed principle](#the-openclosed-principle)
- [The Liskov substitution principle](#the-liskov-substitution-principle)
- [The interface segregation principle](#the-interface-segregation-principle)
- [The dependency inversion principle](#the-dependency-inversion-principle)

<br>

Following are the 5 SOLID design principles (definitions are taken from [Wikipedia](https://en.wikipedia.org/wiki/SOLID)):

### The single-responsibility principle
"There should never be more than one reason for a class to change." In other words, every class should have only one responsibility. This is also known as separation of concerns. Following sample displays this effect:

```python
from typing import Union, Any

class Journal:
    """
    currently this class does only 1 thing i.e. managing entries - logging, deleting and displaying
    """
    def __init__(self):
        self.entries = []
        self.count = 0
        
    def add_entry(self, note: str):
        self.count += 1
        self.entries.append(f"{self.count}. {note}")
    
    def remove_entry(self, pos: int):
        del self.entries[pos]
        
    def __str__(self) -> str:
        return "\n".join(self.entries)
    
    
    # this is an anti-pattern, when we try to add save/load features i.e. persistance to the Journal class
    # if we have other classes, they would need similar functioanily and then we would be implementing similar methods for those classes as well
    # thus it's better to handle this is a separate class - separation of concerns :)
    def save(self, file_path: str):
        pass
    
    def load(self, file_path: str):
        pass
    
    
class PersistanceManager:
    @staticmethod
    # can take any other type
    def save(journal: Union[Journal, Any], filename: str):
        with open(filename, "w") as f:
            f.write(str(journal))
    
    @staticmethod
    def load(filepath: str):
        with open(filepath, "r") as f:
            return f.read()


if __name__ == "__main__":
    j = Journal()
    j.add_entry("this is good.")          
    j.add_entry("hello world")
    print(j)

    # saving and loading journal
    journal_path = "journal.log"
    PersistanceManager.save(j, journal_path)
    print("\n loaded journal")
    print(PersistanceManager.load(journal_path))
```

<hr>

### The open–closed principle
"Software entities ... should be open for extension, but closed for modification." Following sample displays that how adding modifying the class to deliver new feature would result into state-space explosion. And, how we can use [Specification pattern](https://en.wikipedia.org/wiki/Specification_pattern#Python) to better solve the problem.

```python
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
        
        
# by adding filters for each case will cause state-space explosion
# 2 features -> 3 possible filter method with and
# 3 features -> 7 possible filter method with and


# Apart from Design-patterns there are Enterprise patterns and one of those is Specification which we can use here  
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
```

<hr>


### The Liskov substitution principle
"Functions that use pointers or references to base classes must be able to use objects of derived classes without knowing it."


<hr>

### The interface segregation principle
"Many client-specific interfaces are better than one general-purpose interface."


<hr>

### The dependency inversion principle
"Depend upon abstractions, [not] concretions."



