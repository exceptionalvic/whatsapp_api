# WhatsApp API Server

This repository demonstrates typical chat application's (WhatsApp) API server backend architecture using Web Socket technology, Django REST Framework, RabbitMQ server.

**Steps to run application**
1. Clone repo: git clone "https://github.com/exceptionalvic/whatsapp_api.git"
2. Create a virtual environment and activate it: `python -m venv env`
3.  Run `pip install -r requirements.txt`
4. Setup database either PostgreSQL and add credentials in `settings.py` file or use default db.slite3 (not suitable for production)

>    DATABASES = {
>           "default": {
>               "ENGINE": "django.db.backends.postgresql_psycopg2",
>               "NAME": "whatsapp_api",
>               "USER": "postgres",
>                "PASSWORD": "mypassword",
>                "HOST": 'localhost',
>                "PORT": "5432"
>            }
>        }
   

Replace NAME, USER and PASSWORD with your actual PostgreSQL RDBMS database. You need to have PostgreSQL installed in your local machine.

5. Run `python manage.py migrate`
6. Setup your RabbitMQ server in `settings.py` file


>    RABBITMQ_HOST = '127.0.0.1'
>    RABBITMQ_PORT = 5672
>    RABBITMQ_USER = os.getenv('RABBITMQ_USER')
>    RABBITMQ_PASS = os.getenv('RABBITMQ_PASS')
>    
>    CHANNEL_LAYERS = {
>        "default": {
>            "BACKEND": "channels_rabbitmq.core.RabbitmqChannelLayer",
>            "CONFIG": {
>                "host": f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASS}@127.0.0.1/",
>            },
>        },
>    }

To use RabbitMQ, you will need to have RabbitMQ installed and started on your local machine, then access the manager interface to create a user and password if you don't want to use the default username: "guest" and password: "guest". Refer to this [documentation](https://www.rabbitmq.com/documentation.html) for help.

7. Start django ASGI server with `python manage.py runserver`. Because Django Channels is installed with daphne, this automatically runs the django ASGI server suitable for websocket connections.
8. Create a .env file at the root of your project and add your RabbitMQ configs and secret key, you can repeat that for database. This is suitable for production environment.

>     Django version 3.2.6, using settings 'whatsapp_api.settings'
>     Starting ASGI/Channels version 3.0.4 development server at http://127.0.0.1:8000/
>     Quit the server with CTRL-BREAK.
>     HTTP/2 support enabled
>     Configuring endpoint tcp:port=8000:interface=127.0.0.1
>     Listening on TCP address 127.0.0.1:8000
9. Open another terminal to run the chat subscriber service  `python manage.py run_chat_subscriber` This service worker listens to receive messages from RabbitMQ exchange via publisher and sends them to the appropriate web socket channels. This is a kind of pub/sub custom approach using Django Channel_Rabbitmq package which have async limitations.

> [uWSGI](https://uwsgi-docs.readthedocs.io/en/latest/#quickstarts) a performant server with inbuilt web sockets support is another
> alternative approach using pika module that connects with RabbitMQ
> broker without relying on Django Channels.

9. Create account using the Swagger API docs at http://localhost:8000/api/v1/docs/ which also contains API docs for other functions.
10. Authenticate a new user `user1` and create a Chatroom using your preferred Client like Postman or Insomnia.
11.  Open another tab in your Client, create and authenticate another user  `user2` and note the user account id.
12. Join the Chatroom created by `user1` using the `chatroom_id` to join the web socket channel layer for this chat room
13. Then open another tab in the client and create a Web socket  request method `WS` usually `ws://`.  This tab will listen to messages and chats and notifications going on on the chatroom created by first user1 which user2 has joined.
To test, in the URL field of your client (Postman or Insomnia), type in 127.0.0.1:8000/ws/chat/<chatroom_id>/?token=your_jwt_access_token gotten from authentication API endpoint response body
14. Whenever user1 sends a message, notice the response in the channel
15. To run tests, run  `pytest`

## Sample message to chatroom
![sample chat message sent in a chatroom](https://lh3.googleusercontent.com/pw/ADCreHeCwf62qDet0TSLuU-zCYdj5BeSC6M714UhkGLOmLmuB22iI_ifRbgtQA2VuENK8DsdYSfym_xRK_kMjxQSPOlo9g9yR-3OpYlVWOR4PubKHxoAyLU=w2400)

## Sample broadcasted message to chatroom via web sockets, all connected chatroom members see new messages.
![Broadcasted message to chatroom via web sockets](https://lh3.googleusercontent.com/pw/ADCreHeQtnMOI1Qc1TOy5ymIKy9ztuViHAoyAzpPeNoGGmSP0Yh_s1MJ3Oq2oxcTGjpuHbNlI3lzmlc5bnp1F9S9Q4NChOyM4h5YwcriX7pnjHa23x61NI8=w2400)

## Possible further improvements
1. Uploading files in chunks to handle large files
2. Usage of uWSGI server gateway for performance with embedded web socket capability
