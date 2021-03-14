docker build -t factory .
docker run -d -p 8000:8000 factory
echo "server started on URL http://127.0.0.1:8000"
