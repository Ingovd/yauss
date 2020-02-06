import sys
sys.path.append(r'.\\yauss\\')

from models import db, scoped_session
from app import app
from keys import bulk_insert

def main():
    db.create_all()
    with scoped_session() as session:
        bulk_insert(session, n=1337)

if __name__ == "__main__":
    main()