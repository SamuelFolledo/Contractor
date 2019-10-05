# tests.py

from unittest import TestCase, main as unittest_main, mock
from bson.objectid import ObjectId
from app import app

sample_user_id = ObjectId('5d55cffc4a3d4031f42827a3')
sample_user = {
    'user_name': 'Kobe Bryant',
    'user_description': 'Best player in the NBA',
    'user_rating': 5
    # 'videos': [
    #     'https://youtube.com/embed/hY7m5jjJ9mM',
    #     'https://www.youtube.com/embed/CQ85sUNBK7w'
    # ]
}
sample_form_data = {
    'user_name': sample_user['user_name'],
    'user_description': sample_user['user_description'],
    'user_rating': int(sample_user['user_rating'])
    # 'videos': '\n'.join(sample_user['videos'])
}

class UsersTests(TestCase):

    def setUp(self): #SET UP
        self.client = app.test_client()
        app.config['TESTING'] = True # Show Flask errors that happen during tests

    def test_index(self): #test home page
        result = self.client.get('/')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'User', result.data)

    def test_new(self): #test new
        result = self.client.get('/users/new')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'New User', result.data)

    @mock.patch('pymongo.collection.Collection.find_one')
    def test_show_user(self, mock_find):
        """Test showing a single user."""
        mock_find.return_value = sample_user

        result = self.client.get(f'/users/{sample_user_id}')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'Kobe Bryant', result.data)

    @mock.patch('pymongo.collection.Collection.find_one')
    def test_edit_user(self, mock_find):
        """Test editing a single user."""
        mock_find.return_value = sample_user
        result = self.client.get(f'/users/{sample_user_id}/edit')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'Kobe Bryant', result.data)

    @mock.patch('pymongo.collection.Collection.insert_one')
    def test_submit_user(self, mock_insert):
        """Test submitting a new user."""
        result = self.client.post('/users', data=sample_form_data)
        # After submitting, should redirect to that user's page
        self.assertEqual(result.status, '302 FOUND')
        mock_insert.assert_called_with(sample_user)

    @mock.patch('pymongo.collection.Collection.update_one')
    def test_update_user(self, mock_update):
        result = self.client.post(f'/users/{sample_user_id}', data=sample_form_data)
        self.assertEqual(result.status, '302 FOUND')
        mock_update.assert_called_with({'_id': sample_user_id}, {'$set': sample_user})

    @mock.patch('pymongo.collection.Collection.delete_one')
    def test_delete_user(self, mock_delete):
        form_data = {'_method': 'DELETE'}
        result = self.client.post(f'/users/{sample_user_id}/delete', data=form_data)
        self.assertEqual(result.status, '302 FOUND')
        mock_delete.assert_called_with({'_id': sample_user_id})


if __name__ == '__main__':
    unittest_main()