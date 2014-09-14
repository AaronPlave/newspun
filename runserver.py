from newspun import app

if __name__ == "__main__":
    app.run()


### RUNNING
# sudo uwsgi --http 127.0.0.1:5000 --wsgi-file rs.py --callable app --processes 3 --threads 2 --stats 127.0.0.1:9191