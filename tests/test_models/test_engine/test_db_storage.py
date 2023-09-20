#!/usr/bin/python3
"""
Module for unittesting the database file storage.

This module contains unit tests for the methods and functionality of the
database file storage system. It tests the integration of the database storage
with the User class and various database operations.
"""
import unittest
import MySQLdb
import os
from datetime import datetime
from models import storage
from models.user import User


@unittest.skipIf(
    os.getenv('HBNB_TYPE_STORAGE') != 'db', 'DBStorage test')
class TestDBStorage(unittest.TestCase):
    """Defines unit tests for the database storage methods"""

    def test_new(self):
        """Test if a new object is correctly added to the database"""
        new_obj = User(
            email='test0x00@mail.com',
            password='password',
            first_name='Monty',
            last_name='Python'
        )
        self.assertFalse(new_obj in storage.all().values())
        new_obj.save()
        self.assertTrue(new_obj in storage.all().values())
        db_connect = MySQLdb.connect(
            host=os.getenv('HBNB_MYSQL_HOST'),
            port=3306,
            user=os.getenv('HBNB_MYSQL_USER'),
            passwd=os.getenv('HBNB_MYSQL_PWD'),
            db=os.getenv('HBNB_MYSQL_DB')
        )
        cursor = db_connect.cursor()
        cursor.execute('SELECT * FROM users WHERE id="{}"'.format(new_obj.id))
        output = cursor.fetchone()
        self.assertTrue(output is not None)
        self.assertIn('test0x00@mail.com', output)
        self.assertIn('password', output)
        self.assertIn('Monty', output)
        self.assertIn('Python', output)
        cursor.close()
        db_connect.close()

    def test_save(self):
        """Test if the object is successfully saved to the database"""
        new_obj = User(
            email='test0x00@mail.com',
            password='password',
            first_name='Monty',
            last_name='Python'
        )

        db_connect = MySQLdb.connect(
            host=os.getenv('HBNB_MYSQL_HOST'),
            port=3306,
            user=os.getenv('HBNB_MYSQL_USER'),
            passwd=os.getenv('HBNB_MYSQL_PWD'),
            db=os.getenv('HBNB_MYSQL_DB')
        )
        cursor = db_connect.cursor()
        cursor.execute('SELECT * FROM users WHERE id="{}"'.format(new_obj.id))
        output = cursor.fetchone()
        cursor.execute('SELECT COUNT(*) FROM users;')
        old_cnt = cursor.fetchone()[0]
        self.assertTrue(output is None)
        self.assertFalse(new_obj in storage.all().values())

        new_obj.save()
        db_connect1 = MySQLdb.connect(
            host=os.getenv('HBNB_MYSQL_HOST'),
            port=3306,
            user=os.getenv('HBNB_MYSQL_USER'),
            passwd=os.getenv('HBNB_MYSQL_PWD'),
            db=os.getenv('HBNB_MYSQL_DB')
        )
        cursor1 = db_connect1.cursor()
        cursor1.execute('SELECT * FROM users WHERE id="{}"'.format(new_obj.id))
        output = cursor1.fetchone()
        cursor1.execute('SELECT COUNT(*) FROM users;')
        new_cnt = cursor1.fetchone()[0]
        self.assertFalse(output is None)
        self.assertEqual(old_cnt + 1, new_cnt)
        self.assertTrue(new_obj in storage.all().values())
        cursor1.close()
        db_connect1.close()
        cursor.close()
        db_connect.close()

    def test_delete(self):
        """Test if an object is correctly deleted from the database"""
        new_obj = User(
            email='test0x00@mail.com',
            password='password',
            first_name='Monty',
            last_name='Python'
        )
        obj_key = 'User.{}'.format(new_obj.id)
        db_connect = MySQLdb.connect(
            host=os.getenv('HBNB_MYSQL_HOST'),
            port=3306,
            user=os.getenv('HBNB_MYSQL_USER'),
            passwd=os.getenv('HBNB_MYSQL_PWD'),
            db=os.getenv('HBNB_MYSQL_DB')
        )
        new_obj.save()
        self.assertTrue(new in storage.all().values())
        cursor = db_connect.cursor()
        cursor.execute('SELECT * FROM users WHERE id="{}"'.format(new_obj.id))
        output = cursor.fetchone()
        self.assertTrue(output is not None)
        self.assertIn('test0x00@mail.com', output)
        self.assertIn('password', output)
        self.assertIn('Monty', output)
        self.assertIn('Python', output)
        self.assertIn(obj_key, storage.all(User).keys())
        new_obj.delete()
        self.assertNotIn(obj_key, storage.all(User).keys())
        cursor.close()
        db_connect.close()

    def test_reload(self):
        """Test the reloading of the database session"""
        db_connect = MySQLdb.connect(
            host=os.getenv('HBNB_MYSQL_HOST'),
            port=3306,
            user=os.getenv('HBNB_MYSQL_USER'),
            passwd=os.getenv('HBNB_MYSQL_PWD'),
            db=os.getenv('HBNB_MYSQL_DB')
        )
        cursor = db_connect.cursor()
        cursor.execute(
            'INSERT INTO users(id, created_at, updated_at, email, password' +
            ', first_name, last_name) VALUES(%s, %s, %s, %s, %s, %s, %s);',
            [
                '00x01',
                str(datetime.now()),
                str(datetime.now()),
                'test@mail.com',
                'passwd',
                'Monty',
                'Python',
            ]
        )
        self.assertNotIn('User.00x01', storage.all())
        db_connect.commit()
        storage.reload()
        self.assertIn('User.00x01', storage.all())
        cursor.close()
        db_connect.close()

    def test_storage_type_created(self):
        """Test if the DBStorage object storage is created"""
        from models.engine.db_storage import DBStorage
        self.assertEqual(type(storage), DBStorage)

    def test_new_save(self):
        """test the new and save methods"""
        db = MySQLdb.connect(user=os.getenv('HBNB_MYSQL_USER'),
                             host=os.getenv('HBNB_MYSQL_HOST'),
                             passwd=os.getenv('HBNB_MYSQL_PWD'),
                             port=3306,
                             db=os.getenv('HBNB_MYSQL_DB'))
        new_user = User(**{'first_name': 'Monty',
                           'last_name': 'Python',
                           'email': 'test@mail.com',
                           'password': 12345})
        cur = db.cursor()
        cur.execute('SELECT COUNT(*) FROM users')
        old_record = cur.fetchall()
        cur.close()
        db.close()
        new_user.save()
        db = MySQLdb.connect(user=os.getenv('HBNB_MYSQL_USER'),
                             host=os.getenv('HBNB_MYSQL_HOST'),
                             passwd=os.getenv('HBNB_MYSQL_PWD'),
                             port=3306,
                             db=os.getenv('HBNB_MYSQL_DB'))
        cur = db.cursor()
        cur.execute('SELECT COUNT(*) FROM users')
        new_record = cur.fetchall()
        self.assertEqual(new_record[0][0], old_record[0][0] + 1)
        cur.close()
        db.close()


if __name__ == '__main__':
    unittest.main()
