def test_health_check(client):
    """Test health check endpoint under /usecases/health/"""
    response = client.get("/usecases/health/")
    assert response.status_code == 200
    assert response.json == {"status": "ok"}
