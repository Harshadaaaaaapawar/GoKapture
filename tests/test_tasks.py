def test_create_task(client):
    client.post('/api/register', json={
        "username": "testuser",
        "password": "testpassword"
    })
    login_response = client.post('/api/login', json={
        "username": "testuser",
        "password": "testpassword"
    })
    token = login_response.get_json()['access_token']

    response = client.post('/api/tasks', json={
        "title": "New Task",
        "description": "Task description",
        "status": "Todo",
        "priority": "High",
        "due_date": "2024-08-30"
    }, headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 201
    assert response.get_json()['message'] == "Task created successfully"

def test_get_tasks(client):
    client.post('/api/register', json={
        "username": "testuser",
        "password": "testpassword"
    })
    login_response = client.post('/api/login', json={
        "username": "testuser",
        "password": "testpassword"
    })
    token = login_response.get_json()['access_token']

    client.post('/api/tasks', json={
        "title": "Task 1",
        "description": "Description 1",
        "status": "Todo",
        "priority": "High"
    }, headers={"Authorization": f"Bearer {token}"})

    client.post('/api/tasks', json={
        "title": "Task 2",
        "description": "Description 2",
        "status": "In Progress",
        "priority": "Medium"
    }, headers={"Authorization": f"Bearer {token}"})

    response = client.get('/api/tasks?page=1&per_page=1', headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.get_json()
    assert len(data['tasks']) == 1
    assert data['total'] == 2
    assert data['pages'] == 2
