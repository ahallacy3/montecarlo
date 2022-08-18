Written with:
python 3.7.9
npm 6.14.4
node 12.16.2

Will not work with anything older than python 3.7.3. 
Might work with something newer than 3.7.9

Setup Instructions:
These instructions assume a Windows CMD shell. The will need to be modified for any other system

1. Create a python virtual environment
2. Activate the virtual environment 
3. Navigate to the "backend" directory
4. Install the project requirements with pip install -r requirements.txt
5. Run "set PYTHONPATH=.\.."
6. Run "python setup.py" to configure the Sqlite database
7. start the data load process by running "python get_scheduled_data.py"
8. Open a new terminal, navigate to the backend directory, and run "python app.py" to start the API
9. Query the api using the /data?metric=<metric-name> and /metric-options endpoints

To run the UI

1. navigate to the "frontend/montecarlo-ui" folder
2. run "npm install"
3. run "npm run start"
4. Open localhost:4200 in a browser


Scalability:
The first scalability improvement would be to use a server based RDBMS like Postgres or MySQL to store and maintain system data. While Sqlite is useful in the context of a small test application like this, its performance degrades rapidly as data quantity increases.
Further improvements could include partitioning the table by symbol and/or date to improve query performance.
Tracking many metrics would require updating the list in the constants.py file and possibly reconfiguring how the metrics are loaded if a difference base metric were desired.
Tracking significantly more metrics might require true multithreading rather than just multiprocessing, or could require additional physical workers with each worker handling some subset of the metric list.
Polling metrics more frequently might require additional workers, though it's likely that the maximum polling speed supported by the API is lower than what could be handled by a single worker, so more than one worker per symbol would likely not be necessary
As the data is updated in a process that is unrelated to the users pulling the metrics, and the update process does not block the loading of data, many users could be supported with a single RDBMS server. Read replicas of the server could be created if the user load justified it


Testing:
There is currently no testing implemented in the application, as there are only about 30 lines of code involved.
A slightly more complex app would likely benefit from unit testing in both the UI and API, as all methods used by the api and all functions in the UI could be covered by tests
As the app contains both a UI and and API it would also benefit from integration tests to ensure that changes made to one are accurately reflected in the other.
If usage grew significantly the application would also benefit from performance testing, as simulating a heavy load on the application would likely help determine bottlenecks


New Feature:
In order to implement this, we must first integrate the get_schedule_data functionality with the api. This is relatively simple to set up, as the get_scheduled_data code can be called directly from the app.py file when it is run.
We must then modify the flask implementation to use some library, like gevent, that will support users connecting to the system using websockets.
When a user loads the UI, the will immediately establish a websocket connection to the modified API. They can continue loading data via the existing flask endpoints once that connection is established.

As a part of the get_scehdule_data function, a sql query would be added that looked something like "SELECT AVG((price) FROM price_in_usdt WHERE symbol = <symbol> and timestamp >= datetime('now','-24 hours'))"
The result of this query would be checked against the incoming price to determine if an alert needs to be sent.
If an alert is to be sent, the get_schedule_data function will call a new function that will take the list of open websocket connections and push the event to all of them