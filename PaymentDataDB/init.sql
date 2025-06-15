CREATE SCHEMA IF NOT EXISTS payment_storage;

CREATE TABLE IF NOT EXISTS payment_storage.bank_accounts (
    user_id UUID PRIMARY KEY,
    balance FLOAT NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL
);

CREATE TABLE IF NOT EXISTS payment_storage.inbox_messages (
    order_id UUID PRIMARY KEY NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    processed BOOLEAN NOT NULL DEFAULT FALSE,
    user_id UUID NOT NULL,
    amount FLOAT NOT NULL
);

CREATE TABLE IF NOT EXISTS payment_storage.outbox_messages (
    order_id UUID PRIMARY KEY NOT NULL,
    is_success BOOLEAN NULL,
    processed BOOLEAN NOT NULL DEFAULT FALSE,
    description VARCHAR(255) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES payment_storage.inbox_messages(order_id)
);