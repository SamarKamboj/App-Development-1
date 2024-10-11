CREATE TABLE "admins" (
    "id" INTEGER,
    "username" TEXT NOT NULL UNIQUE,
    "password" TEXT NOT NULL,
    PRIMARY KEY("id")
);

INSERT INTO "admins" ("username", "password")
VALUES ('admin', 'admin');

CREATE TABLE "professionals" (
    "id" INTEGER,
    "fname" TEXT NOT NULL,
    "lname" TEXT,
    "email" TEXT NOT NULL UNIQUE,
    "password" TEXT NOT NULL,
    "service_id" INTEGER NOT NULL,
    "experience" INTEGER,
    "address" TEXT,
    "pincode" INTEGER,
    "description" TEXT,
    "date_created" DATETIME DEFAULT CURRENT_TIMESTAMP,
    "status" CHAR(1) CHECK("status" in ('A', 'N')),
    PRIMARY KEY("id"),
    FOREIGN KEY("service_id") REFERENCES "services"("id")
);

CREATE TABLE "customers" (
    "id" INTEGER,
    "fname" TEXT NOT NULL,
    "lname" TEXT,
    "email" TEXT NOT NULL UNIQUE,
    "password" TEXT NOT NULL,
    "address" TEXT,
    "pincode" INTEGER,
    PRIMARY KEY("id")
);

CREATE TABLE "services" (
    "id" INTEGER,
    "name" TEXT NOT NULL UNIQUE,
    "description" TEXT,
    "price" NUMERIC NOT NULL,
    PRIMARY KEY("id")
);

CREATE TABLE "service_requests" (
    "id" INTEGER,
    "service_id" INTEGER NOT NULL,
    "customer_id" INTEGER NOT NULL,
    "professional_id" INTEGER NOT NULL,
    "date_of_request" DATETIME DEFAULT CURRENT_TIMESTAMP,
    "date_of_completion" DATETIME,
    "status" CHAR(1) CHECK("status" in ('R', 'A', 'C')),
    "remarks" TEXT,
    PRIMARY KEY("id"),
    FOREIGN KEY("service_id") REFERENCES "services"("id"),
    FOREIGN KEY("customer_id") REFERENCES "customers"("id"),
    FOREIGN KEY("professional_id") REFERENCES "professionals"("id")
);