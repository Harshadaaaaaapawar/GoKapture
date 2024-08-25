def test_registration(client):
    response = client.post('/api/register', json={
        "username": "testuser",
        "password": "testpassword",
        "role": "User"
    })
    assert response.status_code == 201
    assert response.get_json()['message'] == "User registered successfully"

def test_login(client):
    client.post('/api/register', json={
        "username": "testuser",
        "password": "testpassword",
        "role": "User"
    })
    response = client.post('/api/login', json={
        "username": "testuser",
        "password": "testpassword"
    })
    assert response.status_code == 200
    assert 'access_token' in response.get_json()
