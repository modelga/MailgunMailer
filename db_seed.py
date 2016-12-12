from app.models.SQL_DB import User, Newsletter, db

print("\nCreating DB Tables")
try:
    db.create_all()
    print("OK  : Tables Created")
except:
    print("BAD : Problem creating tables. Check DB connection parameters")

print("\nCreating user Admin with username/pass : admin@example.com/admin")
try:
    admin = User('1', 'admin@example.com', '$2b$12$0wT4k2MD5r7tcTmADJ1.ROdTNKIff2TDFIXxtXiReXauBqkDaQpgq', 'Mailer',
                 'Admin', 'Mailer', 'www.example.com', 'key-123456789', 'newsletter.example.com',
                 'Example.com <postmaster@example.com>', 'e64c7d89f26bd1972efa854d13d7dd61', True)
    db.session.add(admin)
    db.session.commit()
    print("OK  : User Admin created")
except:
    print("BAD : Problem in User creation")

print("\nCreating example Newsletter for admin user")
try:
    newsletter = Newsletter('1', 'admin@example.com', 'all@example.com', 'Hello World', None, '123', 0, 'Test Subject',
                            'admin@example.com', 'TAG1', 'CAMP1')
    db.session.add(newsletter)
    db.session.commit()
    print("OK  : Newsletter Created")
except:
    print("BAD : Problem in Newsletter creation")
