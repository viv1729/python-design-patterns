"""
    @author      : Vivek Anand
    @create date : Mon, Jan 16, 2022, 23:55
    @modify date : Mon, Jan 17, 2022, 21:30
    @description : [description]
"""

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
    
    
    # this is an anti-pattern
    # we are adding save/load features i.e. persistance to the Journal class
    # if we have other classes, they would need similar functioanily and then we would be implementing similar methods for those classes as well
    # thus it's better to handle this is a separate class
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




            