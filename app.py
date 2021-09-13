import time
from datetime import datetime
import streamlit as st
from PIL import Image
import sqlite3

#==============================
def conectar_db():

    con = sqlite3.connect('jetclub.db')
    cursor = con.cursor()

    return con, cursor


def cria_db():
    con = sqlite3.connect('jetclub.db')
    cursor = con.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS jetclub
                      (cota UNIQUE, login UNIQUE, senha, nome, lanchas, status, agenda, dias_utilizados)''')
    con.commit()
    con.close()


def add_login(cota, login, senha, nome, lanchas, status, agenda):
    con, cursor = conectar_db()
    cursor.execute(f'INSERT INTO jetclub VALUES ({cota}, "{login}", "{senha}", "{nome}", "{lanchas}", "{status}", "{agenda}")')

    con.commit()
    con.close()


def consultar_db(login):
    con, cursor = conectar_db()

    pesquisa = cursor.execute(f"select * from jetclub WHERE login = '{login}'")
    infos = pesquisa.fetchall()
    #print(infos)
    senha = infos[0][2]
    nome = infos[0][3]
    lanchas = infos[0][4]
    status = infos[0][5]
    agenda = infos[0][6]

    #print(agenda)

    con.commit()
    con.close()

    return nome, senha, lanchas, status, agenda


def conserta_data(info, nova_data):
    lista = []
    info = info.replace("'",'').replace('\\','').replace('\t','').replace(' ','').replace('[','').replace(']','')
    info = info.split(',')
    lista.append(nova_data)
    for x in info:
        lista.append(x)
    lista = str(lista)
    lista = lista.replace("'",'').replace('\\','').replace('\t','').replace(' ','').replace('[','').replace(']','')
    return lista


def add_cotista(nome, nascimento, cpf, endereco, bairro, cidade, uf, login, senha, lancha, status, email, celular):

    con, cursor = conectar_db()

    cursor.execute(f"INSERT INTO cotistas VALUES (NULL, '{nome}', '{nascimento}', '{cpf}', '{endereco}', '{bairro}',"
                   f" '{cidade}', '{uf}', '{login}', '{senha}', '{lancha}', '{status}', '{email}', '{celular}')")

    con.commit()
    con.close()


def add_data(login, cotista, lancha, data):

    data = data.split('/')
    dia = data[0]
    mes = data[1]
    ano = data[2]
    data = f'{dia}/{mes}/{ano}'

    con, cursor = conectar_db()

    now = datetime.now()
    now = now.strftime("%d/%m/%Y %H:%M:%S")
    print(now)

    cursor.execute(f"INSERT INTO agendamentos VALUES (NULL, '{login}', '{cotista}', '{lancha}', '{now}', '{data}')")

    con.commit()
    con.close()


def add_log(login, registro):

    con, cursor = conectar_db()

    now = datetime.now()
    now = now.strftime("%Y/%m/%d - %H:%M:%S")

    cursor.execute(f"INSERT INTO log VALUES (NULL, '{login}', '{registro}', '{now}')")

    con.commit()
    con.close()


def add_utilizados(login, data):
    con, cursor = conectar_db()

    nome, senha, lanchas, status, agenda = consultar_db(login)

    agenda_nova = conserta_data(marcado, data)

#    agenda.append(data)

#    agenda = str(agenda)

    cursor.execute(f"UPDATE jetclub SET dias_utilizados = '{agenda_nova}' WHERE login = '{login}'")
    #cursor.execute(f"INSERT INTO jetclub VALUES ('{data}')")

    con.commit()
    con.close()


def del_data(data):

    con, cursor = conectar_db()

    cursor.execute(f"DELETE from agendamentos WHERE DATA_AGENDADA = '{data}'")

    con.commit()
    con.close()


def conserta_data2(info, nova_data):
    lista = []
    info = info.replace("'",'').replace('\\','').replace('\t','').replace(' ','').replace('[','').replace(']','')
    info = info.split(',')
    for x in info:
        if nova_data != x:
            lista.append(x)
    lista = str(lista)
    lista = lista.replace("'",'').replace('\\','').replace('\t','').replace(' ','').replace('[','').replace(']','')
    return lista


def remove_data(login, data):
    con, cursor = conectar_db()

    nome, senha, lanchas, status, agenda = consultar_db(login)

    agenda_nova = conserta_data2(agenda, data)

#    agenda.append(data)

#    agenda = str(agenda)

    cursor.execute(f"UPDATE jetclub SET agenda = '{agenda_nova}' WHERE login = '{login}'")
    #cursor.execute(f"INSERT INTO jetclub VALUES ('{data}')")

    con.commit()
    con.close()


def consultar_marcados(lancha):
    con, cursor = conectar_db()

    datas_marcadas = []
    datas_marcadas_pessoa = []
    nomes = []
    pesquisa = cursor.execute(f"select * from jetclub WHERE lanchas = '{lancha}'")
    infos = pesquisa.fetchall()
    senha = infos[0][2]
    nome = infos[0][3]
    lanchas = infos[0][4]
    status = infos[0][5]
    agenda = infos[0][6]

    for x in infos:
        # nome = x[3]
        datas = x[3].split(',')
        for y in datas:
            datas_marcadas.append(y)
            # for x in nomes:
            #     datas_marcadas_pessoa.append(data)


    print(nomes)

    print(datas_marcadas_pessoa)



    # for x in infos:
    #     nome = x[3].split(',')
    #     for y in nome:
    #         nomes.append(y)



    print(datas_marcadas)

    con.commit()
    con.close()

    return datas_marcadas


def cons_marcados_por_nome(nome):

    con, cursor = conectar_db()

    datas_marcadas = []
    pesquisa = cursor.execute(f"select * from agendamentos WHERE NOME = '{nome}'")
    infos = pesquisa.fetchall()

    for x in infos:
        datas_marcadas.append({'nome': x[2],
                               'data': x[5],
                               'lancha': x[3]})

    con.commit()
    con.close()

    return datas_marcadas


def cons_marcados_geral(lancha):

    con, cursor = conectar_db()

    datas_marcadas = []
    pesquisa = cursor.execute(f"select * from agendamentos WHERE LANCHA = '{lancha}'")
    infos = pesquisa.fetchall()

    for x in infos:
        datas_marcadas.append({'lancha': x[3],
                               'data': x[5],
                               'nome': x[2],
                               })

    con.commit()
    con.close()

    return datas_marcadas


def consultar_agenda(lancha):
    con, cursor = conectar_db()

    datas_marcadas_pessoa = []
    nomes = []
    pesquisa = cursor.execute(f"select * from jetclub WHERE lanchas = '{lancha}'")
    infos = pesquisa.fetchall()
    senha = infos[0][2]
    nome = infos[0][3]
    lanchas = infos[0][4]
    status = infos[0][5]
    agenda = infos[0][6]

    for x in infos:
        # nome = x[3]
        datas = x[3].split(',')
        for y in datas:
            datas_marcadas.append(y)
            # for x in nomes:
            #     datas_marcadas_pessoa.append(data)


    print(nomes)

    print(datas_marcadas_pessoa)



    # for x in infos:
    #     nome = x[3].split(',')
    #     for y in nome:
    #         nomes.append(y)



    print(datas_marcadas)

    con.commit()
    con.close()

    return datas_marcadas


def cons_cotista(login):

    con, cursor = conectar_db()

    pesquisa = cursor.execute(f"select * from cotistas WHERE LOGIN = '{login}'")
    infos = pesquisa.fetchall()
    print(infos)

    cotistas = []
    for x in infos:
        id_cotista = x[0]
        nome = x[1]
        login = x[8]
        senha = x[9]
        lancha = x[10]
        status = x[11]
        cotistas.append({'id': id_cotista,
                         'nome': nome,
                         'login': login,
                         'senha': senha,
                         'lancha': lancha,
                         'status': status
                             })

    con.commit()
    con.close()

    return cotistas


def cons_todos_agendamentos():
    con, cursor = conectar_db()

    pesquisa = cursor.execute(f"select * from agendamentos")
    infos = pesquisa.fetchall()

    agendamentos = []
    for x in infos:
        id_evento = x[0]
        marcador = x[1]
        cotista = x[2]
        lancha = x[3]
        evento = x[4]
        data = x[5]
        agendamentos.append({'id': id_evento,
                             'marcador': marcador,
                             'cotista': cotista,
                             'lancha': lancha,
                             'evento': evento,
                             'data': data
                             })


    # infos_len = len(infos)
    #
    # agendamentos = []
    # for x in range(infos_len):
    #     ret_datas = infos[x][6]
    #     ret_datas = str(ret_datas).split(',')
    #     # print(f'LEN DATAS: {len(ret_datas)}')
    #     if len(ret_datas) > 0:
    #         for y in ret_datas:
    #             if y != None and y != '' and y != ' ':
    #                 ret_lancha = infos[x][4]
    #                 ret_cotista = infos[x][3]
    #                 agendamentos.append({'cotista': ret_cotista,
    #                                      'lancha': ret_lancha,
    #                                      'data': y})
    #
    # print(agendamentos)

    con.commit()
    con.close()

    return agendamentos


def cons_todos_agendamentos_sem_id():
    con, cursor = conectar_db()

    pesquisa = cursor.execute(f"select * from agendamentos")
    infos = pesquisa.fetchall()

    agendamentos = []
    for x in infos:
        id_evento = x[0]
        marcador = x[1]
        cotista = x[2]
        lancha = x[3]
        evento = x[4]
        data = x[5]
        agendamentos.append({'marcador': marcador,
                             'cotista': cotista,
                             'lancha': lancha,
                             'evento': evento,
                             'data': data
                             })


    # infos_len = len(infos)
    #
    # agendamentos = []
    # for x in range(infos_len):
    #     ret_datas = infos[x][6]
    #     ret_datas = str(ret_datas).split(',')
    #     # print(f'LEN DATAS: {len(ret_datas)}')
    #     if len(ret_datas) > 0:
    #         for y in ret_datas:
    #             if y != None and y != '' and y != ' ':
    #                 ret_lancha = infos[x][4]
    #                 ret_cotista = infos[x][3]
    #                 agendamentos.append({'cotista': ret_cotista,
    #                                      'lancha': ret_lancha,
    #                                      'data': y})
    #
    # print(agendamentos)

    con.commit()
    con.close()

    return agendamentos


def cons_log_geral():

    con, cursor = conectar_db()

    pesquisa = cursor.execute(f"select * from log")
    infos = pesquisa.fetchall()

    log = []
    for x in infos:
        id_log = x[0]
        login = x[1]
        registro = x[2]
        data = x[3]
        log.append({'id': id_log,
                    'login': login,
                    'registro': registro,
                    'data': data
                    })

    con.commit()
    con.close()

    return log

#==============================

# image = Image.open('foto.jpg')

# st.image(image, use_column_width=True)

# cons_cotista('vicmendon')

login = st.sidebar.text_input(label='Login')
login = login.lower()

senha_digitada = st.sidebar.text_input(label='Senha', type='password')

ret_cotista = cons_cotista(login)

senha = 'não digitada'

if len(ret_cotista) > 0:
    nome = ret_cotista[0]['nome']
    senha = ret_cotista[0]['senha']
    lancha = ret_cotista[0]['lancha']
    status = ret_cotista[0]['status']
if len(ret_cotista) == 0 and login != '':
    st.sidebar.error('Usuário não encontrado')

cotista = 'Não encontrado'

if senha == senha_digitada:
    add_log(login, f'Usuário logado com Sucesso!')
    cotista = nome
    status = status
    barco = lancha
elif senha_digitada != senha and senha_digitada != '':
    st.sidebar.error('Senha incorreta!')
    add_log(login, f'Senha incorreta ({senha_digitada})')


if cotista != 'Não encontrado' and cotista != 'Administrador':

    todos_marcados = cons_marcados_geral(barco)

    st.title(f'JetClub')

    st.sidebar.text(f'Bem vindo, {cotista}')

    st.sidebar.text('Agendamentos')

    if len(todos_marcados) > 0:
        with st.expander(label=f'{len(todos_marcados)} dias indisponíveis'):
            if todos_marcados:
                st.header(f'Datas agendadas - {lancha}')
                st.table(data=todos_marcados)

    now = datetime.now()
    zerado = now.replace(now.year, now.month, 1)

    data = st.date_input(label='Agendar dia', value=zerado, min_value=now)

    dia = data.day
    mes = data.month
    ano = data.year

    marcacao = f'{dia}/{mes}/{ano}'

    hoje = datetime.now()

    agendamento = ''

    agendado = False

    agendados = []
    for data_marcada in todos_marcados:
        agendados.append(data_marcada['data'])

    for x in agendados:
        print(x)
        y = x.split('/')
        dia = int(y[0])
        mes = int(y[1])
        ano = int(y[2])

        agora = datetime.now()
        marcado = agora.replace(ano, mes, dia, 18, 00, 00)
        print(marcado < agora)
        if marcado <= hoje:
            del_data(x)
            # add_utilizados(login, marcacao)
            # remove_data(login, x)
            st.experimental_rerun()


    marcados = cons_marcados_por_nome(nome)
    # st.write(marcados)

    for data_cotista in marcados:
        form = st.sidebar.form(key=data_cotista['data'])
        form.text(f'{data_cotista["lancha"]} - {data_cotista["data"]}')
        submit = form.form_submit_button('Remover Agendamento')
        if submit:
            del_data(data_cotista['data'])
            add_log(login, f'Removeu Agendamento {data_cotista["data"]}')
            form.success('Agendamento removido com sucesso!')
            time.sleep(.3)
            st.experimental_rerun()

    #========================================================================= mexer daqui pra baixo
    for x in agendados:
        print(f'AGENDADOS: {x}')
        if marcacao == x:
            st.error(f'Dia {marcacao} já agendado!')
            agendado = True

    if agendado is False:
        if st.button('Reservar'):
            if status == 'Pago':
                # marcou = 0
                # for x in marcados:
                #     print(f'MARCADOS: {len(marcados)}')
                #     if x != '':
                #         marcou += 1
                if len(marcados) >= 3:
                    st.error('Limite de Agendamenos esgotado!')
                else:
                    add_data(login, cotista, lancha, marcacao)
                    add_log(login, f'Reservou para o dia {marcacao}!')
                    st.success(f'Reserva realizada com sucesso para o dia {marcacao}!')
                    time.sleep(1)
                    st.experimental_rerun()
            if status == 'Devedor':
                st.error('Acerte a sua mensalidade!')

if cotista == 'Administrador':

    st.sidebar.write('Logado como Administrador')
    st.title('Administração')

    painel = st.selectbox(label='Painel de Controle', options=['[SELECIONE]',
                                                               'Consultar Agendamentos',
                                                               'Editar Agendamentos',
                                                               'Histórico de Uso',
                                                               'Cadastrar Cotista',
                                                               'Alterar Status de Pagamento',
                                                               'Log de eventos'])

    if painel == 'Consultar Agendamentos':

        # IDEIAS
        # ADICIONAR A OPÇÃO DE AGENDAMENTOS NO DIA, PRÓXIMO DIA, PRÓXIMA SEMANA E POR DATA ESPECÍFICA
        # TAMBÉM A IMPLEMENTAÇÃO DE FILTROS DE PESQUISA (POR NOME, DATA, COTISTA)

        todos_agendamentos = cons_todos_agendamentos_sem_id()

        # container1 = st.container()
        # aba = container1.expander('Veja mais:', expanded=False)
        # aba.text('teste')


        # filtros = containerConsAgenda.expander(label='Filtros de pesquisa', expanded=False)
        #
        # checkGeral = filtros.checkbox(label='Geral', value=True)
        # # filtros.selectbox('', options=['Geral',
        # #                                'Por Cotista',
        # #                                'Por Embarcação',
        # #                                'Por Data'], index=0)

        containerConsAgenda = st.container()
        containerConsAgenda.header('Eventos agendados')
        containerConsAgenda.dataframe(data=todos_agendamentos)

    elif painel == 'Editar Agendamentos':

        todos_agendamentos = cons_todos_agendamentos()

        for linha in todos_agendamentos:
            st.text(linha)

        containerEditAgenda = st.container()
        containerEditAgenda.header('Editar agendamentos')
        containerEditAgenda.info('Selecione o agendamento que deseja alterar')
        containerEditAgenda.selectbox('', options=todos_agendamentos)


    elif painel == 'Cadastrar Cotista':

        st.header('Formulário de cadastro')

        with st.form(key='cadastra_cotista') as form_cad:
            cad_nome = st.text_input(label='Nome', max_chars=50)
            cad_nome = cad_nome.title()
            if len(cad_nome) < 5 and cad_nome != '':
                st.error('Preencha Nome e Sobrenome')
                cad_nome = ''
            dataantiga = datetime.now()
            menos18 = dataantiga.replace(2003, 1, 1)
            cad_nascimento = st.date_input(label='Nascimento', value=menos18, min_value=menos18)

            cad_nascimento = cad_nascimento.strftime("%d/%m/%Y")

            st.write(cad_nascimento)

            cad_cpf = st.text_input(label='CPF (apenas números)', help='CPF requer 11 dígitos', max_chars=11)
            len_cpf = len(cad_cpf)
            try:
                cad_cpf = int(cad_cpf)
                if len_cpf != 11:
                    st.error('Padrão de CPF incorreto.')
            except Exception as e:
                if cad_cpf != '':
                    st.error('O campo CPF aceita apenas números')
            cad_login = st.text_input(label='Login', help='Apenas letras e sem espaços')
            if ' ' in cad_login:
                st.error('o Login não pode ter espaços')
                cad_login = ''
            cad_senha = st.text_input(label='Senha', type='password', help='Entre 6 e 16 caracteres. Letra maiúscula, letra minúscula, números e caracteres especiais (** ! @ # $ % * **)')
            minuscula = False
            maiuscula = False
            numero = False
            simbolo = False
            letra = False
            carac_espec = ['!', '@', '#', '$', '%', '*']
            nums = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
            if len(cad_senha) > 5 and len(cad_senha) < 17:
                for x in cad_senha:
                    if x in carac_espec:
                        simbolo = True
                    if x in nums:
                        numero = True
                    if x.isupper():
                        maiuscula = True
                    if x.islower():
                        minuscula = True
            else:
                if cad_senha != '':
                    st.error('Senha muito pequena')
                    cad_senha = ''
            if simbolo is True and numero is True and maiuscula is True and minuscula is True:
                cad_senha = cad_senha
            else:
                cad_senha = ''
                if cad_senha != '':
                    st.error('Senha necessita ter entre 6 e 16 caracteres. Letra maiúscula, letra minúscula, números e caracteres especiais (** ! @ # $ % * **)')
            cad_email = st.text_input(label='Email')
            if '@' not in cad_email and cad_email != '':
                st.error('Preencha um email válido!')
                cad_email = ''
            cad_celular = st.text_input(label='Celular (somente números)', max_chars=11)
            try:
                cad_celular = int(cad_celular)
            except Exception as e:
                cad_celular = ''
                if cad_celular != '':
                    st.error('Digite apenas NÚMEROS')

            st.markdown('<hr>', True)

            cad_endereco = st.text_input(label='Endereço (opcional)')
            cad_bairro = st.text_input(label='Bairro (opcional)')
            cad_cidade = st.text_input(label='Cidade (opcional)')
            cad_uf = st.text_input(label='UF (opcional)')

            st.markdown('<hr>', True)

            cad_lancha = st.selectbox(label='Embarcação', options=['[SELECIONE]', 'Jet 1', 'Jet 2', 'Lancha 1', 'Lancha 2'])
            if cad_lancha == '[SELECIONE]':
                cad_lancha = ''
            cad_status = st.selectbox(label='Status de Pagamento', options=['[SELECIONE]', 'Pago', 'Devedor'])
            if cad_status == '[SELECIONE]':
                cad_status = ''

            st.markdown('', True)

            submit = st.form_submit_button(label='Cadastrar')

        if submit:
            if cad_nome != '' and cad_cpf and cad_login != '' and cad_senha and cad_email and cad_celular and cad_lancha != '' and cad_status!= '':
                try:
                    add_cotista(cad_nome, cad_nascimento, cad_cpf, cad_endereco, cad_bairro, cad_cidade, cad_uf, cad_login, cad_senha, cad_lancha, cad_status, cad_email, cad_celular)
                    st.success('Usuário cadastrado com Sucesso!')
                    time.sleep(3)
                    st.experimental_rerun()
                except Exception as e:
                    st.write(e)
            else:
                st.error('Preencha os campos corretamente!')


    elif painel == 'Log de eventos':

        st.header('Log de eventos')

        logs = cons_log_geral()

        st.dataframe(data=logs)