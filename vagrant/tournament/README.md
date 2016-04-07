#Running the Tournament Scripts

##Connecting to Database
1.  Open Git Bash or other acceptable console program and navigate to the location of the **vagrant** folder on your local machine
2.  Enter the command **vagrant up**
3.  Enter the command **vagrant ssh**
4.  Enter the command **cd /vagrant**
5.  Enter the command **cd tournament/**
6.  Enter **psql** to launch Postgresql
7.  Enter the command **\i tournament.sql** to create the tournament database and required objects
8.  Enter **\q** to exit the tournament database
9.  Enter the command **python tournament_test.py** to run the test against the tournament database
10. 10 tests should run and if they all run successfully you should see the message **"Success! All tests pass!"**
