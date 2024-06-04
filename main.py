from app.static.GUI import App
from app.db.cbdb_connection import DB_Connection

import app.api.run_api as dec_api

import threading


if __name__ == "__main__":
    app = App()
    app.title("CipherBytesDB")
    app.geometry("1300x800")
    app.configure(bg="white")

    # Start the decryption API server in a daemon thread
    api_thread = threading.Thread(target=dec_api.run, daemon=True)
    api_thread.start()

    app.mainloop()
    
    # Close open database connections
    DB_Connection.close_connections()
