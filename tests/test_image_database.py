import pytest
from src.database.image_db import ImageDatabase

@pytest.fixture(scope='module')
def database():
    db = ImageDatabase(':memory:')
    yield db
    db.close()

def test_connection(database):
    assert database.conn is not None

def test_add_image(database):
    database.add_image('/images/photo1.jpg', 'photo1.jpg', '{"resolution": "1920x1080"}', 'This is a sample note')
    image = database.read_image('photo1.jpg')
    assert image is not None
    assert image['filename'] == 'photo1.jpg'

def test_find_images_by_tag(database):
    database.add_image('/images/photo4.jpg', 'photo4.jpg', '{"resolution": "1920x1080"}', 'This is a sample note')
    database.add_image('/images/photo5.jpg', 'photo5.jpg', '{"resolution": "1080x720"}', 'Another note')
    database.add_image('/images/photo6.jpg', 'photo6.jpg', '{"resolution": "2048x1536"}', 'Third note')

    database.add_tag('vacation')
    database.add_tag('family')

    database.add_image_tag('photo4.jpg', 'vacation')
    database.add_image_tag('photo5.jpg', 'vacation')
    database.add_image_tag('photo6.jpg', 'family')
    images = database.find_images_by_tag('vacation')
    assert len(images) == 2
    images = database.find_images_by_tag('family')
    assert len(images) == 1
