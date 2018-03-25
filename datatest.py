import sqlite3
from difflib import get_close_matches

def create_table():
    conn = sqlite3.connect("lite.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS books(name TEXT,quantity INT,price REAL)")
    conn.commit()
    conn.close()

def insert(name,quantity,price):
    conn = sqlite3.connect("lite.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO books values(?,?,?)",(name,quantity,price))
    conn.commit()
    conn.close()

def delete(name):
    conn = sqlite3.connect("lite.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM books WHERE name = ?",(name,))
    conn.commit()
    conn.close()



def display():
    conn = sqlite3.connect("lite.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM books")
    rows = cur.fetchall()
    keys = list(rows)
    print("name\t\tquantity\tprice")
    print("_______________________________________")
    for i in rows:
        for j in i:
            print(j,end="\t\t")
        print()
    conn.close()

def search(name):
    conn = sqlite3.connect("lite.db")
    cur = conn.cursor()
    cur.execute("SELECT name from books")
    rows = cur.fetchall()
    keys=[]
    for i in range(0,len(rows)):
        keys.append(rows[i][0])
    if name in keys:
        cur.execute("SELECT * FROM books WHERE name=?",(name,))
        row = cur.fetchall()
        return row
    elif name.title() in keys:
        cur.execute("SELECT * FROM books WHERE name=?",(name.title(),))
        row = cur.fetchall()
        return row
    elif name.upper() in keys:
        cur.execute("SELECT * FROM books WHERE name=?",(name.upper(),))
        row = cur.fetchall()
        return row
    elif len(get_close_matches(name,keys,cutoff=0.8))>0:
        print("No search found related to "+name)
        c = get_close_matches(name,keys,cutoff=0.8)[0]
        y = input("did you mean "+c+" \n press Y to continue N to cancel: ")
        if y.lower()=='y':
            cur.execute("SELECT * FROM books WHERE name=?",(c,))
            row = cur.fetchall()
            return row[0]
    else:
        return "such word doesnot exist please double check your word"
    conn.close()

def update(name,quantity,price):
    conn = sqlite3.connect("lite.db")
    cur = conn.cursor()
    cur.execute("UPDATE books SET quantity=?,price=? where name = ?",(quantity,price,name,))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    s = input("choose any one:\n1.create\n2.insert\n3.display\n4.search\n5.update\n6.delete\n")
    if s == '1':
        create_table()
        print("succesfully created")

    elif s=='2':
        name = input('insert name: ')
        quantity = int(input('insert quantity: '))
        price = float(input('insert price: '))
        insert(name,quantity,price)
        display()
        print("succesfully inserted")

    elif s=='3':
        display()

    elif s=='4':
        name = input("enter the name to be searched: ")
        k = search(name.lower())
        if type(k)==list:
            for i in k:
                print(k)
        else:
            print(k)

    elif s=='5':
        name = input("enter the name to update the quantity and price: ")
        quantity = input("quantity: ")
        price = input("price: ")
        update(name,quantity,price)
        display()
        print("succesfully updated")

    elif s=='6':
        name = input("enter the name to be deleted: ")
        delete(name)
        display()
        print("succesfully deleted")
    else:
        print("enter the correct option")
