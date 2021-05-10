USE databaseName;                 --- Database_name
CREATE TABLE users (
				userid varchar(50) not null,
				passwd varchar(50) not null,
				uname varchar(50) not null,
				photo BLOB not null,
				accntno varchar(10) not null,
				addr varchar(70) not null,
				email varchar(40) not null,
				branchcode varchar(5),
				accntbal decimal(15,2),
				aadhar varchar(12) not null,
				phoneno varchar(10) not null,
                unique (userid),
				primary key (userid)
);
INSERT INTO users VALUES('temp','temp','temp','temp','1005921356','temp','temp','temp','0.00','temp','temp');
CREATE TABLE branches (brname varchar(20),brcode varchar(5),ifsc varchar(11));
INSERT INTO branches VALUES
                    ('Jaipur','JP010','RBN100JP010'),
                    ('Surat','ST011','RBN100ST011'),
                    ('Pune','PN012','RBN100PN012'),
                    ('Ahmedabad','AMD13','RBN100AMD13'),
                    ('Hyderabad','HDB14','RBN100HDB14'),
                    ('Bengaluru','BN015','RBN100BN015'),
                    ('Chennai','CN016','RBN100CN016'),
                    ('Kolkata','KL017','RBN100KL017'),
                    ('Agra','AG018','RBN100AG018'),
                    ('Mumbai','MB019','RBN100MB019'),
                    ('Noida','ND020','RBN100ND020');
SELECT * FROM users;
SELECT * FROM branches;
commit;
