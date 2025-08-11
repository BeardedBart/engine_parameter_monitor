#flask blueprints for db of SQLite3
from flask import Blueprint, render_template, redirect
from flask import g, request, url_for, flash
import sqlite3 
# import os 
 

# NOTE: end of functions for sql handling 
engdb = Blueprint(__name__, "engdb",
                  template_folder="templates",
                  static_folder='static', 
                  static_url_path='/')


PathToDB = 'engparamdb.db'


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(PathToDB)
        print("DB connected")
    return db


def make_db(cursor):
    #func for checking if db called engparamdb exists
    temp = "engpdb" #Engine Parameters Database
    table_check = cursor.execute(f"""
                                 SELECT name FROM sqlite_master 
                                 WHERE type='table' AND name='{temp}';
                                 """).fetchall()
    if table_check == []:
        cursor.execute(f"""
                       CREATE TABLE {temp} (
                           eng_name char(32),
                           typ char(32),
                           TOil REAL,
                           cht REAL,
                           egt REAL, 
                           oil_press_l REAL,
                           oil_press_h REAL
                       );
                       """)
    else:
        return True


def get_data(cursor):
    data = cursor.execute("""SELECT * FROM engpdb""").fetchall()
    return data

def g_coln(cursor,column):
    # GET COLUMN
    temp = cursor.execute(f"SELECT {column} FROM engpdb").fetchall()
    out = []
    for i in temp:
        out.append(i[0])
    return out

@engdb.route("/")
def database():
    temp_data = get_data(get_db().cursor())
    return render_template("db_view.html", tbl=temp_data)


@engdb.route("/add", methods=['GET','POST'])
def add_val():
    connect = get_db()
    cur = connect.cursor()
    
    if request.method == 'GET':
        return render_template("db_add.html")
    if request.method == 'POST':
        engname = request.form.get('engname')
        typ =  request.form.get('typ')
        toil = request.form.get('toil')
        cht = request.form.get('cht')
        egt = request.form.get('egt')
        p_oil_l = request.form.get('')
        p_oil_h = request.form.get('')
        
        cur.execute(f"""
                    INSERT INTO engpdb VALUES (
                        '{engname}',
                        '{typ}',
                        '{toil}',
                        '{cht}',
                        '{egt}',
                        '{p_oil_l}',
                        '{p_oil_h}'
                    );""")
        connect.commit()
        connect.close()
        return redirect(url_for("fdbsql.database"))


@engdb.route("/remove", methods=['GET','POST'])
def del_val():
    if request.method == 'POST':
        conn = get_db()
        cur = conn.cursor()
        check = g_coln(cur,'eng_name')
        rmvname = request.form.get('rmvname')
        
        if rmvname in check: 
            cur.execute(f"""DELETE FROM engpdb 
                        WHERE eng_name='{rmvname}'
                        """)
            
            conn.commit()
            conn.close()
            return redirect(url_for('fdbsql.database'))
        else:
            flash("Podany silnik nie istnieje w bazie danych, wpisz nazwę ponownie.")
            return redirect(url_for('fdbsql.del_val'))
            
    return render_template("db_rem_row.html")
    
    
@engdb.route("/remove_duplicates", methods=['GET','POST'])
def del_dupli():
    #function responsible for deleting duplicates
    if request.method == 'POST':
        # if request.form['rmvdupl]:
        connection = get_db()
        cur = connection.cursor()
        cur.execute(f"""
                    DELETE FROM engpdb
                    WHERE ROWID NOT IN(
                        SELECT MIN(ROWID)
                        FROM engpdb
                        GROUP BY eng_name);
                    """)
        connection.commit()
        connection.close()
        return redirect(url_for('fdbsql.database'))
    
    return render_template("db_rem_dupli.html")


@engdb.route("/mod_row_main", methods=['GET','POST'])
def mod_row_main():
    temp_data = get_data(get_db().cursor())
    if request.method == 'POST':
        conn = get_db()
        cur = conn.cursor()
        engname = request.form.get('engname')
        
        check = g_coln(cur,'eng_name')
        if engname in check:
            typ =  request.form.get('typ')
            toil = request.form.get('toil')
            cht = request.form.get('cht')
            egt = request.form.get('egt')
            p_oil_l = request.form.get('p_oil_l')
            p_oil_h = request.form.get('p_oil_h')
            
            cur.execute(f"""
                        UPDATE engpdb SET
                            typ='{typ}',
                            TOil='{toil}',
                            egt='{cht}',
                            cht='{egt}',
                            oil_press_l='{p_oil_l}',
                            oil_press_h='{p_oil_h}'
                        WHERE eng_name='{engname}';""")
            conn.commit()
            conn.close()
        else:
            flash("Podany silnik nie jest w bazie danych, spróbuj wpisać nazwę ponownie")
            return redirect(url_for('fdbsql.mod_row_main'))
    
    return render_template('db_chng_row.html', tbl=temp_data)


@engdb.route("/add_col", methods=['GET','POST'])
def add_col():
    DTYPES = ['char(32)','REAL','INTEGER','TEXT']
    if request.method == "POST":
        conn = get_db()
        cur = conn.cursor()
        ColName = request.form.get('ColName')
        dtype = request.form.get('dtype')
        cur.execute(f"""ALTER TABLE engpdb
                    ADD '{ColName}' '{dtype}';
                    """)
        conn.commit()
        conn.close()
        return redirect(url_for('fdbsql.database'))
        
    return render_template('db_add_col.html', tbl=DTYPES)

@engdb.route('/rem_col', methods=['GET','POST'])
def rem_col():
    conn = get_db()
    cur = conn.cursor()
    NAMES = list()
    # ta - temporary array
    ta = cur.execute(f"""PRAGMA table_info('engpdb')
                        """).fetchall()
    for i in ta:
        NAMES.append(i[1])
    if request.method == 'POST':
        RColName = request.form.get('RColName')
        cur.execute(f"""ALTER TABLE engpdb
                    DROP COLUMN '{RColName}'""")
        conn.commit()
        conn.close()
        return redirect(url_for('fdbsql.database'))
        
    return render_template('db_rem_col.html',tbl=NAMES)


if __name__ == '__main__':
    print("Wrong way!")