from API import create_app  # , db
import os
app = create_app()

if __name__ == '__main__':
    # with app.app_context():
    #     db.create_all()
    debug_mode = True if os.getenv("DEBUG") == "true" else False
    app.run(debug=debug_mode)
