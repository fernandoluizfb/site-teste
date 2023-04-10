# site-teste

O objetivo desse site é buscar dados das cotações do dólar, euro, libra e dólar canadense via API do Banco Central, processá-los e criar um robô que envia as informações para o usuário no Telegram, conforme solicitado.

# Esse é repositório é um site que possui 

*   Robô em Telegram
*   Integração com o Google Sheets
*   Site em Flask
*   Uso da API do Banco Central

# Etapa 1

A primeira etapa é estabelecer uma configuração para que as informações sensíveis, como tokens e ID do bot, fiquem alocadas de forma segura.

# Etapa 2

Depois, é hora de criar as páginas no Flask.

# Etapa 3

Em seguida, é definido o dia de hoje, ontem e anteontem com a biblioteca datetime.

# Etapa 4

A etapa seguinte é quando o código usa a biblioteca do Banco Central para pegar as cotações das moedas.

# Etapa 5

Essas moedas são salvas em funções, como def dolar_ptax(), euro_ptax(), dolar_canadense_ptax() e libra_ptax(). Logo abaixo de cada função, é possível ver o dataframe de cada moeda, que será usado mais tarde para processar os dados.

# Etapa 6

Aí é hora de memorizar as cotações das moedas nos últimos quatro dias em variáveis, como dolar_hoje e dolar_ontem.

# Etapa 7

A partir dos dados dos dataframes das funções das diferentes moedas, é usado a função pct_change(periods=-1) para definir a variação da moeda de um dia para o outro. As variações também são salvas em funções, como dolar_percentual_hoje e dolar_percentual_ontem.

# Etapa 8

A última parte do código com as moedas é estabelecer funções com frases que serão exibidas para o usuário. Com 'if' e 'else', o código consegue exibir se uma determinada moeda subiu ou caiu e qual foi a sua variação.

# Etapa 9

A última parte é criar o robô do telegram via webhook. Para isso, ao invés do modelo get, é usada a biblioteca requests com o methods=["POST"]).

No caso desse robô, ele exibe as frases processadas sobre determinada moeda, de acordo com a solicitação do usuário. 
