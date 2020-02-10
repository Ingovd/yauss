import sys
from yauss import create_app as create_yauss
from key_store import create_app as create_key_store

def main():
    if len(sys.argv) == 1:
        app = create_yauss()
    else:
        app = create_key_store()
    app.run(debug=True)

if __name__ == "__main__":
    main()