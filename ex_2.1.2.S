//apartado a)
/*
N = 4;
sum = 0;
partial_sum = 0;
i = 0;		
while ( i< N)  {
   partial_sum = partial_sum + V[i];
   i = i + 1;
}sum = partial_sum; 
*/
MOV R1,4        //asignamos N a R1
MOV R2,0        //asignamos i a R2
MOV R3,0        //asignamos partial_sum a R3
MOV R4,V        //guardamos la posición de V en R4
while: 
CMP R2,R1
JGE end         //verificamos que i<N(almacenada en R1)
MOV R5,[R4]     //cargamos  V[i] en R5
ADD R3,R5       //partial_sum(almacenado en R3)+=V[i]
INC R2          //incrementamos la variable iteradora
ADD R4,4        //desplazamos una posición en el vector sumando 4
JMP while          
end:
MOV [SUM],R3    //Almacenamos el resultado en sum
RET


//apartado b)
/*
Tenemos definido un vector, V, de 8 elementos. Cada elemento es un número entero codificado en complemento a 2 con 32 bits:
	V: 3, -7, 125, 421, -9, 1000, 7, 8
Escribid un código en ensamblador que cambie el orden en que se encuentran los elementos del vector, dejando el primer elemento en la última posición, el segundo en la antepenúltima etc. Después de la ejecución del código el vector debe quedar así:
	V: 8, 7, 1000, -9, 421, 125, -7, 3
El bucle principal del programa debería servir para vectores con un número cualquiera de elementos. Antes de este bucle, habría que iniciar el contenido de ciertos registros con los valores apropiados para este ejemplo (vector de 8 elementos)
*/

MOV R1, 8        //en R1 asignamos el tamaño de elementos de V
MOV R2, V        //en R2 asignamos la dirección de V
MOV R3, V        //en R3 asignamos también la dirección de V
ADD R3, 28       //4*8=32, asignamos a R3 la última posición del vector

while:
CMP R2, R3       //R2(V por la izquierda) con R3 (V por la derecha)
JGE end          //si R2>=R3 implica que lo ha recorrido entero, saltamos
MOV R4, [R2]     //a R4 asignamos el valor de R2(V izq)
MOV R5, [R3]     //a R5 asginamos valor de R3 (V der)
MOV [R2], R5     //asignamos valor almacenado en R5 a R2
MOV [R3], R4     //asignamos valor almacenado en R4 a R3
ADD R2, 4        //Movemos una posición R2(V izq)
SUB R3, 4        //Movemos una posición R2(V der)
JMP while     

end:
    RET              Salimos
