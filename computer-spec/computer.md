INSTRUCTION SET FOR DESMOS COMPUTER

FLAGS
-----

EQUALS
GREATER THAN
LESS THAN

INSTRUCTIONS
------------

STO ( value, address ) -> store a value into an address
ADD ( addra, addrb, toaddr ) -> add a value from two addresses to a third address
SUB ( addra, addrb, toaddr ) -> subtract a value from two addresses to a third address
MUL ( addra, addrb, toaddr ) -> multiply a value from two addresses to a third address
DIV ( addra, addrb, toaddr ) -> divide a value from two addresses to a third address
CMP ( addra, addrb ) -> compare two values, store result in flags
	- set all flags to false
	- if equal, set EQUALS
	- if addra > addrb, set GREATER THAN
	- if addra < addrb, set LESS THAN

ELD ( address ) -> store the value of EQUALS flag to address (1 if true, 0 if false)
GLD ( address ) -> store the value of GREATER THAN flag to address (1 if true, 0 if false)
LLD ( address ) -> store the value of LESS THAN flag to address (1 if true, 0 if false)

JMP ( address ) -> change execution to address
BE ( address ) -> branch if equal
BNE ( address ) -> branch if not equal
BG ( address ) -> branch if greater
BL ( address ) -> branch if less
