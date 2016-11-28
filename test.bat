del *.java
del *.class
call antlr4 Sparksql.g4
javac Sparksql*.java
REM call grun Sparksql root C:\Users\zhangchen12\projects\JXL\Model.sql -gui