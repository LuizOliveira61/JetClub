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

#add_login(3, 'vicmendon', '123', 'Victor', ['Itaipu','Paquetá'], 'Pago', ' ')

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


# def add_data(login, data):
#     con, cursor = conectar_db()
#
#     nome, senha, lanchas, status, agenda = consultar_db(login)
#
#     agenda_nova = conserta_data(agenda, data)
#
# #    agenda.append(data)
#
# #    agenda = str(agenda)
#
#     cursor.execute(f"UPDATE jetclub SET agenda = '{agenda_nova}' WHERE login = '{login}'")
#     #cursor.execute(f"INSERT INTO jetclub VALUES ('{data}')")
#
#     con.commit()
#     con.close()

def add_cotista(nome, login, senha, lancha, status):

    con, cursor = conectar_db()

    cursor.execute(f"INSERT INTO cotistas VALUES (NULL, '{nome}', '{login}', '{senha}', '{lancha}', '{status}')")

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
        login = x[2]
        senha = x[3]
        lancha = x[4]
        status = x[5]
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

#==============================

# image = Image.open('foto.jpg')

# st.image(image, use_column_width=True)

# cons_cotista('vicmendon')

login = st.sidebar.text_input(label='Login')

senha_digitada = st.sidebar.text_input(label='Senha', type='password')

ret_cotista = cons_cotista(login)

senha = 'não digitada'

if len(ret_cotista) > 0:
    nome = ret_cotista[0]['nome']
    senha = ret_cotista[0]['senha']
    lancha = ret_cotista[0]['lancha']
    status = ret_cotista[0]['status']
if len(ret_cotista) == 0:
    st.sidebar.error('Usuário não encontrado')

cotista = 'Não encontrado'

if senha == senha_digitada:
    add_log(login, f'Usuário logado com Sucesso!')
    cotista = nome
    status = status
    barco = lancha
elif senha_digitada != senha:
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
                                                               'Cadastrar Cotista'])

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

    if painel == 'Editar Agendamentos':

        todos_agendamentos = cons_todos_agendamentos()

        for linha in todos_agendamentos:
            st.text(linha)

        containerEditAgenda = st.container()
        containerEditAgenda.header('Editar agendamentos')
        containerEditAgenda.info('Selecione o agendamento que deseja alterar')
        containerEditAgenda.selectbox('', options=todos_agendamentos)

    if painel == 'Cadastrar Cotista':

        st.header('Formulário de cadastro')
