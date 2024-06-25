from models.image_ops import get_image_metadata
def main():
    image_path = '..\\resources\images\\ride.jpg'
    metadata = get_image_metadata(image_path)
    for key, value in metadata.items():
        print(f'{key}: {value}')

if __name__ == "__main__":
    main()

