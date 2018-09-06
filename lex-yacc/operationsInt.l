%{
#include <stdio.h>
%}
%%
" "             ;
\n              ;
[\+\-\/\*]      printf("OPERATOR\n");
[ \t]+          ;
[0-9]+          printf("INTEGER\n");
%%