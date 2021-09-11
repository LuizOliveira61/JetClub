import streamlit as st
import datetime

cotistas = [
    {
        'login': 'luizeduardo',
        'senha': 'luiz123',
        'nome': 'LUIZ EDUARDO',
        'lancha': ['Lancha 01', 'Lancha 02'],
        'status': 'Pago'
    },
    {
        'login': 'vicmendon',
        'senha': 'vic123',
        'nome': 'VICTOR',
        'lancha': ['Lancha 05'],
        'status': 'Pago'
    },    {
        'login': 'teste',
        'senha': 'testando123',
        'nome': 'Luiz Carlos JetClub',
        'lancha': ['Lancha 03', 'JETSKY 03'],
        'status': 'Devedor'
    },    {
        'login': 'admin',
        'senha': 'admin',
        'nome': 'ADMINISTRADOR',
        'lancha': ['Lancha 01', 'Lancha 02'],
        'status': 'Pago'
    }
            ]

st.title('Agendamento JetClub')

login = st.text_input(label='Login')
senha = st.text_input(label='Senha')

cotista = 'Não encontrado'

for x in cotistas:
    if login == x['login'] and senha == x['senha']:
        cotista = x['nome']
        status = x['status']

if cotista != 'Não encontrado':
    st.text(f'Bem vindo, {cotista}')

    dia1 = datetime.date(2021, 9, 20)

    marcados = [datetime.date(2021, 9, 20),
                datetime.date(2021, 9, 21),
                datetime.date(2021, 9, 22)]

    data = st.date_input(label='Data', value=None)

    agendamento = ''

    agendado = False

    for x in marcados:
        if data == x:
            st.error('Data já agendada')
            agendado = True

    if agendado == False:
        if st.button('Reservar') and agendado == False:
            if status == 'Pago':
                st.success('Reserva realizada com sucesso!')
            if status == 'Devedor':
                st.error('Acerte a sua mensalidade!')
