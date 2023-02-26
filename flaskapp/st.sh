gunicorn --bind 127.0.0.1:5000 wsgi:app & APP_PID=$!
sleep 5
<<<<<<< HEAD
echo start client
python3 client.py
sleep 5
echo $APP_PID
kill -TERM $APP_PID
exit 0
=======
echo $APP_PID
kill -TERM $APP_PID
echo process gunicorns kills
exit 0
>>>>>>> origin/main
