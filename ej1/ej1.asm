; /** defines bool y puntero **/
%define NULL 0
%define TRUE 1
%define FALSE 0

section .data
empty_str db 0   ; Cadena vacía (solo el carácter nulo)

section .text

global string_proc_list_create_asm
global string_proc_node_create_asm
global string_proc_list_add_node_asm
global string_proc_list_concat_asm

; FUNCIONES auxiliares que pueden llegar a necesitar:
extern malloc
extern free
extern str_concat


string_proc_list_create_asm:
    ; Guardar el frame pointer
    push rbp
    mov rbp, rsp
    
    ; Llamar a malloc para alocar el tamaño de string_proc_list
    mov rdi, 16      ; sizeof(string_proc_list) = 16 bytes (2 punteros de 8 bytes)
    call malloc
    
    ; Verificar si malloc devolvió NULL
    test rax, rax
    jz .done
    
    ; Inicializar first y last a NULL
    mov qword [rax], NULL    ; list->first = NULL
    mov qword [rax+8], NULL  ; list->last = NULL
    
.done:
    ; Restaurar frame pointer y retornar
    pop rbp
    ret

string_proc_node_create_asm:
    ; Guardar frame pointer y registros que necesitamos preservar
    push rbp
    mov rbp, rsp
    push rbx        ; Preservar rbx
    push r12        ; Preservar r12
    
    ; Guardar parámetros (type en rdi, hash en rsi)
    mov rbx, rdi    ; rbx = type
    mov r12, rsi    ; r12 = hash
    
    ; Llamar a malloc para alocar el tamaño de string_proc_node
    mov rdi, 32     ; sizeof(string_proc_node) = 32 bytes
    call malloc
    
    ; Verificar si malloc devolvió NULL
    test rax, rax
    jz .done
    
    ; Inicializar los campos del nodo
    mov qword [rax], NULL    ; node->next = NULL
    mov qword [rax+8], NULL  ; node->previous = NULL
    mov byte [rax+16], bl    ; node->type = type (byte bajo de rbx)
    mov [rax+24], r12        ; node->hash = hash
    
.done:
    ; Restaurar registros y frame pointer
    pop r12
    pop rbx
    pop rbp
    ret

string_proc_list_add_node_asm:
    ; Guardar frame pointer y registros necesarios
    push rbp
    mov rbp, rsp
    push rbx        ; Preservar rbx
    push r12        ; Preservar r12
    push r13        ; Preservar r13
    
    ; Guardar parámetros (list en rdi, type en rsi, hash en rdx)
    mov rbx, rdi    ; rbx = list
    mov r12, rsi    ; r12 = type
    mov r13, rdx    ; r13 = hash
    
    ; Crear nuevo nodo: llamar a string_proc_node_create_asm
    mov rdi, r12    ; type
    mov rsi, r13    ; hash
    call string_proc_node_create_asm
    
    ; El nodo creado está en rax
    ; Verificar si la lista está vacía
    cmp qword [rbx], NULL    ; if (list->first == NULL)
    jne .list_not_empty
    
    ; Lista vacía
    mov [rbx], rax           ; list->first = new_node
    mov [rbx+8], rax         ; list->last = new_node
    jmp .done
    
.list_not_empty:
    ; Conectar el nuevo nodo al final
    mov rdx, [rbx+8]         ; rdx = list->last
    mov [rax+8], rdx         ; new_node->previous = list->last
    mov [rdx], rax           ; list->last->next = new_node
    mov [rbx+8], rax         ; list->last = new_node
    
.done:
    ; Restaurar registros y frame pointer
    pop r13
    pop r12
    pop rbx
    pop rbp
    ret

string_proc_list_concat_asm:
    ; Guardar frame pointer y registros necesarios
    push rbp
    mov rbp, rsp
    push rbx        ; Preservar rbx
    push r12        ; Preservar r12
    push r13        ; Preservar r13
    push r14        ; Preservar r14
    push r15        ; Preservar r15
    
    ; Guardar parámetros (list en rdi, type en rsi, hash en rdx)
    mov rbx, rdi    ; rbx = list
    mov r12b, sil   ; r12b = type (byte)
    mov r13, rdx    ; r13 = hash
    
    ; Hacer una copia del hash inicial usando str_concat("", hash)
    mov rdi, empty_str  ; String vacío VÁLIDO (no un NULL)
    mov rsi, r13        ; hash
    call str_concat
    mov r14, rax        ; r14 = result (copia del hash)
    
    ; Obtener el primer nodo
    mov r15, [rbx]  ; r15 = list->first
    
.loop_concat:
    ; Verificar si hemos llegado al final de la lista
    test r15, r15
    jz .done_concat
    
    ; Verificar si el tipo coincide
    mov al, byte [r15+16]   ; al = node->type
    cmp al, r12b
    jne .next_node
    
    ; El tipo coincide, concatenar
    mov rdi, r14            ; Primer parámetro: result actual
    mov rsi, [r15+24]       ; Segundo parámetro: node->hash
    call str_concat
    
    ; Liberar resultado anterior y actualizar
    mov rdi, r14
    mov r14, rax            ; Guardar nuevo resultado
    call free
    
.next_node:
    ; Avanzar al siguiente nodo
    mov r15, [r15]          ; r15 = r15->next
    jmp .loop_concat
    
.done_concat:
    ; Devolver el resultado final
    mov rax, r14
    
    ; Restaurar registros y frame pointer
    pop r15
    pop r14
    pop r13
    pop r12
    pop rbx
    pop rbp
    ret