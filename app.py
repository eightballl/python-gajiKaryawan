import mariadb,datetime,calendar
from flask import Flask, request
from datetime import datetime as dtm

app = Flask(__name__)
# MARIADB MYSQL
app.config['DEBUG'] = True
conn = mariadb.connect(
    user = 'root',
    password = '',
    host = '127.0.0.1',
    port = 3306,
    database = 'python_uas'
    )
dbMysql = conn.cursor()

# LOGIN
hasil = ''
sudahLoginAdmin = False
sudahLoginKeuangan = False
sudahLoginPimpinan = False
@app.route('/login', methods=['POST'])
def login():
    user_admin = '0000000000'
    pass_admin ='0000000000'
    nama_admin = '0000000000'
    user_kgn = '0000000000'
    pass_kgn = '0000000000'
    nama_kgn = '0000000000'
    user_pmp = '0000000000'
    pass_pmp = '0000000000'
    pass_pmp = '0000000000'
    username=request.form['username'].lower()
    password=request.form['password'].lower()
    dbMysql.execute(f'select * from admin a, keuangan b, pimpinan c where a.username_admin = "{username}" and a.password_admin = "{password}" or b.username_keuangan = "{username}" and b.password_keuangan = "{password}" or c.user_pimpinan = "{username}" and c.pass_pimpinan = "{password}"  ')
    admin = dbMysql.fetchall()
    for row in admin:
        nama_admin = row[1]
        user_admin = row[2]
        pass_admin = row[3]
        nama_kgn = row[5]
        user_kgn = row[6]
        pass_kgn = row[7]
        nama_pmp = row[9]
        user_pmp = row[10]
        pass_pmp = row[11]
    if username==user_admin.lower() and password==pass_admin.lower():
        global sudahLoginAdmin,hasil
        sudahLoginAdmin = True
        hasil = f'Welcome {nama_admin}\nAnda sebagai Admin'
    elif username==user_kgn.lower() and password==pass_kgn.lower():
        global sudahLoginKeuangan
        sudahLoginKeuangan = True
        hasil = f'Welcome {nama_kgn}\nAnda sebagai Pegawai Keuangan'
    elif username==user_pmp.lower() and password==pass_pmp.lower():
        global sudahLoginPimpinan
        sudahLoginPimpinan = True
        hasil = f'Welcome {nama_pmp}\nAnda sebagai Pegawai Pimpinan'
    elif username == '' or password == '':
        hasil = 'Silahkan Inputkan'
    elif username == '' and password == '':
        hasil = 'Silahkan Inputkan'
    else:
        hasil = 'Username atau password salah'
    return hasil
# LOGOUT
@app.route('/logout/<username>')
def logout(username):
    if username == 'admin':
        global sudahLoginAdmin
        sudahLoginAdmin = False
        return f'Bye {username}'
    elif username == 'keuangan':
        global sudahLoginKeuangan
        sudahLoginKeuangan = False
        return f'Bye {username}'
    elif username == 'pimpinan':
        global sudahLoginPimpinan
        sudahLoginPimpinan = False
        return f'Bye {username}'

# ADMIN
@app.route('/admin/add', methods = ['POST'])
def addPegawai():
    global sudahLoginAdmin
    if sudahLoginAdmin == False:
        return f'Silahkan login sebagai Admin!'

    nama = request.form['nama_pegawai']
    JenisKelamin = request.form['jenis_kelamin']
    alamat = request.form['alamat']
    no_hp = request.form['no_hp']
    divisi = request.form['id_divisi']

    try:
        dbMysql.execute('INSERT INTO tb_pegawai (id_divisi, nama_pegawai, jenis_kelamin, alamat, no_hp) VALUES (?, ?, ?, ?, ?)', (divisi, nama, JenisKelamin, alamat, no_hp))
    except mariadb.Error as e:
        print(f'Error {e}')

    conn.commit()
    return f'{nama} TELAH BERHASIL DI INPUT' 

@app.route('/admin/data', methods = ['GET'])
def dataPegawai():
    global sudahLoginAdmin
    if sudahLoginAdmin == False:
        return f'Silahkan login sebagai Admin!'

    dbMysql.execute('select * from tb_pegawai')
    row_headers = [x[0] for x in dbMysql.description]
    listData = dbMysql.fetchall()
    json_data = []
    for result in listData:
        json_data.append(dict(zip(row_headers, result)))

    return{'Data Pegawai':json_data}

@app.route('/admin/update/', methods = ['PUT'])
def updatePegawai():
    global sudahLoginAdmin
    if sudahLoginAdmin == False:
        return f'Silahkan login sebagai Admin!'

    id_pegawai = request.form['id_pegawai']
    alamat = request.form['alamat']
    no_hp = request.form['no_hp']
    divisi = request.form['id_divisi']

    try:
        dbMysql.execute(f"UPDATE tb_pegawai set id_divisi=?, alamat=?, no_hp=? where id_pegawai='{id_pegawai}'",(divisi, alamat, no_hp))
        if dbMysql.rowcount == 0:
            return 'ID TIDAK DITEMUKAN'
    except mariadb.Error as e:
        print(f'Error {e}')
    
    conn.commit()
    return f'PEGAWAI DENGAN ID {id_pegawai} TELAH BERHASIL DIUPDATE'

@app.route('/admin/delete', methods = ['DELETE'])
def deletePegawai():
    global sudahLoginAdmin
    if sudahLoginAdmin == False:
        return f'Silahkan login sebagai Admin!'

    id_pegawai = request.form['id_pegawai']
    try:
        dbMysql.execute(f"DELETE FROM tb_pegawai where id_pegawai='{id_pegawai}'")
        if dbMysql.rowcount == 0:
            return 'ID TIDAK DITEMUKAN'
    except mariadb.Error as e:
        print(f'Error {e}')
    
    conn.commit()
    return f'PEGAWAI DENGAN ID = {id_pegawai} TELAH BERHASIL DIHAPUS'

@app.route('/admin/divisi', methods = ['GET'])
def dataDivisi():
    global sudahLoginAdmin
    if sudahLoginAdmin == False:
        return f'Silahkan login sebagai Admin!'

    dbMysql.execute('select * from tb_divisi')
    row_headers = [x[0] for x in dbMysql.description]
    listData = dbMysql.fetchall()
    json_data = []
    for result in listData:
        json_data.append(dict(zip(row_headers, result)))

    return{'Divisi':json_data}

@app.route('/admin/add/divisi', methods = ['POST'])
def addDivisi():
    global sudahLoginAdmin
    if sudahLoginAdmin == False:
        return f'Silahkan login sebagai Admin!'

    id = request.form['id_divisi']
    divisi = request.form['divisi']
    gaji = request.form['gaji']

    try:
        dbMysql.execute('INSERT INTO tb_divisi (id_divisi, divisi, gaji) VALUES (?, ?, ?)', (id, divisi, gaji))
    except mariadb.Error as e:
        print(f'Error {e}')

    conn.commit()
    return f'DIVISI DENGAN ID = {id} TELAH BERHASIL DIINPUT'

@app.route('/admin/update/divisi', methods = ['PUT'])
def updateDivisi():
    global sudahLoginAdmin
    if sudahLoginAdmin == False:
        return f'Silahkan login sebagai Admin!'
    id = request.form['id_divisi']
    divisi = request.form['divisi']
    gaji = request.form['gaji']

    try:
        dbMysql.execute(f"UPDATE tb_divisi set divisi=?, gaji=? where id_divisi='{id}'",(divisi, gaji))
        if dbMysql.rowcount == 0:
            return 'ID DIVISI TIDAK DITEMUKAN'
    except mariadb.Error as e:
        print(f'Error {e}')
    
    conn.commit()
    return f'{id} TELAH DI UPDATE'

@app.route('/admin/delete/divisi', methods = ['DELETE'])
def deleteDivisi():
    global sudahLoginAdmin
    if sudahLoginAdmin == False:
        return f'Silahkan login sebagai Admin!'

    id = request.form['id_divisi']
    try:
        dbMysql.execute(f"DELETE FROM tb_divisi where id_divisi='{id}'")
        if dbMysql.rowcount == 0:
            return 'ID DIVISI TIDAK DITEMUKAN'
    except mariadb.Error as e:
        print(f'Error {e}')
    
    conn.commit()
    return f'{id} TELAH BERHASIL DIHAPUS'

# KEUANGAN
@app.route('/keuangan/datapegawai', methods = ['GET'])
def dataPegawai1():
    global sudahLoginKeuangan
    if sudahLoginKeuangan == False:
        return f'Silahkan login sebagai Keuangan!'

    dbMysql.execute('select * from tb_pegawai')
    row_headers = [x[0] for x in dbMysql.description]
    listData = dbMysql.fetchall()
    json_data = []
    for result in listData:
        json_data.append(dict(zip(row_headers, result)))

    return{'Data Pegawai':json_data}

@app.route('/keuangan/gaji', methods = ['POST'])
def gajiLembur():
    global sudahLoginKeuangan
    if sudahLoginKeuangan == False:
        return f'Silahkan login sebagai Keuangan!'

    id_pegawai = request.form['id_pegawai']
    lembur = request.form['lembur']
    hari = request.form['hari']
    bulan = request.form['bulan']
    tanggal = datetime.datetime.now()
    tanggalFormat = f'{hari}-{bulan}-{tanggal.strftime("%Y")}'
    hasil2 = ''
    bulanTampil = int(bulan)
    bulanHitung = int(bulan)
    def nama_bulan(bulanTampil): 
        switcher = { 
            1: "Januari", 
            2: "Februari", 
            3: "Maret", 
            4: "April",
            5: "Mei",
            6: "Juni",
            7: "Juli",
            8: "Agustus",
            9: "September",
            10: "Oktober",
            11: "November",
            12: "Desember",
        } 
        return switcher.get(bulanTampil, "Bukan nomor bulan yang benar")
    if __name__ == "__main__":
        hasil2 += nama_bulan(bulanTampil)
    hitungHari = calendar.monthrange(int(tanggal.strftime("%Y")),bulanHitung)[1]

    if int(hari) > hitungHari:
        return f'Tanggal yang anda inputkan melebihi jumlah hari dibulan {bulan}({nama_bulan(bulanTampil)})!'

    tanggalInput= dtm.strptime(tanggalFormat,"%d-%m-%Y")
    
    

    
    dbMysql.execute(f"select nama_pegawai,divisi,gaji from (select * from tb_pegawai where id_pegawai = '{id_pegawai}') a left join tb_divisi on a.id_divisi=tb_divisi.id_divisi")
    data = dbMysql.fetchall()
    for row in data:
        gaji = row[2]
    
    
    if int(lembur) == 0:
        gaji_lembur = 0
    elif int(lembur) > 0 and int(lembur) < 16:
        gaji_lembur = 75000
    elif int(lembur) > 15:
        gaji_lembur = 150000

    gajiInput = int(gaji)
    total = gajiInput + gaji_lembur
   

    try:
        dbMysql.execute('INSERT INTO tb_gaji (id_pegawai, gaji, lembur, gaji_lembur,total_gaji,tanggal) VALUES (?, ?, ?, ?, ?,?)', (id_pegawai, gaji, lembur, gaji_lembur, total,tanggalInput))
    except mariadb.Error as e:
        print(f'Error {e}')

    conn.commit()
    return f'Tanggal Gajian = {tanggalFormat}\nID_Pegawai  = {id_pegawai}\nGaji        = {gaji}\nLembur/jam  = {lembur}\nGaji Lembur = {gaji_lembur}\nTotal Gaji  = {total}'

    
@app.route('/keuangan/updategaji/', methods = ['PUT'])
def updateGaji():
    global sudahLoginKeuangan
    if sudahLoginKeuangan == False:
        return f'Silahkan login sebagai Keuangan!'

    id_pegawai = request.form['id_pegawai']
    lembur = request.form['lembur']
    dbMysql.execute(f"select nama_pegawai,divisi,gaji from (select * from tb_pegawai where id_pegawai = '{id_pegawai}') a left join tb_divisi on a.id_divisi=tb_divisi.id_divisi")
    data = dbMysql.fetchall()
    for row in data:
        gaji = row[2]
    if int(lembur) == 0:
        gaji_lembur = 0
    elif int(lembur) > 0 and int(lembur) < 16:
        gaji_lembur = 75000
    elif int(lembur) > 15:
        gaji_lembur = 150000
    
    total = int(gaji) + gaji_lembur

    try:
        dbMysql.execute(f"UPDATE tb_gaji set gaji=?, lembur=?, gaji_lembur=?, total_gaji=? where id_pegawai = '{id_pegawai}' order by tanggal desc limit 1",(gaji, lembur, gaji_lembur, total))
        if dbMysql.rowcount == 0:
            return 'ID PEGAWAI TIDAK DITEMUKAN'
    except mariadb.Error as e:
        print(f'Error {e}')
    
    conn.commit()
    return f'ID_Pegawai  = {id_pegawai}\nGaji        = {gaji}\nLembur/jam  = {lembur}\nGaji Lembur = {gaji_lembur}\nTotal Gaji  = {total}'

@app.route('/keuangan/deletegaji', methods = ['DELETE'])
def deleteGaji():
    global sudahLoginKeuangan
    if sudahLoginKeuangan == False:
        return f'Silahkan login sebagai Keuangan!'

    id_pegawai = request.form['id_pegawai']
    try:
        dbMysql.execute(f"DELETE FROM tb_gaji where id_pegawai='{id_pegawai}'")
        if dbMysql.rowcount == 0:
            return "ID TIDAK DITEMUKAN"
    except mariadb.Error as e:
        print(f'Error {e}')
    
    conn.commit()
    return 'success'

@app.route('/keuangan/datagaji', methods = ['GET'])
def dataGaji():
    global sudahLoginKeuangan
    if sudahLoginKeuangan == False:
        return f'Silahkan login sebagai Keuangan!'

    dbMysql.execute('select * from tb_gaji')
    row_headers = [x[0] for x in dbMysql.description]
    listData = dbMysql.fetchall()
    json_data = []
    for result in listData:
        json_data.append(dict(zip(row_headers, result)))

    return{'Data Gaji Pegawai':json_data}

@app.route('/keuangan/rekaplaporan', methods = ['GET'])
def rekapLaporan():
    global sudahLoginKeuangan
    if sudahLoginKeuangan == False:
        return f'Silahkan login sebagai Keuangan!'

    dbMysql.execute('select * from tb_pegawai LEFT JOIN tb_gaji on tb_pegawai.id_pegawai=tb_gaji.id_pegawai')
    row_headers = [x[0] for x in dbMysql.description]
    listData = dbMysql.fetchall()
    json_data = []
    for result in listData:
        json_data.append(dict(zip(row_headers, result)))

    return{'Rekap Laporan':json_data}

# PIMPINAN
@app.route('/pimpinan/laporan', methods = ['GET'])
def dataPimpinan():
    global sudahLoginPimpinan
    if sudahLoginPimpinan == False:
        return f'Silahkan login sebagai Pimpinan!'

    dbMysql.execute('select * from tb_pegawai LEFT JOIN tb_gaji on tb_pegawai.id_pegawai=tb_gaji.id_pegawai')
    row_headers = [x[0] for x in dbMysql.description]
    listData = dbMysql.fetchall()
    json_data = []
    for result in listData:
        json_data.append(dict(zip(row_headers, result)))

    return{'Laporan Data Pegawai':json_data}

# PEGAWAI
@app.route('/pegawai/cekGaji', methods = ['get'])
def cekGaji():

    id_pegawai = request.form['id_pegawai']
    dbMysql.execute(f"select gaji,lembur,gaji_lembur,total_gaji,tanggal as tanggal_gajian from tb_gaji where id_pegawai = '{id_pegawai}' order by tanggal desc limit 1")
    row_headers = [x[0] for x in dbMysql.description]
    listData = dbMysql.fetchall()
    json_data = []
    for result in listData:
        json_data.append(dict(zip(row_headers, result)))
    
    return{'Gaji Anda':json_data}

# DUMPPP

# from flask import Flask, request
# import mariadb
# app = Flask(__name__)

# # MARIADB MYSQL
# app.config['DEBUG'] = True
# conn = mariadb.connect(
#     user = 'root',
#     password = '',
#     host = '127.0.0.1',
#     port = 3306,
#     database = 'python_uas'
#     )
# dbMysql = conn.cursor()

# # LOGIN
# hasil = ''
# sudahLoginAdmin = False
# sudahLoginKeuangan = False
# sudahLoginPimpinan = False
# @app.route('/login', methods=['POST'])
# def login():
#     user_admin = '0000000000'
#     pass_admin ='0000000000'
#     nama_admin = '0000000000'
#     user_kgn = '0000000000'
#     pass_kgn = '0000000000'
#     nama_kgn = '0000000000'
#     user_pmp = '0000000000'
#     pass_pmp = '0000000000'
#     pass_pmp = '0000000000'
#     username=request.form['username'].lower()
#     password=request.form['password'].lower()
#     dbMysql.execute(f'select * from admin a inner join keuangan b inner join pimpinan c on a.username_admin = "{username}" and a.password_admin = "{password}" or b.username_keuangan = "{username}" and b.password_keuangan = "{password}" or c.user_pimpinan = "{username}" and c.pass_pimpinan = "{password}"  ')
#     admin = dbMysql.fetchall()
#     tampil = []
#     for row in admin:
#         nama_admin = row[4]
#         user_admin = row[1]
#         pass_admin = row[2]
#         nama_kgn = row[5]
#         user_kgn = row[6]
#         pass_kgn = row[7]
#         nama_pmp = row[9]
#         user_pmp = row[10]
#         pass_pmp = row[11]
#     # if username==user_admin.lower() and password==pass_admin.lower():
#     #     global sudahLoginAdmin,hasil
#     #     sudahLoginAdmin = True
#     #     hasil = f'Welcome {nama_admin}\nAnda sebagai Admin'
#     # elif username==user_kgn.lower() and password==pass_kgn.lower():
#     #     global sudahLoginKeuangan
#     #     sudahLoginKeuangan = True
#     #     hasil = f'Welcome {nama_kgn}\nAnda sebagai Pegawai Keuangan'
#     # elif username==user_pmp.lower() and password==pass_pmp.lower():
#     #     global sudahLoginPimpinan
#     #     sudahLoginPimpinan = True
#     #     hasil = f'Welcome {nama_pmp}\nAnda sebagai Pegawai Pimpinan'
#     # elif username == '' or password == '':
#     #     hasil = 'Silahkan Inputkan'
#     # elif username == '' and password == '':
#     #     hasil = 'Silahkan Inputkan'
#     # else:
#     #     hasil = 'Password Anda Salah'
#     return f'{nama_admin + user_admin + pass_admin + nama_kgn+user_kgn+pass_kgn+nama_pmp+user_pmp+pass_pmp}'

# # LOGOUT
# @app.route('/logout/<username>')
# def logout(username):
#     if username == 'admin':
#         global sudahLoginAdmin
#         sudahLoginAdmin = False
#         return f'Bye {username}'
#     elif username == 'keuangan':
#         global sudahLoginKeuangan
#         sudahLoginKeuangan = False
#         return f'Bye {username}'
#     elif username == 'pimpinan':
#         global sudahLoginPimpinan
#         sudahLoginPimpinan = False
#         return f'Bye {username}'

# # ADMIN
# @app.route('/admin/add', methods = ['POST'])
# def addPegawai():
#     global sudahLoginAdmin
#     if sudahLoginAdmin == False:
#         return f'Silahkan login sebagai Admin!'

#     nama = request.form['nama_pegawai']
#     JenisKelamin = request.form['jenis_kelamin']
#     alamat = request.form['alamat']
#     no_hp = request.form['no_hp']
#     divisi = request.form['id_divisi']

#     try:
#         dbMysql.execute('INSERT INTO tb_pegawai (id_divisi, nama_pegawai, jenis_kelamin, alamat, no_hp) VALUES (?, ?, ?, ?, ?)', (divisi, nama, JenisKelamin, alamat, no_hp))
#     except mariadb.Error as e:
#         print(f'Error {e}')

#     conn.commit()
#     return 'success' 

# @app.route('/admin/data', methods = ['GET'])
# def dataPegawai():
#     global sudahLoginAdmin
#     if sudahLoginAdmin == False:
#         return f'Silahkan login sebagai Admin!'

#     dbMysql.execute('select * from tb_pegawai')
#     row_headers = [x[0] for x in dbMysql.description]
#     listData = dbMysql.fetchall()
#     json_data = []
#     for result in listData:
#         json_data.append(dict(zip(row_headers, result)))

#     return{'Data Pegawai':json_data}

# @app.route('/admin/update/', methods = ['PUT'])
# def updatePegawai():
#     global sudahLoginAdmin
#     if sudahLoginAdmin == False:
#         return f'Silahkan login sebagai Admin!'

#     id_pegawai = request.form['id_pegawai']
#     alamat = request.form['alamat']
#     no_hp = request.form['no_hp']
#     divisi = request.form['id_divisi']

#     try:
#         dbMysql.execute(f'UPDATE tb_pegawai set id_divisi=?, alamat=?, no_hp=? where id_pegawai=?',(divisi, alamat, no_hp, id_pegawai))
#     except mariadb.Error as e:
#         print(f'Error {e}')
    
#     conn.commit()
#     return 'success'

# @app.route('/admin/delete', methods = ['DELETE'])
# def deletePegawai():
#     global sudahLoginAdmin
#     if sudahLoginAdmin == False:
#         return f'Silahkan login sebagai Admin!'

#     id_pegawai = request.form['id_pegawai']
#     try:
#         dbMysql.execute(f"DELETE FROM tb_pegawai where id_pegawai='{id_pegawai}'")
#     except mariadb.Error as e:
#         print(f'Error {e}')
    
#     conn.commit()
#     return 'success'

# @app.route('/admin/divisi', methods = ['GET'])
# def dataDivisi():
#     global sudahLoginAdmin
#     if sudahLoginAdmin == False:
#         return f'Silahkan login sebagai Admin!'

#     dbMysql.execute('select * from tb_divisi')
#     row_headers = [x[0] for x in dbMysql.description]
#     listData = dbMysql.fetchall()
#     json_data = []
#     for result in listData:
#         json_data.append(dict(zip(row_headers, result)))

#     return{'Divisi':json_data}

# @app.route('/admin/add/divisi', methods = ['POST'])
# def addDivisi():
#     global sudahLoginAdmin
#     if sudahLoginAdmin == False:
#         return f'Silahkan login sebagai Admin!'

#     id = request.form['id_divisi']
#     divisi = request.form['divisi']
#     gaji = request.form['gaji']

#     try:
#         dbMysql.execute('INSERT INTO tb_divisi (id_divisi, divisi, gaji) VALUES (?, ?, ?)', (id, divisi, gaji))
#     except mariadb.Error as e:
#         print(f'Error {e}')

#     conn.commit()
#     return 'success'

# @app.route('/admin/update/divisi', methods = ['PUT'])
# def updateDivisi():
#     global sudahLoginAdmin
#     if sudahLoginAdmin == False:
#         return f'Silahkan login sebagai Admin!'
#     id = request.form['id_divisi']
#     divisi = request.form['divisi']
#     gaji = request.form['gaji']

#     try:
#         dbMysql.execute(f'UPDATE tb_divisi set divisi=?, gaji=? where id_divisi=?',(divisi, gaji, id))
#     except mariadb.Error as e:
#         print(f'Error {e}')
    
#     conn.commit()
#     return 'success'

# @app.route('/admin/delete/divisi', methods = ['DELETE'])
# def deleteDivisi():
#     global sudahLoginAdmin
#     if sudahLoginAdmin == False:
#         return f'Silahkan login sebagai Admin!'

#     id = request.form['id_divisi']
#     try:
#         dbMysql.execute(f"DELETE FROM tb_divisi where id_divisi='{id}'")
#     except mariadb.Error as e:
#         print(f'Error {e}')
    
#     conn.commit()
#     return 'success'

# # KEUANGAN
# @app.route('/keuangan/datapegawai', methods = ['GET'])
# def dataPegawai1():
#     global sudahLoginKeuangan
#     if sudahLoginKeuangan == False:
#         return f'Silahkan login sebagai Keuangan!'

#     dbMysql.execute('select * from tb_pegawai')
#     row_headers = [x[0] for x in dbMysql.description]
#     listData = dbMysql.fetchall()
#     json_data = []
#     for result in listData:
#         json_data.append(dict(zip(row_headers, result)))

#     return{'Data Pegawai':json_data}

# @app.route('/keuangan/gaji', methods = ['POST'])
# def gajiLembur():
#     global sudahLoginKeuangan
#     if sudahLoginKeuangan == False:
#         return f'Silahkan login sebagai Keuangan!'

#     id_pegawai = request.form['id_pegawai']
#     lembur = request.form['lembur']
#     dbMysql.execute(f"select nama_pegawai,divisi,gaji from (select * from tb_pegawai where id_pegawai = '{id_pegawai}') a left join tb_divisi on a.id_divisi=tb_divisi.id_divisi")
#     data = dbMysql.fetchall()
#     for row in data:
#         gaji = row[2]
    
#     if int(lembur) == 0:
#         gaji_lembur = 0
#     elif int(lembur) > 0 and int(lembur) < 16:
#         gaji_lembur = 75000
#     elif int(lembur) > 15:
#         gaji_lembur = 150000

#     total = int(gaji) + gaji_lembur

#     try:
#         dbMysql.execute('INSERT INTO tb_gaji (id_pegawai, gaji, lembur, gaji_lembur, total_gaji) VALUES (?, ?, ?, ?, ?)', (id_pegawai, gaji, lembur, gaji_lembur, total))
#     except mariadb.Error as e:
#         print(f'Error {e}')

#     conn.commit()
#     return f'ID_Pegawai  = {id_pegawai}\nGaji        = {gaji}\nLembur/jam  = {lembur}\nGaji Lembur = {gaji_lembur}\nTotal Gaji  = {total}'

# @app.route('/keuangan/updategaji/', methods = ['PUT'])
# def updateGaji():
#     global sudahLoginKeuangan
#     if sudahLoginKeuangan == False:
#         return f'Silahkan login sebagai Keuangan!'

#     dbMysql.execute('select nama_pegawai,divisi,gaji from tb_pegawai inner join tb_divisi on tb_pegawai.id_divisi=tb_divisi.id_divisi')
#     data = dbMysql.fetchall()
#     for row in data:
#         gaji = row[2]

#     id_pegawai = request.form['id_pegawai']
#     lembur = request.form['lembur']
#     if int(lembur) == 0:
#         gaji_lembur = 0
#     elif int(lembur) > 0 and int(lembur) < 16:
#         gaji_lembur = 75000
#     elif int(lembur) > 15:
#         gaji_lembur = 150000
    
#     total = int(gaji) + gaji_lembur

#     try:
#         dbMysql.execute(f'UPDATE tb_gaji set gaji=?, lembur=?, gaji_lembur=?, total_gaji=? where id_pegawai=?',(gaji, lembur, gaji_lembur, total, id_pegawai))
#     except mariadb.Error as e:
#         print(f'Error {e}')
    
#     conn.commit()
#     return f'ID_Pegawai  = {id_pegawai}\nGaji        = {gaji}\nLembur/jam  = {lembur}\nGaji Lembur = {gaji_lembur}\nTotal Gaji  = {total}'

# @app.route('/keuangan/deletegaji', methods = ['DELETE'])
# def deleteGaji():
#     global sudahLoginKeuangan
#     if sudahLoginKeuangan == False:
#         return f'Silahkan login sebagai Keuangan!'

#     id_pegawai = request.form['id_pegawai']
#     try:
#         dbMysql.execute(f"DELETE FROM tb_gaji where id_pegawai='{id_pegawai}'")
#     except mariadb.Error as e:
#         print(f'Error {e}')
    
#     conn.commit()
#     return 'success'

# @app.route('/keuangan/datagaji', methods = ['GET'])
# def dataGaji():
#     global sudahLoginKeuangan
#     if sudahLoginKeuangan == False:
#         return f'Silahkan login sebagai Keuangan!'

#     dbMysql.execute('select * from tb_gaji')
#     row_headers = [x[0] for x in dbMysql.description]
#     listData = dbMysql.fetchall()
#     json_data = []
#     for result in listData:
#         json_data.append(dict(zip(row_headers, result)))

#     return{'Data Gaji Pegawai':json_data}

# @app.route('/keuangan/rekaplaporan', methods = ['GET'])
# def rekapLaporan():
#     global sudahLoginKeuangan
#     if sudahLoginKeuangan == False:
#         return f'Silahkan login sebagai Keuangan!'

#     dbMysql.execute('select * from tb_pegawai LEFT JOIN tb_gaji on tb_pegawai.id_pegawai=tb_gaji.id_pegawai')
#     row_headers = [x[0] for x in dbMysql.description]
#     listData = dbMysql.fetchall()
#     json_data = []
#     for result in listData:
#         json_data.append(dict(zip(row_headers, result)))

#     return{'Rekap Laporan':json_data}

# # PIMPINAN
# @app.route('/pimpinan/laporan', methods = ['GET'])
# def dataPimpinan():
#     global sudahLoginPimpinan
#     if sudahLoginPimpinan == False:
#         return f'Silahkan login sebagai Pimpinan!'

#     dbMysql.execute('select * from tb_pegawai LEFT JOIN tb_gaji on tb_pegawai.id_pegawai=tb_gaji.id_pegawai')
#     row_headers = [x[0] for x in dbMysql.description]
#     listData = dbMysql.fetchall()
#     json_data = []
#     for result in listData:
#         json_data.append(dict(zip(row_headers, result)))

#     return{'Laporan Data Pegawai':json_data}