Carol - DE Challenge - Openflights
Este repositório tem por objetivo apresentar como utilizar o processamento de dados SQL unificado na plataforma Carol. 

O contexto é de um cliente que precisa visualizar por meio de um dashboard estatísticas de rotas de vôos e o resultado final pode ser visualizado [aqui](https://carol.ai/insights/dashboard/473-desafio).

As ferramentas utilizadas foram:

TOTVS Carol com processamento SQL unificado
Base de dados estática extraída do site [openflights](https://openflights.org/data.html)
Scritps em Python utilizando a biblioteca [pycarol](https://github.com/totvslabs/pyCarol) para criar estruturas e subir os dados.
Carol Insights Studio para geração de gráficos e dashboard

# 1. Clonagem do repositório
Ao clonar esse repositório, na pasta "data" estão localizados os arquivos .dat disponíveis no site openflights para download. Na pasta "ddl" (data definition language) estão os scripts para criação dos conectores e staging tables dentro da carol. Os scripts são nomeados convenientemente com o seguinte padrão "pycarol_nomedoarquivofonte.py". Na pasta raiz do repositório temos alguns scripts para ingestão de dados.

pycarol_senddata.py -> envia para a Carol os dados de todas as stagings do projeto.
pycarol_sendnewplanes.py -> envia para a Carol novos dados de aviões para a staging "planes", afim de simular uma ingestão contínua de dados.
OBS: as stagings devem estar préviamente criadas para executar esses scripts.

# 2. Carol
Após a clonagem do repositório (passo 1), devemos criar um tenant de desenvolvimento, onde iremos criar nosso Carol App com todos os conectores, staging tables, datamodels e pipelines necessárias para processamento de dados. A tenant criada para tal função foi a tenant brenopapadev. Também foi criada a tenant unificada brenopapaunif e três tenants de cliente brenopapa1, brenopapa2 e brenopapa3. Com isso, temos o panorama de tenants abaixo.

| Tenant        | Tipo           | Informações                                                                       |
| ------------- |:--------------:| :---------------------------------------------------------------------------------|
| [brenopapadev](https://datascience.carol.ai/brenopapa/carol-ui/home)  | DEV            |  Tenant onde será desenvolvido o Carol App                                        |
| [brenopapaunif](https://datascience.carol.ai/brenopapaunif/carol-ui/home)  | UNIFIED        |  Tenant que receberá dados das tenants customer e fará o processamento dos dados. |
| [brenopapa1](https://datascience.carol.ai/brenopapa1/carol-ui/home)     | CUSTOMER       |  Tenant que receberá os dados de um dos clientes.                                 |
| brenopapa2     | CUSTOMER       |  Tenant que receberá os dados de um dos clientes. Deletada no processo de validação de fluxos.                                |
| [brenopapa3](https://datascience.carol.ai/brenopapa1/carol-ui/home)     | CUSTOMER       |  Tenant que receberá os dados de um dos clientes.                                 |

OBS: todas as tenants criadas são SQL Processing Only.

## 2.1. Setup tenant brenopapadev
A maior parte do trabalho será feito dentro da tenant de desenvolvimento, já que é nela que iremos criar toda a estrutura para o nosso Carol App.
Com o repositório clonado, abra o script "pycarol_createconnector.py" e confira se há arquivo de credenciais para o script consumir, verifique se o atributo "domain" e "organization" estão preenchidos corretamente e execute o script. Após a execução será criado um conector e precisaremos do ID dele para os próximos passos. Anote o retorno do script ou entre na Carol e obtenha o ID do connector pela UI.

Com o ID do connector em mãos, abra os arquivos "pycarol_airlines.py", "pycarol_airports.py", "pycarol_countries", "pycarol_planes", "pycarol_routes", verifique os atributos "domain", "organization", "connector" e arquivo de credenciais. Execute cada um deles. Será criada uma staging table para cada script, utilizando a estrutura de cada um dos arquivos da pasta "data". A estrutura criada deve ser esta:

| Staging Table | Informações                                                                                    |
| ------------- |:---------------------------------------------------------------------------------------------- |
| airlines      | Reponsável por receber os dados brutos de linhas áereas. Vindos do arquivo .dat de mesmo nome. |
| airports      | Reponsável por receber os dados brutos de aeroportos. Vindos do arquivo .dat de mesmo nome.    |
| countries     | Reponsável por receber os dados brutos de países. Vindos do arquivo .dat de mesmo nome.        |
| planes        | Reponsável por receber os dados brutos de aviões. Vindos do arquivo .dat de mesmo nome.        |
| routes        | Reponsável por receber os dados brutos de rotas. Vindos do arquivo .dat de mesmo nome.         |

Ao final da criação das staging tables, podemos executar o script pycarol_senddata.py, que irá enviar os dados dos arquivos .dat para o intake da Carol, dados estes que serão depositados nas staging tables designadas.

✅ NOSSAS STAGINGS JÁ ESTÃO CRIADAS E POPULADAS COM DADOS ✅

O próximo passo é criarmos os datamodels que convenientemente estão com seus snapshots presentes na pasta "dms" (datamodels) desse repositório. Vá até a UI da Carol e crie os datamodels utilizando as snapshots disponibilizadas.

| Datamodel     | Informações                                                                                                             |
| ------------- |:----------------------------------------------------------------------------------------------------------------------- |
| airlines      | Reponsável por receber os dados processados pela pipeline SQL de linhas áereas. Vindos da staging table de mesmo nome.  |
| airports      | Reponsável por receber os dados processados pela pipeline SQL  de aeroportos. Vindos da staging table de mesmo nome.    |
| countries     | Reponsável por receber os dados processados pela pipeline SQL  de países. Vindos da staging table de mesmo nome.        |
| planes        | Reponsável por receber os dados processados pela pipeline SQL  de aviões. Vindos da staging table de mesmo nome.        |
| routes        | Reponsável por receber os dados processados pela pipeline SQL  de rotas. Vindos da staging table de mesmo nome.         |

Com os datamodels criados, agora precisamos de pipelines para processar os dados brutos presentes nas staging tables e inserir os dados tratados nos datamodels. Para isso, basta utilizar as pipelines presentes na pasta "dml" (data manipulation language) desse repositório. As pipelines podem ser executadas localmente no VScode, porém o nosso Carol App terá processamento por pipelines vinculado ao GitHub, que será descrito em seguida. Execute as pipelines para verificar se tudo foi criado corretamente e os dados das stagings estão chegando nos datamodels da maneira que deseja. Faça ajustes nas pipelines conforme achar necessário.

✅ NOSSOS DATAMODELS JÁ ESTÃO CRIADOS E POPULADAS COM DADOS VINDOS DAS STAGINGS ✅

## 2.2. Carol App
Com toda a estrutura de dados (stagings, datamodels e pipelines) criados no nosso tenant de desenvolvimento, precisamos criar uma tenant para ser a tenant unificada, que receberá os dados de todos os tenants customer vinculados ao mesmo Carol App. Crie uma tenant com a flag "Unified Tenant" marcada. Volte a tenant de desenvolvimento e inicie a criação do Carol App para "empacotar" tudo que foi criado até agora. Na tela de criação de Carol App, você verá todos os conectores, stagings e datamodels criados. Se tudo estiver OK, crie o Carol App com as seguintes configurações.

| Configuração        | Informações                                                                                                                           |
| ------------------- |:------------------------------------------------------------------------------------------------------------------------------------- |
| Label e Nome        | Servem para identificação lógica e visual do seu Carol App.                                                                           |
| Version             | Serve para identificar a versão atual do Carol App.                                                                                   |
| Unified Tenant      | Identifica qual tenant será a tenant unificada desse Carol App, todos os clientes com esse Carol App enviarão dados para essa tenant. |
| Processing Strategy | Aqui será selecionado SQL, para seguirmos as práticas mais atuais da plataforma.                                                      |

É importante vincularmos nosso Carol App a um repositório no Github, assim as pipelines irão aparecer no nosso tenant e em todos os tenants com o App instalado, para que sejam processadas. Para isso, é necessário logar com o Github e apontar para um repositório, além de ter um arquivo pipelines.json dentro dele, que será solicitado para que a Carol encontre as pipelines, quais dados de stagings serão usados em cada pipeline e qual datamodel será populado em cada pipeline. Há um arquivo nesse repositório que serve de exemplo e já funciona com a estrutura desse projeto, caso tenha seguido todos os passos até aqui.

Realize a release do Carol App. O Carol App criado nesse desafio foi [este](https://datascience.carol.ai/brenopapa/carol-ui/carol-app-dev/569034f7a61046aba9230cbc17c025af/overview).

✅ CAROL APP CRIADO ✅

## 2.3. Tenants Customer
Agora podemos criar as tenants customer, apenas criando a tenant sem marcar "Unified Tenant". Após a criação, devemos instalar o Carol App na tenant e a mesma já será vinculada a tenant unificada.

# 3. Processamento unificado
Com toda a estrutura criada, agora temos um cenário onde sempre que as tenants com o Carol App instalado recebam dados nas stagings, automaticamente a Carol envia esses dados para a tenant unificada. A tenant unificada irá processar os dados utilizando as pipelines e depositar esses dados tratados nos datamodels. Pelo campo mdmTenantId os dados são divididos e enviados corretamente para cada tenant de cliente em seus datamodels respectivos.

# 4. Gerando insights a partir dos dados processados
Nesse projeto utilizamos o Carol Insights para apresentar dados dos tenants. Para habilitar essa integração, é necessário ir até a aba "Tenant Admin" > "Tokens" para gerar uma Google Service Account, para integrar ao Metabase presente no Carol Insights. O dashboard final pode ser acessado [aqui](https://carol.ai/insights/dashboard/473-desafio) e está apontado para a tenant unificada.

# 5. DAEN-2019 - Validação de fluxos.
Esse repositório, Carol App e tenants foram alvo da issue [DAEN-2019](https://totvslabs.atlassian.net/browse/DAEN-2019), dessa forma, foram validados outros fluxos além do desafio de data engineering. Portanto, algumas estruturas podem estar um pouco diferentes do resultado final ao seguir esse passo-a-passo. O resultado da validação de fluxos está na issue.