import pytest
from app.features.post import schemas

def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")
    print(res.json())
    #assert len(res.json()) == len(test_posts)
    assert res.status_code == 200

def test_unauth_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401

def test_unauth_user_get_one_posts(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401 
   
def test_auth_user_get_unexist_posts(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/8888")
    assert res.status_code == 404 

def test_get_one_posts(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    
    post = schemas.PostOut(**res.json())
    assert post.Post.id == test_posts[0].id
    assert post.Post.content == test_posts[0].content
    assert post.Post.title == test_posts[0].title

@pytest.mark.parametrize("title, content, published",[
    ("one t","one content",True),
    ("two t","two content",True),
    ("three t","three content",True)
])
def test_create_post(authorized_client, test_user,test_posts,title, content, published):
    res = authorized_client.post("/posts/",json={"title":title, "content":content, "published":published})

    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    #assert created_post.owner_id == test_user['id']

def test_create_post_default_publish(authorized_client, test_user,test_posts):
    res = authorized_client.post("/posts/",json={"title":"test t", "content":"test content"})

    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == "test t"
    assert created_post.content == "test content"
    assert created_post.published == True
    #assert created_post.owner_id == test_user['id']

def test_unauth_user_create_posts(client, test_posts):
    res = client.post("/posts/",json={"title":"test t", "content":"test content"})
    assert res.status_code == 401

def test_unauth_user_delete_posts(client, test_user, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 405

# def test_auth_user_delete_posts(authorized_client, test_user, test_posts):
#     res = authorized_client.delete(f"/posts/{test_posts[3].id}")
#     assert res.status_code == 204

# def test_auth_user_delete_non_exist_posts(authorized_client, test_user, test_posts):
#     res = authorized_client.delete("/posts/4566")
#     assert res.status_code == 401

# def test_auth_user_delete_other_user_posts(authorized_client, test_user, test_posts):
#     res = authorized_client.delete(f"/posts/{test_posts[3].id}")
#     assert res.status_code == 403

def test_update_post(authorized_client, test_user, test_posts):
    data = {"title":"update test t", "content":"updated test content", "id":test_posts[0].id}
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)  
    updated_post = schemas.Post(**res.json())
    assert res.status_code == 200
    assert updated_post.title == data["title"]

def test_update_other_user_post(authorized_client, test_user, test_user2, test_posts):
    data = {"title":"update test t", "content":"updated test content", "id":test_posts[3].id}
    res = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)    
    assert res.status_code == 403
   
def test_unauth_user_update_posts(client, test_user, test_posts):
    res = client.put(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_auth_user_update_non_exist_posts(authorized_client, test_user, test_posts):
    data = {"title":"update test t", "content":"updated test content", "id":test_posts[3].id}
    res = authorized_client.put(f"/posts/4566", json=data)
    assert res.status_code == 404