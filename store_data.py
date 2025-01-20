import mysql.connector
import os
from fetch_data import fetch_all_breeds, fetch_images_by_breed

def store_breeds_in_db(breeds):
    """Store all breeds in the MySQL database."""
    db_user = os.getenv('MYSQL_USER')
    db_password = os.getenv('MYSQL_PASSWORD')
    db_host = os.getenv('MYSQL_HOST', 'localhost')
    db_database = os.getenv('MYSQL_DATABASE', 'dog_project')

    conn = mysql.connector.connect(
        user=db_user,
        password=db_password,
        host=db_host,
        database=db_database
    )
    cur = conn.cursor()

    for breed in breeds:
        breed_id = breed['id']
        breed_name = breed['name']
        cur.execute("INSERT IGNORE INTO breeds (breed_id, breed_name) VALUES (%s, %s)", (breed_id, breed_name))

    conn.commit()
    cur.close()
    conn.close()
    print("Breeds stored successfully!")

def store_images_for_all_breeds():
    """Fetch and store images for all breeds in the database."""
    db_user = os.getenv('MYSQL_USER')
    db_password = os.getenv('MYSQL_PASSWORD')
    db_host = os.getenv('MYSQL_HOST', 'localhost')
    db_database = os.getenv('MYSQL_DATABASE', 'dog_project')

    conn = mysql.connector.connect(
        user=db_user,
        password=db_password,
        host=db_host,
        database=db_database
    )
    cur = conn.cursor()

    # Get all breed IDs from the database
    cur.execute("SELECT breed_id FROM breeds")
    breed_ids = cur.fetchall()

    for (breed_id,) in breed_ids:
        print(f"Fetching images for breed_id={breed_id}")
        images = fetch_images_by_breed(breed_id)

        if not images:
            print(f"No images found for breed_id={breed_id}")
            continue

        for image in images:
            image_url = image.get("url")
            if image_url:
                print(f"Inserting image for breed {breed_id}: {image_url}")
                cur.execute("INSERT INTO breed_images (breed_id, image_url) VALUES (%s, %s)", (breed_id, image_url))

    conn.commit()
    cur.close()
    conn.close()
    print("Images for all breeds stored successfully!")

if __name__ == '__main__':
    # Step 1: Store all breeds
    breeds = fetch_all_breeds()
    if breeds:
        store_breeds_in_db(breeds)

    # Step 2: Store images for all breeds
    store_images_for_all_breeds()
