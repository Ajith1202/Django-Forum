## DJANGO-FORUM

---

**Django Forum** is a REST API which serves endpoints for a Forum.

The main functionalities of this API are:

- User Login/Registration using [Token Authentication](https://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication)
  
- Create, Retrieve, Update, Delete a Post
  
- Vote (Upvote/Downvote) a Post
  
- Comment on a Post
  
  - Nested Commenting upto one level
    
- Add, Update Tags on a Post (using [django-taggit](https://github.com/jazzband/django-taggit))
  
- Search for posts based on tags
  

#### Setup

```bash
git clone https://github.com/Ajith1202/Django-Forum.git
cd Django-Forum
pip install pipenv
pipenv install
pipenv shell
```

#### Run the server

```bash
python manage.py runserver
```

---

### REST API

- User Registration
  
  - `POST /auth/registration/`
    
- User Login
  
  - `POST /auth/login/` 
    

- List all posts
  
  - `GET /api/posts/`
    
- Create a post
  
  - `POST /api/posts/`
    

- Retrieve a specific post
  
  - `GET /api/posts/<post_id>/`
    
- Update a specific post
  
  - `PUT /api/posts/<post_id>/`
    
- Delete a post
  
  - `DELETE /api/delete/<post_id>/`
    
- Vote for a post
  
  - `GET /api/posts/<post_id>/vote/<vote_type>/`
    
- List all Comments of a post
  
  - `GET /api/posts/<post_id>/comments/`
    
- Comment on a post
  
  - `POST /api/posts/<post_id>/comments/`
    
- Reply to a Comment
  
  - `POST /api/posts/<post_id>/comments/<comment_id>/reply/`
    
- Search for posts by tag
  
  - `GET /api/posts/search/<tag_name>/`

### Packages Used

- `python`
  
- `django`
  
- `djangorestframework`
  
- `django-rest-auth`
  
- `django-allauth`
  
- `django-taggit`