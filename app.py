from sampling import app

if __name__ == "__main__":
    app.run(debug = False, host="0.0.0.0", port="9080", use_reloader=False,)