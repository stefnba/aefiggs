CREATE TABLE
    IF NOT EXISTS "currency_rate" (
        "base_currency" text NOT NULL,
        "quote_currency" text NOT NULL,
        "date" timestamp(3) NOT NULL,
        "rate" numeric NOT NULL,
        "created_at" timestamp(3) DEFAULT now () NOT NULL,
        CONSTRAINT "currency_rate_base_currency_quote_currency_date_pk" PRIMARY KEY ("base_currency", "quote_currency", "date")
    );