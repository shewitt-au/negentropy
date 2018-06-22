cls
call antlr4 -o javaantlrparser memmap.g4
javac javaantlrparser/memmap*.java
cd javaantlrparser
call grun memmap r ../MemType.txt -gui
cd ..
