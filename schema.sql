CREATE TABLE "admins" (
    "username" TEXT,
    "password" TEXT NOT NULL,
    PRIMARY KEY("username")
);

CREATE TABLE "services" (
    "id" INTEGER,
    "name" TEXT NOT NULL UNIQUE,
    "description" TEXT NOT NULL,
    "price" REAL NOT NULL,
    PRIMARY KEY("id")
);

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
    "experience" INTEGER NOT NULL,
    "description" TEXT NOT NULL,
    "date_created" DATETIME DEFAULT CURRENT_TIMESTAMP,
    "rating" REAL DEFAULT 0,
    "status" TEXT CHECK("status" in (NULL, 'active', 'block')) DEFAULT NULL,
    PRIMARY KEY("id"),
    FOREIGN KEY("service_id") REFERENCES "services"("id") ON DELETE CASCADE
);

CREATE TABLE "customers" (
    "id" INTEGER,
    "fname" TEXT NOT NULL,
    "lname" TEXT,
    "address" TEXT NOT NULL,
    "pincode" INTEGER NOT NULL,
    "contact_number" TEXT NOT NULL UNIQUE,
    "email" TEXT NOT NULL UNIQUE,
    "password" TEXT NOT NULL,
    "status" TEXT CHECK("status" in ('active', 'block')) DEFAULT 'active',
    PRIMARY KEY("id")
);

CREATE TABLE "service_requests" (
    "id" INTEGER,
    "service_id" INTEGER NOT NULL,
    "customer_id" INTEGER NOT NULL,
    "professional_id" INTEGER NOT NULL,
    "date_of_request" DATETIME DEFAULT CURRENT_TIMESTAMP,
    "date_of_completion" DATETIME,
    "status" TEXT DEFAULT 'requested' CHECK("status" in ('requested', 'accepted', 'rejected', 'closed')),
    "rating" INTEGER,
    "remarks" TEXT,
    PRIMARY KEY("id"),
    FOREIGN KEY("service_id") REFERENCES "services"("id") ON DELETE CASCADE,
    FOREIGN KEY("customer_id") REFERENCES "customers"("id") ON DELETE CASCADE,
    FOREIGN KEY("professional_id") REFERENCES "professionals"("id") ON DELETE CASCADE
);

INSERT OR IGNORE INTO "admins"
VALUES ('admin', 'admin');