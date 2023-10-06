//apartado a)
MOV	R1, V
ADD	R1, 4
MOV	R2, [R1]
MOV	[A], R2
/*
Solución:		A = V[1];
Es la forma más simple de explicar lo que hacen las 4 instr.
*/

//apartado b)
MOV	R1, [A]     //almacena el valor de la direccion A en R1
MOV	R2, V       //situa la dirección del vector V en R2
MOV	[R2+12],R1  //mueve 4 bytes pisición 3 y asigna el valor de R1(A)

;*Solución:V[3]=A;*/

//apartado c)
MOV	R1, 8        //asigna en R1 el valor de 0x08
MOV	R3, [V+R1]   //suma R1 a la dirección V y carga el valor en R3
MOV	[A], R3      //almacena R3 en la dirección [A]

;*Solución:A=V[2];*/

