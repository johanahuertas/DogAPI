from flask import Flask, render_template
import mysql.connector
import os
from fetch_data import fetch_images_by_breed

app = Flask(__name__)


def get_images_by_breed(breed_id):
    """Fetch images for a specific breed from the database."""
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
    # Retrieve only image URLs for the given breed_id
    cur.execute("SELECT image_url FROM breed_images WHERE breed_id = %s", (breed_id,))
    images = cur.fetchall()
    print(f"Images retrieved for breed_id={breed_id}: {images}")  # Debugging
    cur.close()
    conn.close()
    return images


def get_random_logo_image():
    """Fetch a random dog image from the database to be used as the logo."""
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
    # Fetch a random image URL from the breed_images table
    cur.execute("SELECT image_url FROM breed_images ORDER BY RAND() LIMIT 1")
    logo_image = cur.fetchone()  # Fetch one random image
    cur.close()
    conn.close()

    if logo_image:
        return logo_image[0]  # Return the image URL
    else:
        return "https://via.placeholder.com/100"  # Fallback if no image found


@app.route('/')
def index():
    """Render the home page with all breeds and a random logo."""
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
    cur.execute("SELECT breed_id, breed_name FROM breeds")
    breeds = cur.fetchall()
    cur.close()
    conn.close()

    # Fetch a random dog image to use as the logo
    logo_image = get_random_logo_image()

    return render_template('index.html', breeds=breeds, logo_image=logo_image)


@app.route('/images/<breed_id>')
def images(breed_id):
    """Fetch and display images for a breed."""
    images = get_images_by_breed(breed_id)

    # Fetch a random dog image to use as the logo for the images page
    logo_image = get_random_logo_image()

    return render_template('images.html', images=images, breed_id=breed_id, logo_image=logo_image)


if __name__ == '__main__':
    app.run(debug=True, port=5002)
