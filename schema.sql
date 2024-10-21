CREATE TABLE "admins" (
    "username" TEXT,
    "password" TEXT NOT NULL,
    PRIMARY KEY("username")
);

CREATE TABLE "services" (
    "id" INTEGER,
    "name" TEXT NOT NULL UNIQUE,
    "description" TEXT NOT NULL,
    "base_price" REAL NOT NULL,
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
    "service_price" REAL NOT NULL,
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

INSERT OR IGNORE INTO "services" ("name", "description", "base_price")
VALUES ('Saloon', 'We provide best hair cut for men and women in the market at a very low price.',199.99),
('Cleaning', 'We provide cleaning of toilets at a very low price', 999),
('Cook', "Cooks are a need in today's life where both men and women go to work. Our active customers trust us the most. Price below is per month.", 2199);