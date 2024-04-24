
# IoT-Data-Handling-System

## How to Run the App

1. Configure and run MongoDB, RabbitMQ with MQTT plugins on your system using their official sites.
2. Create a virtual environment using: 
    ```
    python3 -m venv env
    ```
3. Install the dependencies using: 
    ```
    pip install -r requirements.txt
    ```
4. To run the app, simply execute the command: 
    ```
    py app.py
    ```
5. To enable debug mode and get logs, use: 
    ```
    py app.py --debug
    ```

Follow the instructions on the terminal to publish data and retrieve data to MQTT and MongoDB respectively.

