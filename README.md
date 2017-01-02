# Pygame Engine para a 2ª UFSM GameJam
Game engine escrita em pygame 1.92 e python 3

O guia de estilo pra codificação que será usado é o pep8, o qual pode
ser encontrado no diretório **doc/** em formato de pdf. A mesma pasta
conterá itens referentes à documentação como um diagrama de classes.

Código fonte devem ser colocado dentro da pasta **src/** e resources do
jogo devem estar localizados em seus respectivos diretórios dentro de 
**etc/**

A ideia é manter uma engine compacta e simples de usar, mas com grande
potencial de implementação.

A ideia é basicamente a seguinte:

O sistema (_System_) contém uma pilha de cenas (_Scene_), sendo que a cena
do topo da pilha é a cena ativa.

Cada cena controla seus objetos (_GameObject_), e deve ser responsável com
interações entre eles, como colisão.

Cada objeto terá _keys_ referentes a alguns recursos gerenciado pelos 
_managers_ (imagem, som, fontes, etc), e sua renderização pode ser simples
ou controlada por alguma animação (_Animation_) 