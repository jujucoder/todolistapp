
from urllib import response
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from todos.models import Todo

# Create your tests here.


class TodosApiTestCase(APITestCase):
    def create_todo(self):
       sample_todo={'title':'hello','desc':'nothing to do'}
       response=self.client.post(reverse('todos'),sample_todo)
       return response

    def authenticate(self):
        self.client.post(
            reverse("register"),
            {
                "username": "username",
                "email": "email@gmail.com",
                "password": "password",
            },
        )

        response = self.client.post(
            reverse("login"), {"email": "email@gmail.com", "password": "password"}
        )

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['token']}")
    



class TestListCreateTodos(TodosApiTestCase):

    def test_should_not_create_todo_with_no_auth(self):
        response=self.create_todo()
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)

    def test_should_create_todo(self):
        previous_todo_count=Todo.objects.all().count()
        self.authenticate()
        response=self.create_todo()
        self.assertEqual(Todo.objects.all().count(),previous_todo_count+1)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)  
        self.assertEqual(response.data['title'],'hello')  
        self.assertEqual(response.data['desc'],'nothing to do')  

    def test_retrieves_all_todos(self):
        self.authenticate()
        response=self.client.get(reverse('todos'))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertIsInstance(response.data['results'],list)
        self.create_todo()
        res=self.client.get(reverse('todos'))
        self.assertIsInstance(res.data['count'],int)
        self.assertEqual(res.data['count'],1)


class TestTodoDetailApiView(TodosApiTestCase):


        def test_retrieves_one_item(self):
            self.authenticate()
            response=self.create_todo()


            res=self.client.get(reverse('todo',kwargs={'id':response.data['id']}))

            self.assertEqual(res.status_code,status.HTTP_200_OK)

            todo=Todo.objects.get(id=response.data['id'])
            self.assertEqual(todo.title,res.data['title'])

            


        def test_deletes_one_item(self):
            self.authenticate()
            response=self.create_todo()
            prev_db_count=Todo.objects.all().count()
            self.assertGreater(prev_db_count,0)
            self.assertEqual(prev_db_count,1)
            res=self.client.delete(reverse('todo',kwargs={'id':response.data['id']}))
            self.assertEqual(res.status_code,status.HTTP_204_NO_CONTENT)
            self.assertEqual(Todo.objects.all().count(),0)


        def test_updates_one_item(self):
            self.authenticate()
            response=self.create_todo()
            res=self.client.patch(reverse('todo',kwargs={'id':response.data['id']}),{
                'title':'new one',
                'desc':'nee new',
                'is_complete':True
            })
            updated_todo=Todo.objects.get(id=response.data['id'])
            self.assertEqual(res.status_code,status.HTTP_200_OK)
            self.assertEqual(updated_todo.is_complete,True)
            self.assertEqual(updated_todo.title,'new one')
