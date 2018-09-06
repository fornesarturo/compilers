%{
#include <stdio.h>
#include <string.h>
 
void yyerror(const char *str) { fprintf(stderr,"error: %s\n",str); }
 
int yywrap() { return 1; } 
  
main() { yyparse(); } 

%}

%token OPERATOR INTEGER

%%
commands: /* empty */
        | operation
        ;

operation:
        INTEGER OPERATOR INTEGER
        { printf("Basic operation\n"); }
        |
        INTEGER OPERATOR more
        { printf("Some more\n"); }
        ;
more:
        INTEGER
        { printf("End of operations\n"); }
        |
        INTEGER OPERATOR more
        { printf("Again some more\n"); }
        ;
%%