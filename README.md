# Mininal++ Compiler

Στόχος του project είναι η μεταγλώττιση μιας αυτοσχέδιας συναρτησιακής
προγραμματιστικής γλώσσας(Minimal++). Το αρχείο εξόδου θα είναι σε Assembly.

## Minimal++'s  Grammar

\<program> ::= program id { <block> }<br/>
\<block> ::= <declarations> <subprograms> <statements><br/>
\<declarations> ::= (declare <varlist>;)*<br/>
\<varlist> ::= ε | id (, id)*<br/>
\<subprograms> ::= (<subprogram>)*<br/>
\<subprogram> ::= function id <funcbody> | procedure id <funcbody><br/>
\<funcbody> ::= <formalpars> { <block> }<br/>
\<formalpars> ::= ( <formalparlist> )<br/>
\<formalparlist> ::= <formalparitem> (, <formalparitem>)* | ε<br/>
\<formalparitem ::= in id | inout id<br/>
\<statements> ::= <statement> | { <statement> (; <statement>)* }<br/>
\<statement> ::= <assignment_stat><br/>
| <if_stat><br/>
| <whilestat><br/>
| <forcase_stat><br/>
| <call_stat><br/>
| <return_stat><br/>
| <input_stat><br/>
| <print_stat><br/>
\<assignment_stat> ::= id := <expression><br/>
\<if_stat> ::= if (<condition>) then <statements> <elsepart><br/>
\<elsepart> ::= ε | else <statements><br/>
\<whilestat> ::= while (<condition>)<statements><br/>
\<forcase_stat> ::= forcase ( when (<condition>) : <statements>)* default: <statements><br/>
\<return_stat> ::= return <expression><br/>
\<call_stat> ::= call id <actualpars><br/>
\<print_stat> ::= print (<expression>)<br/>
\<input_stat> ::= input (id)<br/>
\<actualpars> ::= (<actualparlist>)<br/>
\<actualparlist> ::= <actualparitem> (, <actualparitem>)* | ε<br/>
\<actualparitem> ::= in <expression> | inouttk id<br/>
\<condition> ::= <boolterm> (or <boolterm>)*<br/>
\<boolterm> ::= <boolfactor> (and <boolfactor>)*<br/>
\<boolfactor> ::= not [<condition>] | [<condition>] | <expression> <relational_oper> <expression><br/>
\<expression> ::= <optional_sign> <term> (<add_oper> <term>)*<br/>
\<term> ::= <factor> (<mul_oper> <factor>)*<br/>
\<factor> ::= constant | (<expression>) | id <idtail<br/>
\<idtail> ::= ε | <actualpars><br/>
\<relational_oper> ::= = | <= | >= | < | > | <><br/>
\<add_oper> ::= + | -<br/>
\<mul_oper> ::= * | /<br/>
\<optional_sign> ::= ε | <add_oper><br/>
<br/>
Comments:
* Multiple lines: <</*>>, <<*/>>
* Single line: <<//>>

## Running the project

<ol>
<li>min_compiler.py</li>
<li>Give a file</li>
<li>Output files:</li>
<ol>
<li>semi_code.int</li>
<li>semi_code.c</li>
<li>final_code.asm</li>
</ol>
</ol>

## Output files

### semi_code.int

Αποτελείται από αριθμημένες τετράδες.<br/>
Πράξεις:<br/>
* +, a, b, t_1 (a+b). Εκχωρούμε την πράξη σε μια προσωρινή μεταβλητή
* -, *, /. Το ίδιο.
<br/>
Εκχώρηση:<br/>
:=, x, _, z (z := x)<br/>
Jump(goto):<br/>
jump, _, _, 100. Θα πάει στην τετράδα 100.<br/>
Συγκρίσεις:<br/>
* =, x, y, z (x=z). Αν ισχύει η σύγκριση θα μεταπηδήσει στο z(αριθμός τετράδας).<br/>
* >=, <=, >, <, <>. To ίδιο.
<br/>
Αρχή main ή συναρτήσεων:<br/>
begin_block, name, _, _<br/>
Τέλος main ή συναρτήσεων:<br/>
end_block, name, _, _<br/>
Τερματισμός προγράμματος:<br/>
halt, _, _, _<br/>
Παράμετροι:<br/>
par, x, m, _<br/>
Όπου x:<br/>
* CV: Μετάδοση τιμής.
* REF: Μετάδοση με αναφορά.
<br/>
Κλήση συνάρτησης:<br/>
call, name, _, _<br/>
Επιστροφή τιμής συνάρτησης:<br/>
ret, x, _, _<br/>
