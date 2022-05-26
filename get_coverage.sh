docker-compose exec web coverage run manage.py test
docker-compose exec web coverage report
docker-compose exec web coverage html