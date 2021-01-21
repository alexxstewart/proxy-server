# proxy-server
A simple proxy server to handle http requests

## TO RUN IN WINDOWS

1) Go to any folder(in file explorer) that you wan the proxy file to be stored

2) Copy the path address by left clicking the path at the top and then selecting 'copy address as text'

3) Open up Terminal and type 'cd' followed by pasting the text you just copied

4) Now type in the following command 'git clone https://github.com/aste425/proxy-server.git'

5) Now move into the folder 'proxy-server' (do this by typing 'cd proxy-server')

6) Now we need to setup the proxy so it can recieve requests from the browser. Open up the windows setting and type in 'Change Proxy Setting'. Turn of the buttons 'Automatically detect settings' and 'use setup script'. Scroll down and turn on the button 'Use a proxy server'. By deafault the python script has the host as 127.0.0.1 and listens on port 8000 (but the port number can be any number between 1024 and 65535), so you can input these numbers to their respective fields on the page.

7) Now go back to terminal and type in "python server.py '127.0.0.1' 8000" (type everything between the "" characters). Now the server should be running.

8) You should be able to see requests as you navigate through http websites.

*Note that this proxy only works for http websites. Most popular websites use the https transfer protocol which differs to http due the secure nature of it. For this project I simply wanted to learn how proxies work so https proxying is not supported, hence https websites will not work while the proxy is running*
