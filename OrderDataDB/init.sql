CREATE SCHEMA IF NOT EXISTS order_storage;

DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'status') THEN
    CREATE TYPE order_storage.status AS ENUM (
      'NEW',
      'FINISHED',
      'CANCELLED'
    );
  END IF;
END$$;

CREATE TABLE IF NOT EXISTS order_storage.orders (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL,
    amount FLOAT NOT NULL,
    description VARCHAR(255) NOT NULL,
    status order_storage.status NOT NULL DEFAULT 'NEW'
);

CREATE TABLE IF NOT EXISTS order_storage.messages (
    order_id UUID PRIMARY KEY NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    processed BOOLEAN NOT NULL DEFAULT FALSE,
    user_id UUID NOT NULL,
    amount FLOAT NOT NULL,
    FOREIGN KEY (order_id) REFERENCES order_storage.orders(id)
);