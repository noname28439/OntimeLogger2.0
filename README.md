# OntimeLogger2.0

This Programm check the current active Window every second. 
You can then look for this information on the webServer, where it is displayed in a chart. 

Setup:
Just run
./Logger.py and ./WebServer/webServer.py
on startup

requestExample: http://localhost:34567/times/?days=50&amount=0.3&type=line&avrg=5
(Get parameters: 
?days={last ... days}
&amount={minimal use in hours}
&type={bar(stacked)/line}
&avrg={smoothing the graphs(default: 0)})
