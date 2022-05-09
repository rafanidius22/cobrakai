from sqlite3.dbapi2 import Cursor, connect
from PyQt5 import  uic,QtWidgets,QtGui
import sqlite3
from sqlite3 import Error
from datetime import datetime
def getRow(Nom):
    cursor.execute("SELECT Nome FROM usuarios ORDER BY Nome")
    Nomes = cursor.fetchall()
    for x in range(len(Nomes)):
            Nome = ''.join(Nomes[x])
            if Nom < Nome:
                    return x - 1
    return len(Nomes) - 1

def Cadastrar():
    Ajust = Menu.Nome_Line.text().split()
    Nome = ""
    for x in Ajust:
        Nome += x.capitalize() + " "
    CPF=Menu.CPF1_Line.text()+"/"+Menu.CPF2_Line.text()
    Endereço=Menu.Endereco_Line.text()
    Telefone= Menu.Tel_Line.text()
    email=Menu.Email_Line.text()
    login=Menu.Cod_Line.text()
    senha=Menu.Senha_Line.text()
    try:
                cursor.execute("INSERT INTO usuarios VALUES ('"+Nome+"','"+CPF+"','"+Endereço+"','"+Telefone+"','"+email+"','"+login+"','"+senha+"')")
                banco.commit()
                LoadTable(QtWidgets.QTableWidgetItem(login), QtWidgets.QTableWidgetItem(Nome), getRow(Nome))
                print("aluno cadastrado: " + Nome)
    except sqlite3.Error as erro:
                print("cadastro deu erro: ",erro)
                print("Cadastro:")
                print("Nome: "+ Menu.Nome_Line.text())
                print("CPF:"+Menu.CPF1_Line.text()+"/"+Menu.CPF2_Line.text())
                print("Endereco:" + Menu.Endereco_Line.text())
                print("e-Mail:"+ Menu.Email_Line.text())
                print("Telefone:"+ Menu.Tel_Line.text())
                print("Login:"+ Menu.Cod_Line.text())
                print("Senha:" + Menu.Senha_Line.text())
                print("por "+Menu.Aulas_Box.currentText())
                print("Mensalidade:" + Menu.Mensalidade.text())
                if erro is " UNIQUE constraint failed: usuarios.Login":
                    print (erro)
                    Menu.Mensagem.setText("Falha: Login em uso")
    Cadastro_ClearLines()

def LoadTable(Log, Nom, newRow):

    Menu.tableWidget.insertRow(newRow)
    Menu.tableWidget.setItem(newRow, 0, Log)
    Menu.tableWidget.setItem(newRow, 1, Nom)

def Load_DB():
    banco=sqlite3.connect('listaacademia.db')
    cursor = banco.cursor()
    cursor.execute("SELECT Nome FROM usuarios ORDER BY Nome")
    Nomes = cursor.fetchall()
    print(Nomes)
    cursor.execute("SELECT Login FROM usuarios ORDER BY Nome")
    Logins = cursor.fetchall()
    print(Logins)
    for x in range(len(Nomes)):
        Nome = ''.join(Nomes[x])
        Login = ''.join(Logins[x])
        LoadTable(QtWidgets.QTableWidgetItem(Login), QtWidgets.QTableWidgetItem(Nome), x)

def Dia_Update():
    Index = Menu.Aulas_Box.currentIndex()
    print(Index)
    if Index == 0:
        Menu.Mensalidade.setText(" ")
    elif Index == 1:
        Menu.Mensalidade.setText("R$ 100,00")
    elif Index == 2:
        Menu.Mensalidade.setText("R$ 170,00")
    elif Index == 3:
        Menu.Mensalidade.setText("R$ 200,00")
    elif Index == 4:
        Menu.Mensalidade.setText("R$ 250,00")

def Edit_LockLines(I):                      #0 = lock   1 = unluck
    if I == 0:
        Menu.Nome_Line_2.setEnabled(False)
        Menu.CPF1_Line_2.setEnabled(False)
        Menu.CPF2_Line_2.setEnabled(False)
        Menu.Endereco_Line_2.setEnabled(False)
        Menu.Email_Line_2.setEnabled(False)
        Menu.Tel_Line_2.setEnabled(False)
        Menu.Cod_Line_2.setEnabled(False)
        Menu.Senha_Line_2.setEnabled(False)
        Menu.Aulas_Box_2.setEnabled(False)
    if I == 1:
        Menu.Nome_Line_2.setEnabled(True)
        Menu.CPF1_Line_2.setEnabled(True)
        Menu.CPF2_Line_2.setEnabled(True)
        Menu.Endereco_Line_2.setEnabled(True)
        Menu.Email_Line_2.setEnabled(True)
        Menu.Tel_Line_2.setEnabled(True)
        Menu.Cod_Line_2.setEnabled(True)
        Menu.Senha_Line_2.setEnabled(True)
        Menu.Aulas_Box_2.setEnabled(True)

def Cadastro_ClearLines():
    print("Limpar")
    Menu.Nome_Line.clear()
    Menu.CPF1_Line.clear()
    Menu.CPF2_Line.clear()
    Menu.Endereco_Line.clear()
    Menu.Email_Line.clear()
    Menu.Tel_Line.clear()
    Menu.Cod_Line.clear()
    Menu.Senha_Line.clear()
    Menu.Aulas_Box.setCurrentIndex(0)

def Edit_Text(Aluno):

    cursor.execute("SELECT Nome, CPF, Endereço, email,Telefone,Login,Senha FROM usuarios WHERE Login = "+Aluno+"")
    info = cursor.fetchall()
    Menu.Nome_Line_2.setText(info[0][0])
    CPF = info[0][1].split("/",2)
    Menu.CPF1_Line_2.setText(CPF[0])
    Menu.CPF2_Line_2.setText(CPF[1])
    Menu.Endereco_Line_2.setText(''.join(info[0][2]))
    Menu.Email_Line_2.setText(''.join(info[0][3]))
    Menu.Tel_Line_2.setText(''.join(info[0][4]))
    Menu.Cod_Line_2.setText(''.join(info[0][5]))
    Menu.Senha_Line_2.setText(''.join(info[0][6]))
    #Menu.Aulas_Box_2.setCurrentIndex(0)

def Aluno_Edit():

    Login = Menu.tableWidget.item(Menu.tableWidget.currentRow(), 0).text()
    print (Login)
    cursor.execute("SELECT Login FROM usuarios")
    Logins = cursor.fetchall()
    for x in Logins:
        check = ''.join(x)
        if Login == check:
            Edit_Text(Login)
            setPage(4)
            break

def Procurar_Aluno():
    Menu.tableWidget.setRowCount(0)
    procura = Menu.lineEdit_Procurar.text()
    if procura.isnumeric():
        cursor.execute("SELECT Login, Nome FROM usuarios WHERE Login LIKE'{}%' ORDER BY Nome".format(procura))
        results = cursor.fetchall()
        print(results)
    else:
        cursor.execute("SELECT Login, Nome FROM usuarios WHERE Nome LIKE '%{}%' or Nome LIKE '{}%' ORDER BY Nome".format(" " + procura,procura))
        results = cursor.fetchall()
        print(results)
    for x in range(len(results)):
        Nome = ''.join(results[x][1])
        Login = ''.join(results[x][0])
        LoadTable(QtWidgets.QTableWidgetItem(Login), QtWidgets.QTableWidgetItem(Nome), x)

def Complete_Edit():
    Login = Menu.tableWidget.item(Menu.tableWidget.currentRow(), 0).text()
    Ajust = Menu.Nome_Line_2.text().split()
    Nome = ""
    for x in Ajust:
        Nome += x.capitalize() + " "
    CPF = Menu.CPF1_Line_2.text() + "/" + Menu.CPF2_Line_2.text()
    Endereço = Menu.Endereco_Line_2.text()
    Telefone = Menu.Tel_Line_2.text()
    email = Menu.Email_Line_2.text()
    login = Menu.Cod_Line_2.text()
    senha = Menu.Senha_Line_2.text()
    try:
        cursor.execute("UPDATE usuarios SET Nome = '"+Nome+"', CPF = '"+CPF+"', Endereço = '"+Endereço+"', email = '"+email+"',Telefone = '"+Telefone+"',Login = '"+login+"',Senha = '"+senha+"' WHERE Login = "+Login+"")
        banco.commit()
        Menu.tableWidget.removeRow(Menu.tableWidget.currentRow())
        LoadTable(QtWidgets.QTableWidgetItem(login), QtWidgets.QTableWidgetItem(Nome), getRow(Nome))
    except sqlite3.Error as erro:
        print("Edição não permitida, erro: ", erro)
        Edit_Text(Menu.tableWidget.item(Menu.tableWidget.currentRow(), 0).text())
    Edit_LockLines(0)

def RemoverAluno():
    Login = Menu.tableWidget.item(Menu.tableWidget.currentRow(), 0).text()
    cursor.execute("DELETE from usuarios WHERE login = "+Login+"")
    banco.commit()
    print("Aluno "+ Login +" removido")
    Menu.tableWidget.removeRow(Menu.tableWidget.currentRow())
    setPage(1)

def Quit():
    print("Saindo")
    banco.close()
    sys.exit(0)

def setPage(I):
    Menu.stackedWidget.setCurrentIndex(I)

def PageChange():
    page = Menu.stackedWidget.currentIndex()
    if page == 3:
        Cadastro_ClearLines()
    elif page == 4:
        Edit_LockLines(0);

def Pagamento(Aluno):
    return True

def CatracaSim():
    login = Catraca.lineEdit.text()
    senha = Catraca.lineEdit_2.text()
    hora = datetime.now()
    hora_string = hora.strftime("%d/%m/%Y %H:%M:%S")
    if login != "":
        cursor.execute("SELECT Senha, COUNT(*) FROM usuarios WHERE Login = "+login+"")
        info = cursor.fetchall()
        if info[0][1] == 1:
            sen = "".join(info[0][0])
            if senha == sen:
                cursor.execute("SELECT Login, Nome FROM usuarios WHERE Senha = " +sen+ "")
                info = cursor.fetchall()
                Login = "".join(info[0][0])
                Nome = "".join(info[0][1])
                if Pagamento(Login) == True:
                    entry = Login + "\t" + Nome + "\t\t\tPERMITIDA\t\t" + hora_string
                    Menu.listEntrada.addItem(entry)
                    print("entrada permitida")
                elif Pagamento (Login) == False:
                    entry = Login + "\t" + Nome + "\t\t\tNEGADA, PAGAMENTO ATRASADO\t\t" + hora_string
                    Menu.listEntrada.addItem(entry)
                    print("entrada negada")
                Catraca.lineEdit.clear()
                Catraca.lineEdit_2.clear()
                return 0
    Menu.listEntrada.addItem("N/A\tDESCONHECIDO\t\tNEGADA, LOGIN/SENHA ERRADO(S)\t\t" + hora_string)
    print("entrada negada")
    Catraca.lineEdit.clear()
    Catraca.lineEdit_2.clear()

app=QtWidgets.QApplication([])
Menu=uic.loadUi("CobraKai.ui")
Catraca=uic.loadUi("Catraca.ui")
Menu.Logo.setPixmap(QtGui.QPixmap('Logo.png'))
setPage(0)
banco=sqlite3.connect('listaacademia.db')
cursor= banco.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS usuarios (Nome text NOT NULL,CPF text NOT NULL,Endereço text,Telefone text,email text,Login text NOT NULL PRIMARY KEY,Senha text NOT NULL)")
banco.commit()
Menu.tableWidget.setColumnCount(2)
Menu.tableWidget.setColumnWidth(0, 100);
Menu.tableWidget.setColumnWidth(1, 600);
Load_DB()
Menu.Nome_Line.setMaxLength(40)
Menu.CPF1_Line.setValidator(QtGui.QIntValidator())
Menu.CPF1_Line.setMaxLength(9)
Menu.CPF2_Line.setValidator(QtGui.QIntValidator())
Menu.CPF2_Line.setMaxLength(2)
Menu.Endereco_Line.setMaxLength(50)
Menu.Email_Line.setMaxLength(40)
Menu.Tel_Line.setValidator(QtGui.QIntValidator())
Menu.Tel_Line.setMaxLength(15)
Menu.Cod_Line.setValidator(QtGui.QIntValidator())
Menu.Cod_Line.setMaxLength(6)
Menu.Senha_Line.setMaxLength(10)
Menu.Senha_Line.setValidator(QtGui.QIntValidator())
Menu.Nome_Line_2.setMaxLength(40)
Menu.CPF1_Line_2.setValidator(QtGui.QIntValidator())
Menu.CPF1_Line_2.setMaxLength(9)
Menu.CPF2_Line_2.setValidator(QtGui.QIntValidator())
Menu.CPF2_Line_2.setMaxLength(2)
Menu.Endereco_Line_2.setMaxLength(50)
Menu.Email_Line_2.setMaxLength(40)
Menu.Tel_Line_2.setValidator(QtGui.QIntValidator())
Menu.Tel_Line_2.setMaxLength(15)
Menu.Cod_Line_2.setValidator(QtGui.QIntValidator())
Menu.Cod_Line_2.setMaxLength(6)
Menu.Senha_Line_2.setMaxLength(10)
Menu.Senha_Line_2.setValidator(QtGui.QIntValidator())

Menu.Botao_Voltar.clicked.connect(lambda: setPage(0))
Menu.Botao_Voltar_2.clicked.connect(lambda: setPage(0))
Menu.Botao_Voltar_3.clicked.connect(lambda: setPage(0))
Menu.Botao_Voltar_3.clicked.connect(Cadastro_ClearLines)

Menu.Botao_Editar.clicked.connect(lambda: setPage(1))
Menu.Botao_Editar_2.clicked.connect(lambda: setPage(1))
Menu.Botao_Editar_3.clicked.connect(lambda: setPage(1))
Menu.Botao_Editar_3.clicked.connect(Cadastro_ClearLines)
Menu.Botao_Voltar_4.clicked.connect(lambda: setPage(1))

Menu.Botao_Relacao.clicked.connect(lambda: setPage(2))
Menu.Botao_Relacao_2.clicked.connect(lambda: setPage(2))
Menu.Botao_Relacao_3.clicked.connect(lambda: setPage(2))
Menu.Botao_Relacao_4.clicked.connect(lambda: setPage(2))
Menu.Botao_Relacao_4.clicked.connect(Cadastro_ClearLines)

Menu.Botao_Cadastro.clicked.connect(lambda: setPage(3))
Menu.Botao_Cadastro_2.clicked.connect(lambda: setPage(3))
Menu.Botao_Cadastro_3.clicked.connect(lambda: setPage(3))
Menu.Botao_Cadastro_4.clicked.connect(lambda: setPage(3))

Menu.Botao_Procurar.clicked.connect(Procurar_Aluno)
Menu.Botao_Cadastrar.clicked.connect(Cadastrar)
Menu.Botao_Limpar.clicked.connect(Cadastro_ClearLines)
Menu.Botao_Edit.clicked.connect(lambda: Edit_LockLines(1))
Menu.Botao_Desfazer.clicked.connect(lambda: Edit_Text(Menu.tableWidget.item(Menu.tableWidget.currentRow(), 0).text()))
Menu.Botao_Remover.clicked.connect(RemoverAluno)
Menu.Botao_Alterar.clicked.connect(Complete_Edit)
Menu.stackedWidget.currentChanged.connect(PageChange)
Menu.Aulas_Box.currentIndexChanged.connect(Dia_Update)

Menu.tableWidget.itemDoubleClicked.connect(Aluno_Edit)

Menu.Botao_Sair.clicked.connect(Quit)


Catraca.lineEdit.setValidator(QtGui.QIntValidator())
Catraca.lineEdit.setMaxLength(6)
Catraca.lineEdit_2.setMaxLength(10)
Catraca.lineEdit_2.setValidator(QtGui.QIntValidator())
Catraca.pushButton_Entrar.clicked.connect(CatracaSim)


Menu.show()
Catraca.show()
app.exec()