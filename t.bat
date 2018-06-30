cls
call antlr4 -o javaantlrparser config.g4
javac javaantlrparser/config*.java
cd javaantlrparser
call grun config r ../MemType.txt -gui
cd ..
