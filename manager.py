from application import app
import sys
import traceback

def main():
    app.run(host="0.0.0.0", port=5001)

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        traceback.print_exc()
