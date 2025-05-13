Para motivos de segurança, não publiquei as chaves de autenticação do google no projeto.
Utilize o e-mail do grupo do projeto e acesse https://console.cloud.google.com/ na parte de "APIs e Serviços" / Credenciais para encontrar as chaves.
Depois é só abrir o arquivo "settings.py" e inserir entre apóstrofos nos seguintes campos:

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = 'INSIRA_A_ID_DO_CLIENTE_AQUI'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'INSIRA_A_CHAVE_SECRETA_DO_CLIENTE_AQUI'
