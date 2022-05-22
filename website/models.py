from abc import ABC, abstractmethod
import traceback
from .settings import db_path
import sqlite3


class BaseModel(ABC):

    def __init__(self, id=None) -> None:
        self.id = id
        self.__isValid = True

    @property
    def isValid(self):
        return self.__isValid

    @isValid.setter
    def isValid(self, isValid):
        self.__isValid = isValid

    @abstractmethod
    def print():
        pass

    @abstractmethod
    def save(self):
        pass

    @abstractmethod
    def delete(self):
        pass

    @classmethod
    @abstractmethod
    def objects():
        pass

    @classmethod
    @abstractmethod
    def get_by_id(id):
        pass


class School(BaseModel):
    table = 'School'

    def __init__(self, name, id=None) -> None:
        super().__init__(id)
        self.name = name

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        if isinstance(name, str):
            self.__name = name
        else:
            self.__name = ''
            self.__isValid = False

    def print():
        pass

    def save(self):
        if self.isValid:
            try:
                with sqlite3.connect(db_path) as conn:
                    cursor = conn.cursor()
                    try:
                        if self.id is None:
                            # insert, create new object (row)
                            cursor.execute(f'''
                                INSERT INTO {School.table} ('Name')
                                VALUES ('{self.name}')
                            ''')
                            self.id = cursor.lastrowid
                        else:
                            # update existing row
                            conn.execute(f'''
                                UPDATE {School.table} set Name = '{self.name}' where Id = {self.id}
                            ''')

                            conn.commit()
                    except:
                        print('Saqlashda xatolik bo\'ldi')
                        conn.rollback()
                return True
            except:
                print('Bog\'lanishda xatolik')
        else:
            return False

    def delete(self):
        try:
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                query = f"""
                Delete From  {School.table} where Id = {self.id}
                """
                cursor.execute(query)
                conn.commit()
        except:
            print('Bog\'lanishda xatolik')

    def objects():
        try:
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                query = f"""
                Select *From  {School.table}
                """
                for row in cursor.execute(query):
                    yield School(row[1], row[0])
        except:
            raise
            print('Bog\'lanishda xatolik')

    def get_by_id(id):
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            query = f"""
                Select *From  {School.table}
                Where Id={id}
                """
            res = cursor.execute(query).fetchone()
            if res is not None:
                return School(res[1], res[0])
            else:
                return None

    def __str__(self):
        return f'{self.name}'


class Class(BaseModel):
    table = 'Class'

    def __init__(self, name, regionId, id=None) -> None:
        super().__init__(id)
        self.name = name
        self.regionId = regionId

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        if isinstance(name, str):
            self.__name = name
        else:
            self.__name = ''
            self.__isValid = False

    @property
    def schoolId(self):
        return self.__schoolId

    @schoolId.setter
    def regionId(self, schoolId):
        if isinstance(schoolId, int) and School.get_by_id(schoolId) is not None:
            self.__schoolId = schoolId
        else:
            self.__schoolId = None
            self.__isValid = False

    @property
    def school(self):
        return School.get_by_id(self.schoolId)

    def print():
        pass

    def save(self):
        if self.isValid:
            try:
                with sqlite3.connect(db_path) as conn:
                    cursor = conn.cursor()
                    try:
                        if self.id is None:
                            # insert, create new object (row)
                            cursor.execute(f'''
                                INSERT INTO {Class.table} ('Name', School_Id)
                                VALUES ('{self.name}', {self.schoolId})
                            ''')
                            self.id = cursor.lastrowid
                        else:
                            # update existing row

                            conn.execute(f'''
                                UPDATE {Class.table} set Name = '{self.name}', School_Id={self.schoolId} where Id = {self.id}
                            ''')

                            conn.commit()
                    except:
                        raise
                        print('Saqlashda xatolik bo\'ldi')
                        conn.rollback()
                return True
            except:
                raise
                print('Bog\'lanishda xatolik')
        else:
            return False

    def delete(self):
        try:
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                query = f"""
                Delete From  {Class.table} where Id = {self.id}
                """
                cursor.execute(query)
                conn.commit()
        except:
            raise
            print('Bog\'lanishda xatolik')

    def objects():
        try:
            print(db_path)
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                query = f"""
                Select *From  {Class.table}
                """
                for row in cursor.execute(query):
                    yield Class(row[1], row[2], row[0])
        except:
            raise
            print('Bog\'lanishda xatolik')

    def get_by_id(id):
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            query = f"""
                Select *From  {Class.table}
                Where Id={id}
                """
            res = cursor.execute(query).fetchone()
            if res is not None:
                return Class(res[1], res[2], res[0])
            else:
                return None

    def __str__(self):
        return f'{self.school}\t | {self.name}'


class Student(BaseModel):
    table = 'Student'

    def __init__(self, surname, name, marks, favorite_science,  neighborhood, classID, id=None) -> None:
        super().__init__(id)
        self.surname = surname
        self.name = name
        self.marks = marks
        self.favorite_science = favorite_science
        self.neighborhood = neighborhood
        self.classID = classID

    @property
    def surname(self):
        return self.__surname

    @surname.setter
    def surname(self, surname):
        if isinstance(surname, str):
            self.__surname = surname
        else:
            self.__surname = ''
            self.__isValid = False

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        if isinstance(name, str):
            self.__name = name
        else:
            self.__name = ''
            self.__isValid = False

    @property
    def marks(self):
        return self.__marks

    @marks.setter
    def marks(self, marks):
        if isinstance(marks, int):
            self.__marks = marks
        else:
            self.__marks = 0
            self.__isValid = False

    @property
    def favorite_science(self):
        return self.__favorite_science

    @favorite_science.setter
    def favorite_science(self, favorite_science):
        if isinstance(favorite_science, str):
            self.__favorite_science = favorite_science
        else:
            self.__favorite_science = 'xato'
            self.__isValid = False

    @property
    def neighborhood(self):
        return self.__neighborhood

    @neighborhood.setter
    def neighborhood(self, neighborhood):
        if isinstance(neighborhood, str):
            self.__neighborhood = neighborhood
        else:
            self.__neighborhood = ''
            self.__isValid = False

    @property
    def classID(self):
        return self.__classID

    @classID.setter
    def classID(self, classID):
        if isinstance(classID, int):
            self.__classID = classID
        else:
            self.__classID = 0
            self.__isValid = False

    @property
    def Class(self):
        return Class.get_by_id(self.classID)

    def del_by_id(id):
        try:
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                query = f"""
                Delete From  {Student.table} where Id = {id}
                """
                cursor.execute(query)
                conn.commit()
        except:
            raise
            print('Bog\'lanishda xatolik')

    def save(self):
        if self.isValid:
            try:
                with sqlite3.connect(db_path) as conn:
                    cursor = conn.cursor()
                    try:
                        if self.id is None:
                            # insert, create new object (row)
                            cursor.execute(f'''
                                INSERT INTO {Student.table} (Surname, Name, Marks, Favorite_Science, Neighborhood, ClassID)
                                 VALUES ('{self.surname}', '{self.name}', {self.marks}, '{self.favorite_science}', '{self.neighborhood}', {self.classID})
                            ''')
                            self.id = cursor.lastrowid
                        else:
                            # update existing row

                            conn.execute(f'''
                                UPDATE {Student.table} set
                                Surname = '{self.surname}',
                                Name = '{self.name}',
                                Marks = {self.marks},
                                Favorite_Science = '{self.favorite_science}',
                                Neighborhood = '{self.neighborhood}',
                                ClassID = {self.classID}
                                where Id = {self.id}
                            ''')

                            conn.commit()
                    except:
                        raise
                        print('Saqlashda xatolik bo\'ldi')
                        conn.rollback()
                        raise
                return True
            except:
                raise
                print('Bog\'lanishda xatolik')
                raise

        else:
            return False

    def delete(self):
        try:
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                query = f"""
                Delete From  {Student.table} where Id = {self.id}
                """
                cursor.execute(query)
                conn.commit()
        except:
            raise
            print('Bog\'lanishda xatolik')

    def objects():
        try:
            print(db_path)
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                query = f"""
                Select *From  {Student.table}
                """
                for row in cursor.execute(query):
                    yield Student(row[1], row[2], row[3], row[4], row[5], row[6], row[0])
        except:
            traceback.print_exc()
            print('Bog\'lanishda xatolik')

    def print():
        pass

    def get_by_id(id):
        pass
