# Twitter Data Mining 
## Mine, extract, and analyze Twitter "tweet" data based on query specifications. 

Command Line Arguments
---
	help: -h, -help

	mine: -m, -mine

	query:
		- since: "yyyy-mm-dd" -s, -since
		- until: "yyyy-mm-dd" -u, -until
		- tweet limit: <int> -l, -limit

	remine: -r, -remine

	extract: -e, -extract

	hashtags:
		- file: <file> -hf, -hashfile
		- list: "tag, tag, ..., tag" -hl, -hashlist
    
Example Usage
---
* Mine for 100 tweets about SpaceX and Elon Musk since March 10th, 2018. 
```console
foo@bar: $ python app.py "SpaceX, Elon" -hl "2018-03-10" -s 100 -l -m
```

* Remine tweets (removing the current contents of the *data* folder)
```console
foo@bar: $ python app.py "SpaceX" -hl "2018-03-10" -s -r
```



