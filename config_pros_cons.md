For frequently used projects that can be reused it is often convenient to have
a config file. There are a lot of opinions on config files on stack overflow
github etc.

Initially I was using .ini files for my projects, however, I found there to be
some major limitations. I wasn't able to create a dictionary inside of an .ini
file which is frustrating for certain uses cases such as this example:

"defining register code"

It makes sense to keep all information related to each register together instead
in some type of list of different attributes. If you wanted to delete a register
you have to edit each list and make sure they are in the correct order. This is
prone to error.

Alternatively you could use something like json directly. I dislike this option
because you cannot put in comments inside the file conveniently. In my example
config, I have put all the documentation of the various settings inside the
actual file which I believe to be very helpful in getting something working
quickly. You can have commented out settings inside the file which is common in
Unix. The other benefit of comments is to quickly be able to change a config file
while developing by commenting out a line. With .ini files I had to have several
of different .ini files while testing and switch files in the code. I found it
more convenient to be able to comment out a line and get rid of a setting.

I did read of possibly security issues with yaml files due to the flexibility
of data structures you can create. I am using safe_load in all of my projects
mitigate this.
