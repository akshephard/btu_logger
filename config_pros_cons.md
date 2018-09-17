# YAML vs JSON vs INI for config files in python

For frequently used projects that can be reused it is often convenient to have
a config file. There are a lot of opinions on config files on stack overflow
github etc. I have switched to using YAML for my python projects for several
reasons I have described below.

Initially I was using INI files for my projects, however, I found there to be
some major limitations. I wasn't able to create a dictionary inside of an INI
file which is frustrating for certain uses cases such as this example:

```registers: {signal_strength:[100,32float],temperature:[102,32float]} ```

The above code is an example of part of a YAML config file. It aggregates all
of the information together for a particular register together into a dictionary.
It makes sense to keep all information related to each register together instead
of multiple lists of different attributes. If you wanted to delete a register you 
have to edit each list and make sure they are in the correct order. This is 
prone to error.

Alternatively you could use something like JSON directly. I dislike this option
because you cannot put in comments inside the file conveniently and it is less 
readable to humans. In this [example code](https://github.com/akshephard/pymodbus_simulator/blob/master/config.yaml)
, I have put all the documentation of the various settings inside the actual file 
which I believe to be very helpful in  getting something working quickly. You can 
have commented out settings inside the file which is common in Unix. The other benefit
of comments is to quickly be able to change a config file while developing by 
commenting out a line. With INI files I had to have several of different INI files
while testing and switch files in the code. I found it more convenient to be able to 
comment out a line and get rid of a setting.

I did read of possibly [security issue](https://security.openstack.org/guidelines/dg_avoid-dangerous-input-parsing-libraries.html) with yaml files due to the flexibility of data structures you can 
create with embedded code. I am using safe_load in all of my projects to mitigate this.

