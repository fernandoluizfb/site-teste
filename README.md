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
