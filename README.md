# Twitter Data Mining 
## Mine, extract, and analyze Twitter "tweet" data based on query specifications. 

Command Line Arguments
---
	help: -h, -help

	mine: -m, -mine

	query:
		- since: [-s, -since] "yyyy-mm-dd" 
		- until: [-u, -until] "yyyy-mm-dd" 
		- tweet limit: [-l, -limit] <int>

	remine: -r, -remine

	extract: -e, -extract

	hashtags:
		- file: [-hf, -hashfile] <file>
		- list: [-hl, -hashlist] "tag, tag, ..., tag" 
    
Example Usage
---
* Mine for 100 tweets about SpaceX and Elon Musk since March 10th, 2018. 
```console
foo@bar: $ python app.py -hl "SpaceX, Elon" -s "2018-03-10" -l 100 -m
```

* Remine tweets (removing the current contents of the *data* folder)
```console
foo@bar: $ python app.py -hl "SpaceX" -s "2018-03-10" -r 
```



