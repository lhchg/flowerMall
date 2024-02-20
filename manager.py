from application import app
import sys
import traceback
import www

def main():
    app.run(host="0.0.0.0", port=app.config['SERVER_PORT'], debug=True)

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        traceback.print_exc()
