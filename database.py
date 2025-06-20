from firebase_admin import db, credentials
import os
import firebase_admin

cred = credentials.Certificate("fax-db-credentials.json")
firebase_admin.initialize_app(cred, {'databaseURL': "https://fax-db-807bb-default-rtdb.europe-west1.firebasedatabase.app"})
def get_db(table):
    ref = db.reference(f'/{table}/')
    got = dict(ref.get())
    return got

def update_db(table, child2, data):
    if "/" in table:
        table = table.split('/')
        ref = db.reference(f'/{table[0]}/')
        table.pop(0)
        ref2 = ref
        for x in table:
            ref2 = ref2.child(x)

    else:
        if child2 == "none":
            ref = db.reference(f'/{table}/')
            ref.update(data)
            return

        else:
            ref = db.reference(f'/{table}/')
            ref2 = ref

    child_ref = ref2.child(f'{child2}')
    child_ref.update(data)


def del_db(table, child2):
    if "/" in table:
        table = table.split('/')
        ref = db.reference(f'/{table[0]}/')
        table.pop(0)
        ref2 = ref
        for x in table:
            ref2 = ref2.child(x)

    else:
        ref = db.reference(f'/{table}/')
        ref2 = ref

    child_ref = ref2.child(f'{child2}')
    child_ref.delete()

