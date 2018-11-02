import abc

from enum import Enum
from typing import List


class UserType(Enum):
    USER = 1
    ADMIN = 2


class User:
    
    def __init__(self, user_type: UserType):
        self.user_type = user_type


class FileSystem(abc.ABC):  # Subject
    
    @abc.abstractmethod
    def list_files(self) -> List[str]:
        pass
    
    @abc.abstractmethod
    def create_file(self, name: str) -> bool:
        pass
    
    @abc.abstractmethod
    def remove_file(self, name: str) -> bool:
        pass


class OSFileSystem(FileSystem):  # RealSubject
    
    def __init__(self):
        self.files = set()
    
    def list_files(self) -> List[str]:
        return list(self.files)
    
    def create_file(self, name: str) -> bool:
        if name in self.files:
            return False
        self.files.add(name)
        return True
    
    def remove_file(self, name: str) -> bool:
        if name not in self.files:
            return False
        self.files.remove(name)
        return True


class AuthenticatedUserFileSystem(FileSystem):  # (protection) Proxy
    
    def __init__(self, user: User):
        self.user = user.user_type
        self.fs = OSFileSystem()
    
    def list_files(self) -> List[str]:
        return self.fs.list_files()

    def create_file(self, name: str) -> bool:
        return self.fs.create_file(name)
    
    def remove_file(self, name: str) -> bool:
        if self.user is UserType.USER:
            print("User unauthorized to remove file {}.".format(name))
            return False
        return self.fs.remove_file(name)


class Client:
    
    def __init__(self, fs: FileSystem):
        self.fs = fs
        
    def list_files(self) -> None:
        print(self.fs.list_files())

    def create_file(self, name: str) -> None:
        if self.fs.create_file(name):
            print("File {} created successfully.".format(name))
        else:
            print("Unable to create file {}.".format(name))
    
    def remove_file(self, name: str) -> None:
        if self.fs.remove_file(name):
            print("File {} removed successfully.".format(name))
        else:
            print("Unable to remove file {}.".format(name))


def main():
    aufs = AuthenticatedUserFileSystem(User(UserType.USER))
    user_client = Client(aufs)
    user_client.create_file("foo.txt")
    # File foo.txt created successfully.
    user_client.create_file("bar.txt")
    # File bar.txt created successfully.
    user_client.list_files()
    # ['bar.txt', 'foo.txt']
    user_client.remove_file("foo.txt")
    # User unauthorized to remove file foo.txt.
    # Unable to remove file foo.txt.
    
    aufs = AuthenticatedUserFileSystem(User(UserType.ADMIN))
    admin_client = Client(aufs)
    admin_client.create_file("foo.txt")
    # File foo.txt created successfully.
    admin_client.create_file("bar.txt")
    # File bar.txt created successfully.
    admin_client.list_files()
    # ['bar.txt', 'foo.txt']
    admin_client.remove_file("foo.txt")
    # File foo.txt removed successfully.


if __name__ == "__main__":
    main()
