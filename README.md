# spark-sql-antlr
spark sql antlr parser 

ADD SUPPORT FOR OVER PARTITION and SOME custom functions.
the grammer is not complete covered.
You may need additional effort for your using.

## Install ANTLR

$ cd /usr/local/lib
$ sudo curl -O http://www.antlr.org/download/antlr-4.5.1-complete.jar
$ export CLASSPATH=".:/usr/local/lib/antlr-4.5.1-complete.jar:$CLASSPATH"
$ alias antlr4='java -jar /usr/local/lib/antlr-4.5.1-complete.jar'
$ alias grun='java org.antlr.v4.gui.TestRig'

## Download dependency

$ tox -r

## Generate parser (python)

$ antlr4 -Dlanguage=Python3 -visitor Sparksql.g4

