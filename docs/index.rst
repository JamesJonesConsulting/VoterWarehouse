VoterWarehouse
==============

--------------

Introduction
------------

Need to be able to import elections office Voter and Voter History files
into a relational database so your campaign can extract walking lists
and better ‘discover’ likely leads in your campaign? This tool does just
that. All you need, at a minimum, is a free instance of MariaDB and
voter files and you are ready to go! This application is redesign in
Python 3 of an application that was written prior in PHP7 (which itself
was a redesign of a Perl application).

So what does this app do?
~~~~~~~~~~~~~~~~~~~~~~~~~

Currently, it only supports Florida Election Office zip files as anybody
can get them for ‘free’ (and Georgia charges significantly these days so
I don’t have access to those monthly disks anymore… but if that changes
and somebody ‘makes a deal’ with me… perhaps I’ll write it in as this is
application is extendable by design).

OK, let's get started... how do I get it?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For now, it just builds as a linux compatible binary and also RPM and DEB
packages. There's still some work to do to setup GitLab, Azure DevOps, Jenkins
and GitHub pipelines. I'll build it all ways.

To build it the 'basic' way, clone the source and run

.. code:: commandline

    ./build.sh

That will build the `voterwarehouse` binary and invoke docker to build
the RPM and DEB packages.

Next steps (for me) involve publishing a container to Dockerhub. After that, building
out all the different pipelines. I'd imagine _if_ there's enough demand, I can
create a Chocolatey package as well.

Command line syntax
^^^^^^^^^^^^^^^^^^^

+------------------+----------------------------------------------------------+
| Command/Argument | Function                                                 |
+==================+==========================================================+
| -a / -action     | [Required] Main ‘action’, currently support ‘import’     |
+------------------+----------------------------------------------------------+
| -t / -type       | [Required] The ‘type’ of function voters/history         |
+------------------+----------------------------------------------------------+
| -f / -file       | Specifies a file to import or export                     |
+------------------+----------------------------------------------------------+
| -c / -config     | Config file in YAML format. If not provided, defaults to |
|                  | ``/etc/VoterWarehouse/config.yml``                       |
+------------------+----------------------------------------------------------+

Example YAML Config file:

.. code:: yaml

   ---
   UnitedStates:
     Florida:
       database:
         host: dbhostname.example.net
         port: 3306
         schema: FloridaVoters
         user: dbuser
         password: dbpassword

Importing Voter Data
^^^^^^^^^^^^^^^^^^^^

Example:

.. code:: commandline

   voterwarehouse -a import -t voters -f ~/VotersExtract.zip [-c myconfig.yml]

Importing Voter History
^^^^^^^^^^^^^^^^^^^^^^^

Example:

.. code:: commandline

   voterwarehouse -a import -t history -f ~/VotersHistory.zip [-c myconfig.yml]

Why ‘rewrite’ it? A bit of history…
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The original ``perl`` version was written in the 1990’s and specifically
to “work” around the *constraint* of the old 2G max file size limitation
(when that was a barrier many years ago). A good chuck of the
application was addressing the fact that ‘unzipping’ the Georgia single
file exceeded 2G in size so it couldn’t be handled in a straight forward
way. The file was unzipped in ‘chunks’ and iterated through and brought
into tables on a per ‘county’ basis. This was to work within that 2G
file size constraint.

Obviously, that 2G restraint went away with time and that ‘workaround’
was no longer needed. I had piddled with writing this on SpringBoot
(Java) but I found handling this kind batch process was poorly suited
for Java and was constantly tasseling with memory and performance
issues. I concluded I had picked the “wrong tool” for the job (it *can*
be done *but* there are better options). Once I relocated to Florida and
a new job had me writing LOT more apps in Java, Nodejs and PHP just left
this project on the backburner and I knew I would circle back to it one
day.

I probably should have selected Nodejs or Python but I had a friend who
approached me who was interested in me developing this for a Florida
candidate that was already campaigning and asked if I could generate
some walking lists for him *fast*. Long story short, I figured PHP would
be the quickest and I belted out the PHP version and generated the
walking lists in about a week and pulled those walking lists.

So, I’ve had some ‘asks’ about this tool I haven’t touched in far too
long. PHP is near the top of my list of my ‘least’ favorite languages
and I thankfully don’t have to write in that awful language anymore. So
this has been sitting in my ‘backlog’ waiting for me to make a ‘better
choice’ in language. Python 3 is the natural choice for me. It has the
advantages of languages like ‘Perl’ that’s low level enough that I can
get good performance and keep this small and even compile it into
packages (aka: portable). So here we are with this Python 3 version over
20 years since the original version and I’m releasing this as ‘open
source’.