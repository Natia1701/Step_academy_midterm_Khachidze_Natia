import json
import os
from pathlib import Path


class Book():
    def __init__(self,title,author,year):
        self.title = title
        self.author = author
        self.year = year

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, new_title):
        if not new_title:
            raise ValueError("Title cannot be empty")
        self._title = new_title.strip()

    @property
    def year(self):
        return self._year

    @year.setter
    def year(self, new_year):
        try:
            year_int = int(new_year)
        except ValueError:
             raise ValueError("Publishing year must be a valid integer.")
        
        if year_int < 0:
            raise ValueError("Year must be a non-negative number.")
        self._year = year_int
     
    @property
    def author(self):
        return self._author
    
    @author.setter
    def author(self, author_str):
        if not author_str or not author_str.strip():     #იჭერს როგორც ' ' ასევე NOne (თუ არაფერს შევიყვანთ)
             raise ValueError("Author cannot be empty.")
        self._author = author_str.strip()

    def __str__(self):
        return f"Title: {self._title} | Author: {self._author} | Year: {self._year}"
    
    def to_dict(self):
        return {
            "title": self._title,
            "author": self._author,
            "year": self._year
        }
    
class Bookmanager():
    def __init__(self):
        self.books = []
    
    def add_book(self,title,author,year):
        try:     
            new_book = Book(title.strip(),author.strip(),year)
            self.books.append(new_book)
            print(f"The book {new_book.title} added successfully.")
            return True
        except ValueError as e:
            print("Error: ", e)
            return False
        except Exception as e:
            print("Unexpected error: ", e)
            return False
    
    def all_books(self):
        if not self.books:
            print("Library is empty.")
        
        print(f"{' '*5} List of Books ")
        for i, book in enumerate(self.books, 1):    #enumarate() ფუნქციით უფრო სწრაფად ხდება გადანომრა და დანომვრა იწყება 1-დან
            print(f"{i}.  {book}")


    def search_book_by_title(self, target_title):
        target_title = target_title.lower().strip()
        found_books = []
        for book in self.books:
            if target_title in book.title.lower():
                found_books.append(book)
        return found_books
    
    def load_books(self, filepath):
        if not Path(filepath).exists():
            print("The file does not exist.")
            try:
                with open(filepath, 'w', encoding='utf-8') as file:
                    json.dump([], file, indent=4) 
                print(f"New file'{Path(filepath).name}' create successfully.")
            except Exception as e:
                print(f"Error: {e}")
                return

        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                data = json.load(file)
                
                if data: 
                    for item in data:
                        self.add_book(      #ამ მეთოდით Json ფაილიდან წამოღებული მონაცემები გაივლიან BOOK კლასის ვალიდაციას და არ ჩაიტვირთება დაზიანებული მონაცემი
                            title=item['title'], 
                            author=item['author'], 
                            year=item['year']
                        )
            
            if not self.books:
                print("The library is empty")
                
        except json.JSONDecodeError:
            print(f"File is damaged. Starting with an empty list.")
        except Exception as e:
            print(f"Unexpected Error: {e}")
    
    def save_books(self, filepath):
        data_to_save = [book.to_dict() for book in self.books]  
        
        try:
            with open(filepath, 'w', encoding='utf-8') as file:
                json.dump(data_to_save, file, ensure_ascii=False, indent=4) 
        except Exception as e:
            print(f"Error: {e}")

def get_file_path(filename="library.json"):
    try: 
        base_dir = Path(__file__).resolve().parent
    except NameError:
        base_dir = Path(os.getcwd())
        
    file_path = base_dir / filename
    return file_path


def main():
    manager = Bookmanager()
    my_file = "library.json"
    filepath = get_file_path(my_file) 
    manager.load_books(filepath)
    
    while True:
        print(f'{' '*6} The library ')
        print("1. add book")
        print("2. search book")
        print("3. Show books")
        print("4. exit")

        answer = input("please enter number of operation - ").strip()

        if answer == '1':
            title = input("Please enter title-").strip()
            author = input("Please enter Author -").strip()
            year = input("pPlease enter year -").strip()
                
            manager.add_book(title,author,year)
        elif answer == '2':
            title = input("Please enter title - ").strip()

            results = manager.search_book_by_title(title)
            if results:
                for i, book in enumerate(results, 1):
                    print(f"[{i}]. {book}") 
            else:
                print("No books found matching the title.")
        elif answer == '3':
            manager.all_books()
        elif answer == '4':
            manager.save_books(filepath)
            print("Good Bye.")
            break
        else:
            print("Invalid input. please try again. ")
            continue

if __name__ == "__main__":
    main()
