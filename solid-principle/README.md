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
"Software entities ... should be open for extension, but closed for modification."


<hr>


### The Liskov substitution principle
"Functions that use pointers or references to base classes must be able to use objects of derived classes without knowing it."


<hr>

### The interface segregation principle
"Many client-specific interfaces are better than one general-purpose interface."


<hr>

### The dependency inversion principle
"Depend upon abstractions, [not] concretions."



