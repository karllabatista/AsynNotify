# Trocas arquiteturas

### Porque troca a fila de mensagens de Redis para apache Kafka?

Essa ideia de troca de filas de mensagens comecou quando surgiu a ideia de implementar idempotencia.
Idempotenica eh uma proporiedade que permiter que uma acao seja executada mutliplas vezes mas o seu 
resultado permanece o mesmo depois da primeira execucao e seu resultado.

No cenario de envio de notificacoes assincronas, a idempotencia funciona da seguinte forma:

Consumer side:

    - O consumer consome as mensagens da fila (Redis fila)
    
    Pergunta: Nesse cenario, a aplicacao consumer sabe se uma mensagem ja foi consumida ou nao? Existe uma verificacao
              para saber se uma mensagem foi processada duas vezes?

              r= A aplicacao consumer nao consegue identificar uma mensagem duplicada por que nao existe uma logica
                implementada para verificar isso.


    Pergunta: Se no momento que o consumer estiver processando uma mensagem, o servico do consumidor cair,
             o que acontece com a mensagem? Uma vez que ela foi retirada da fila Redis, cuja implementacao eh uma lista?

             r=  Na arquitetura atual, o consumer tira a mensagem da fila. Na fila nao existe um "backup" de mensagens.Entao 
             se o consumer ficar fora do ar no processamento, a mensagem se perde. Outro detalhe, eh que a fila usando redis
             nao consegue reenviar uma mensagem porque o redis nao tem um mecanismo de retry e ainda mais uma mecanismo que saiba que o consumidor conseguiu consumir a mensagem com sucesso e que "pode descartar essa mensagem" da fila
 

**Conclusao**:
A decisão de trocar Redis (usado como fila de mensagens) por Apache Kafka está fundamentada na necessidade de aumentar a confiabilidade, resiliência e durabilidade no processamento de eventos. Embora Redis seja extremamente rápido e eficiente como cache e armazenamento em memória, sua implementação de filas com listas ou pub/sub não oferece garantias fortes sobre entrega e persistência de mensagens.

1. Perda de mensagens

**Redis (listas/pubsub)**:

No modelo de lista (LPOP), uma vez que o consumidor retira a mensagem da fila, ela deixa de existir. Se o consumidor falhar durante o processamento, a mensagem é perdida.

No modelo pub/sub, consumidores que não estão ativos simplesmente não recebem as mensagens.

**Kafka (tópicos)**:

Kafka persiste todas as mensagens em disco por um período configurável, independentemente de consumo.

O consumidor controla seu progresso por meio de offsets. Se cair no meio do processamento, pode retomar do último offset confirmado.

Isso elimina o risco de perda de mensagens durante falhas temporárias.


2. Confiabilidade

Redis não possui um mecanismo nativo de acknowledgment para confirmar que o consumidor realmente processou a mensagem.

Kafka fornece uma semântica clara de entrega:

At least once → garante que nenhuma mensagem é perdida, mas pode haver duplicações.

Exactly once → garante processamento único com o suporte de idempotência.

Isso garante que mensagens não desapareçam silenciosamente no caminho.

3. Resiliência

Em Redis, se o consumidor ficar indisponível, as mensagens que foram retiradas da fila não têm backup.

Em Kafka, a mensagem continua disponível no log até que todos os consumidores confirmem o processamento. Isso torna o sistema mais resiliente a falhas de rede, crashes de aplicações ou reinícios de serviços.

4. Escalabilidade

Redis trabalha bem em cenários simples de fila, mas não tem suporte nativo para múltiplos consumidores em grupos, com balanceamento automático de carga.

Kafka foi projetado para processamento distribuído em larga escala, permitindo múltiplos consumidores em grupos de consumo, paralelismo via partições e retenção de histórico de mensagens para reprocessamento.