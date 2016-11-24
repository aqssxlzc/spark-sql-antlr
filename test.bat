del *.java
del *.class
call antlr4 Sparksql.g4
javac Sparksql*.java
call grun Sparksql root -gui