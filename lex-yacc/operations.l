%{
#include <stdio.h>
#include "y.tab.h"
%}
%%
" "             ;
\n              ;
[\+\-\/\*]      return OPERATOR;
[ \t]+          ;
[0-9]+          return INTEGER;
%%