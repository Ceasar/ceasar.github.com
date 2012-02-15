---
layout: post
title: "Your Resume: Powered by Github Pages and Twitter Bootstrap"
category: 
tags: []
---
{% include JB/setup %}

If you love Github and aren't particularly skilled with css, and you also want to make your resume stand out by using anything but Microsoft word, this post is for you.

Meet Bootstrap
--------------

If you don't know what [Twitter Bootrap](http://twitter.github.com/bootstrap/), you're missing out. Basically, Twitter has packaged some very generic, but very pretty css all into one file that just instantly makes any html document aesthetically pleasing.

I'll leave the explanation of how to use it to the docs, but here's the motivation for using bootstrap:

* It provides very sensible default styles, but it's also super easy to override parts as needed.
* It has a built in grid system with support for several new tags, notably "section" and "row".

Combine the two together, and it suddenly there's no reason to bother with Word anymore.

Meet Github
-----------

Better yet, since we no longer are using Word, we can use Git and get some really sensible commits. Again, I'll assume you know how to use Git, but here's something you may not know: Git lets you host pages for your projects (for free).

The service is called [Github Pages](http://pages.github.com) and you're really supposed to use it to power the docs for a project, but in our case we can actually replace the index with a copy of our resume. Just follow the directions [here](http://pages.github.com/#project_pages) making sure to skip the first code-block on cleaning out your project (since your project is our doc). Note that it can take up to ten minutes to get your page up and running the first time, but after that it's nearly instantaneous with each push.

And now we have our resume online for free, it's automatically updated everytime we push, and we can even add links to anything we want. (Time to get rid of PDFs in my opinion.)

HTML to PDF
-----------

Lastly, you'll probably want some PDFs to share with recruiters since many won't accept a URL. Unfortunately, there's no way to "Save as..." HTML to a PDF.

Fortunately, there is a way to get a PDF anyhow, although I've yet to find a particularly nice solution. Turns out, if you're using Chrome you simply right-click a web page, press "Print...", modify the destination to "Print to PDF", and Chrome will save the page to a destination of your choice. Make sure to uncheck "Headers and footers" before printing or you'll have the link and page number appended to the bottom and top of your resume. Note also you can play with the margins.


I hope that was useful!
