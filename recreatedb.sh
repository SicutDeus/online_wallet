sudo rm -rf ./data
sudo docker compose -p online_wallet -f ./docker-compose.yml up -d --force-recreate db
