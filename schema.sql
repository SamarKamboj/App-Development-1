CREATE TABLE "admins" (
    "username" TEXT,
    "password" TEXT NOT NULL,
    PRIMARY KEY("username")
);

INSERT OR IGNORE INTO "admins"
VALUES ('admin', 'admin');

CREATE TABLE "professionals" (
    "id" INTEGER,
    "fname" TEXT NOT NULL,
    "lname" TEXT,
    "address" TEXT NOT NULL,
    "pincode" INTEGER NOT NULL,
    "contact_number" TEXT NOT NULL UNIQUE,
    "email" TEXT NOT NULL UNIQUE,
    "password" TEXT NOT NULL,
    "service_id" INTEGER NOT NULL,
    "experience" INTEGER,
    "description" TEXT NOT NULL,
    "date_created" DATETIME DEFAULT CURRENT_TIMESTAMP,
    "rating" REAL,
    "status" TEXT CHECK("status" in (NULL, 'active', 'block')) DEFAULT NULL,
    PRIMARY KEY("id"),
    FOREIGN KEY("service_id") REFERENCES "services"("id")
);

CREATE TABLE "customers" (
    "id" INTEGER,
    "fname" TEXT NOT NULL,
    "lname" TEXT,
    "address" TEXT,
    "pincode" INTEGER,
    "contact_number" TEXT NOT NULL UNIQUE,
    "email" TEXT NOT NULL UNIQUE,
    "password" TEXT NOT NULL,
    "status" TEXT CHECK("status" in ('active', 'block')) DEFAULT 'active',
    PRIMARY KEY("id")
);

CREATE TABLE "services" (
    "id" INTEGER,
    "name" TEXT NOT NULL UNIQUE,
    "description" TEXT NOT NULL,
    "price" REAL NOT NULL,
    PRIMARY KEY("id")
);

CREATE TABLE "service_requests" (
    "id" INTEGER,
    "service_id" INTEGER NOT NULL,
    "customer_id" INTEGER NOT NULL,
    "professional_id" INTEGER NOT NULL,
    "date_of_request" DATETIME DEFAULT CURRENT_TIMESTAMP,
    "date_of_completion" DATETIME,
    "status" TEXT CHECK("status" in ('requested', 'accepted', 'closed')),
    "rating" INTEGER,
    "remarks" TEXT,
    PRIMARY KEY("id"),
    FOREIGN KEY("service_id") REFERENCES "services"("id"),
    FOREIGN KEY("customer_id") REFERENCES "customers"("id"),
    FOREIGN KEY("professional_id") REFERENCES "professionals"("id")
);