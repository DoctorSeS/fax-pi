from firebase_admin import db, credentials
import os
import firebase_admin

os.environ["FIREBASE_CERTIFICATE"] = str({
  "type": "service_account",
  "project_id": "fax-db-807bb",
  "private_key_id": "fd9c24ea4c3912be9f0261d0d74370d967700cfd",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDROxHHnkkaHGq6\nhgU0FkcmTUqtvMipJW2mSs8ANPIi85Yv8E7lZ3Y65/zzZHikMNcoZmMgE5IV+WCA\nWxeV6rS+slYpYqz3aOh7VwjFNtQoTvxXEr19yGTZsYXQYuF5W/p58gN8jJRZ2pLO\n4PbdtvlE249Q+IFMa/Q3yLNsuM35QezCsNWOFAP89aq3Mt2A8UQS8MggSbNDuWOg\n/PR7/IQemp1dVflhFXfJvDKmLuEiBKJ79wm+xYBq7vUyBQRohRYRK4v6omvgboqN\nSfwRbFyTgR63dDhGiUwNoHO0FdWFbjE7SHdmsU49kMFgXFbh+ddQks/raUy5IWcQ\nMwreZtCXAgMBAAECggEAGJ762KKnt4rghFKBCkAU30z5HLi6ZC0jWg4zjbKtS6+e\nXMXKgvRJ1WS3P2zzRV758qcZwwyKhEt0L6aIf/u+iTIzMWuLLxIJSXpUbeCl1ph0\n2Uo7QjHyrCtXs83u+nj4YKE6B84DJw+xdubCJhUCADhWBRE5JeUOOAJGGuUkV9BT\nsww1e+xDr3cfk3d1GBCpMbJyrhabnpSU9u3nW2OWTbDTdQeNJFfWRETRidZkJHUk\n2dryrK1zdORs/Grnhs5uT0y0t27Qkg9RIPZFzvl/YqZGpxhPtNK7SfiiSOBlrpm+\nay5cZRVdbt83TCVtSRrPZkH9u66T0na0CVuKuFx0AQKBgQDqKqPVXwE5ZTKI6ZzX\nBh+qk+UCiG0cdd60gom2Mzb4ed8pZnsSSf9DvAMGKS8hPR5HQWx68bHArKItUTfw\nx7eyw/xV+qm+SGc2eZI3XvbNjAIeUA1+3CaUZU+b6+coY2O8MM5YLtVr3vVVWw5o\nw4h0+yEEQbjfo/GCq0+tx0rKBwKBgQDkvTt0wqq0bXHnBz6jLRWKi/ACH4UpwJHN\nirQYzCBPlZ/L75XI894VYL3C1wa4oSOoRjuJPJu2Gvv89lCp4N6+usK6pIBhFWBz\nZ2OgaCAaT4pgn7wCRjBB27RJZD4ga1rBW9ho7fmLIAvQjnEzvpKP+YO4nqh5y4sH\nci4dweRg8QKBgFAN1cbLXPrHOviNjR4BrO++8erkwxCYx1NE0VmltqRJ3d4kd+yv\nuYHpk8sWZ1Ngtqo7lp+NY2xwWF1Px+UcEhQeZnTqZf90dzyrYS5m2883jz3XtlVp\nZBMVc5rlkjg/ikg7E0AYesQPDCZrI8jzGAKOHCJ9aXuja5x1fp71Y/8fAoGBAKzN\nIGuW3Kstu0zTNkjDuHBQQ2L3OPxP1FY5INFS9F3rJStFthx3zyDLUtAs7ZDxeySW\n2kdVGDU8sX1q/4k2rk/ce1vRBoNRSOomAyedQhNeX6WbRsdZCv/V4J9JMX4AXDGT\nFyw+C7VE4mgOFAsJP2OxFgeVJKXOVRus8JXeco+hAoGBAKrUEWDSEdHoCYxSdSAv\nEj1bhc3i+zYWFEVzqoCIrl8Ig/B00cwlsFCn9r0RJg8UL5wjUKAYCM89DMN8Y7Iu\nm7V4oobb9QnEf+QmOpLldAmnyjkolRuLxKEKTkOG4xeTbOSQ0NCJPKFneUtT0KbC\naHa/BDm8MjwJiyQ3qegraOM/\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-83pb9@fax-db-807bb.iam.gserviceaccount.com",
  "client_id": "117930048679409101844",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-83pb9%40fax-db-807bb.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
})

cred = credentials.Certificate(eval(os.environ["FIREBASE_CERTIFICATE"]))
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

