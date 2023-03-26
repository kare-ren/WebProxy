# WebProxy

## Testing on Mac via Google Chrome and Safari

* Run: python3 ProxyServer.py 127.0.0.1 100000
* Wait until "Ready to serve..." is printed as standard output
* Then open Chrome and go to: 127.0.0.1:12000/acme.com
* Two files acme.com and styles.css are created in current directory
* To test cache, go to: 127.0.0.1:12000/acme.com prior to cache deletion
* Cache deletes after 60 seconds
