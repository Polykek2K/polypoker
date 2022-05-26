docker-compose up --build -d
docker-compose exec db psql -U postgres -c "CREATE DATABASE webpoker"
docker-compose exec web python manage.py collectstatic
docker-compose exec web python manage.py migrate
docker-compose exec web coverage run manage.py test