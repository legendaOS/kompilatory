prog : expression_list;

expression_list : expression terminator
                | expression terminator expression_list
                | terminator
                ;

expression : function_definition
           | function_inline_call
           | if_statement
           | unless_statement
           | rvalue
           | return_statement
           | while_statement
           | for_statement
           ;

function_inline_call : function_call;

function_definition : function_definition_header function_definition_body END;

function_definition_body : expression_list;

function_definition_header : DEF function_name crlf
                           | DEF function_name function_definition_params crlf
                           ;

function_name : id_;

function_definition_params : LEFT_RBRACKET RIGHT_RBRACKET
                           | LEFT_RBRACKET function_definition_params_list RIGHT_RBRACKET
                           | function_definition_params_list
                           ;

function_definition_params_list : function_definition_param_id
                                | function_definition_param_id COMMA function_definition_params_list
                                ;

function_definition_param_id : id_;

return_statement : RETURN all_result;

function_call : function_name LEFT_RBRACKET function_call_param_list RIGHT_RBRACKET
              | function_name function_call_param_list
              | function_name LEFT_RBRACKET RIGHT_RBRACKET
              ;

function_call_param_list : function_call_params;

function_call_params : function_param
                     | function_param COMMA function_call_params
                     ;

function_param : ( function_unnamed_param | function_named_param );

function_unnamed_param : ( int_result | float_result | string_result | dynamic_result );

function_named_param : id_ ASSIGN ( int_result | float_result | string_result | dynamic_result );

function_call_assignment : function_call;

all_result : ( int_result | float_result | string_result | dynamic_result );

elsif_statement : if_elsif_statement;

if_elsif_statement : ELSIF cond_expression crlf statement_body
                   | ELSIF cond_expression crlf statement_body else_token crlf statement_body
                   | ELSIF cond_expression crlf statement_body if_elsif_statement
                   ;

if_statement : IF cond_expression crlf statement_body END
             | IF cond_expression crlf statement_body else_token crlf statement_body END
             | IF cond_expression crlf statement_body elsif_statement END
             ;

unless_statement : UNLESS cond_expression crlf statement_body END
                 | UNLESS cond_expression crlf statement_body else_token crlf statement_body END
                 | UNLESS cond_expression crlf statement_body elsif_statement END
                 ;

while_statement : WHILE cond_expression crlf statement_body END;

for_statement : FOR LEFT_RBRACKET init_expression SEMICOLON cond_expression SEMICOLON loop_expression RIGHT_RBRACKET crlf statement_body END
              | FOR init_expression SEMICOLON cond_expression SEMICOLON loop_expression crlf statement_body END
              ;

init_expression : for_init_list;

all_assignment : ( int_assignment | float_assignment | string_assignment | dynamic_assignment );

for_init_list : all_assignment COMMA for_init_list
              | all_assignment
              ;

cond_expression : comparison_list;

loop_expression : for_loop_list;

for_loop_list : all_assignment COMMA for_loop_list
              | all_assignment
              ;

statement_body : statement_expression_list;

statement_expression_list : expression terminator
                          | RETRY terminator
                          | break_expression terminator
                          | expression statement_expression_list terminator
                          | RETRY statement_expression_list terminator
                          | break_expression statement_expression_list terminator
                          ;

assignment : lvalue ASSIGN rvalue
           | lvalue ( PLUS_ASSIGN | MINUS_ASSIGN | MUL_ASSIGN | DIV_ASSIGN | MOD_ASSIGN | EXP_ASSIGN ) rvalue
           ;

dynamic_assignment : lvalue ASSIGN dynamic_result
                   | lvalue ( PLUS_ASSIGN | MINUS_ASSIGN | MUL_ASSIGN | DIV_ASSIGN | MOD_ASSIGN | EXP_ASSIGN ) dynamic_result
                   ;

int_assignment : lvalue ASSIGN int_result
               | lvalue ( PLUS_ASSIGN | MINUS_ASSIGN | MUL_ASSIGN | DIV_ASSIGN | MOD_ASSIGN | EXP_ASSIGN ) int_result
               ;

float_assignment : lvalue ASSIGN float_result
                 | lvalue ( PLUS_ASSIGN | MINUS_ASSIGN | MUL_ASSIGN | DIV_ASSIGN | MOD_ASSIGN | EXP_ASSIGN ) float_result
                 ;

string_assignment : lvalue ASSIGN string_result
                  | lvalue PLUS_ASSIGN string_result
                  ;

initial_array_assignment : lvalue ASSIGN LEFT_SBRACKET RIGHT_SBRACKET;

array_assignment : array_selector ASSIGN all_result;

array_definition : LEFT_SBRACKET array_definition_elements RIGHT_SBRACKET;

array_definition_elements : ( int_result | dynamic_result )
                          | ( int_result | dynamic_result ) COMMA array_definition_elements
                          ;

array_selector : id_ LEFT_SBRACKET ( int_result | dynamic_result ) RIGHT_SBRACKET
               ;

dynamic_result : dynamic_ ( MUL | DIV | MOD ) int_result
               | int_result ( MUL | DIV | MOD ) dynamic_result
               | dynamic_ ( MUL | DIV | MOD ) float_result
               | float_result ( MUL | DIV | MOD ) dynamic_result
               | dynamic_ ( MUL | DIV | MOD ) dynamic_result
               | dynamic_ MUL string_result
               | string_result MUL dynamic_result
               | dynamic_ ( PLUS | MINUS ) int_result
               | int_result ( PLUS | MINUS ) dynamic_result
               | dynamic_ ( PLUS | MINUS )  float_result
               | float_result ( PLUS | MINUS )  dynamic_result
               | dynamic_ ( PLUS | MINUS ) dynamic_result
               | LEFT_RBRACKET dynamic_result RIGHT_RBRACKET
               | dynamic_
               ;

dynamic_ : id_
        | function_call_assignment
        | array_selector
        ;

int_result : int_t ( MUL | DIV | MOD ) int_result
           | int_t ( PLUS | MINUS ) int_result
           | LEFT_RBRACKET int_result RIGHT_RBRACKET
           | int_t
           ;

float_result : float_t ( MUL | DIV | MOD ) float_result
             | int_result ( MUL | DIV | MOD ) float_result
             | float_t ( MUL | DIV | MOD ) int_result
             | float_t ( PLUS | MINUS ) float_result
             | int_result ( PLUS | MINUS )  float_result
             | float_t ( PLUS | MINUS )  int_result
             | LEFT_RBRACKET float_result RIGHT_RBRACKET
             | float_t
             ;

string_result : literal_t MUL int_result
              | int_result MUL string_result
              | literal_t PLUS string_result
              | literal_t
              ;

comparison_list : comparison BIT_AND comparison_list
                | comparison AND comparison_list
                | comparison BIT_OR comparison_list
                | comparison OR comparison_list
                | LEFT_RBRACKET comparison_list RIGHT_RBRACKET
                | comparison
                ;

comparison : comp_var ( LESS | GREATER | LESS_EQUAL | GREATER_EQUAL ) comp_var
           | comp_var ( EQUAL | NOT_EQUAL ) comp_var
           ;

comp_var : all_result
         | array_selector
         | id_
         ;

lvalue : id_;

rvalue : lvalue

       | initial_array_assignment
       | array_assignment

       | int_result
       | float_result
       | string_result

       | global_set
       | global_get
       | dynamic_assignment
       | string_assignment
       | float_assignment
       | int_assignment
       | assignment

       | function_call
       | literal_t
       | bool_t
       | float_t
       | int_t
       | nil_t

       | dynamic_result EXP rvalue

       | ( NOT | BIT_NOT ) rvalue

       | dynamic_result ( MUL | DIV | MOD ) rvalue
       | dynamic_result ( PLUS | MINUS ) rvalue

       | dynamic_result ( BIT_SHL | BIT_SHR ) rvalue

       | dynamic_result BIT_AND rvalue

       | dynamic_result ( BIT_OR | BIT_XOR ) rvalue

       | dynamic_result ( LESS | GREATER | LESS_EQUAL | GREATER_EQUAL ) rvalue

       | dynamic_result ( EQUAL | NOT_EQUAL ) rvalue

       | dynamic_result ( OR | AND ) rvalue

       | LEFT_RBRACKET rvalue RIGHT_RBRACKET
       ;

break_expression : BREAK;

literal_t : LITERAL;

float_t : FLOAT;

int_t : INT;

bool_t : TRUE
       | FALSE
       ;

nil_t : NIL;

id_ : ID;


terminator : SEMICOLON terminator
           | crlf terminator
           | SEMICOLON
           | crlf
           ;

else_token : ELSE;

crlf : CRLF;

LITERAL : QUOTE ( SYMB | list_of_symb ) QUOTE;
LITERAL : DQUOTE ( SYMB | list_of_symb ) DQUOTE;

COMMA : ',';
SEMICOLON : ';';

END : 'end';
DEF : 'def';
RETURN : 'return';


IF : 'if';
ELSE : 'else';
ELSIF : 'elsif';
UNLESS : 'unless';
WHILE : 'while';
RETRY : 'retry';
BREAK : 'break';
FOR : 'for';

TRUE : 'true';
FALSE : 'false';

PLUS : '+';
MINUS : '-';
MUL : '*';
DIV : '/';
MOD : '%';
EXP : '**';

EQUAL : '==';
NOT_EQUAL : '!=';
GREATER : '>';
LESS : '<';
LESS_EQUAL : '<=';
GREATER_EQUAL : '>=';

ASSIGN : '=';
PLUS_ASSIGN : '+=';
MINUS_ASSIGN : '-=';
MUL_ASSIGN : '*=';
DIV_ASSIGN : '/=';
MOD_ASSIGN : '%=';
EXP_ASSIGN : '**=';

BIT_AND : '&';
BIT_OR : '|';
BIT_XOR : '^';
BIT_NOT : '~';
BIT_SHL : '<<';
BIT_SHR : '>>';

AND : 'and' | '&&';
OR : 'or' | '||';
NOT : 'not' | '!';

LEFT_RBRACKET : '(';
RIGHT_RBRACKET : ')';
LEFT_SBRACKET : '[';
RIGHT_SBRACKET : ']';

NIL : 'nil';

list_of_symb : ( SYMB | SYMB list_of_symb );

