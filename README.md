DESCRIPTION
===========
minimalistic tracking written in python and twisted

http://trakr.mobi

INSTALLATION
============
you will need python pip

>sudo apt-get install python python-pip
>sudo pip install https://github.com/infin8/trakr/archive/master.zip

USAGE
=====
start the service

> twistd trakr

now visit http://localhost:8101/dashboard

> user: trakr
> pass: trakr

### Tracking

place the following code on your landing page with lpid being your landing page id

> <meta name="lpid" content="mangos" />
> <script language="JavaScript" type="text/javascript" src="http://localhost:8101/js"></script>
