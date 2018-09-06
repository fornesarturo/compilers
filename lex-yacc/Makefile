clean:
	rm operations.out y.tab.c y.tab.h lex.yy.c operationsInt.out
lex:
	lex operations.l
yacc:
	yacc -d operations.y
interactive:
	lex operationsInt.l
	cc lex.yy.c -o operationsInt.out -ll
	./operationsInt.out < operationsRaw
build:
	make lex
	make yacc
	cc lex.yy.c y.tab.c -o operations.out
run:
	make build
	./operations.out < operationsRaw