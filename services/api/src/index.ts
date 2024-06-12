import { Hono } from "hono";
import { db } from "./db/client";

const app = new Hono();

app.get("/", (c) => {
  return c.json({ message: "Hello Hono! How are you? This is v2!" });
});

app.get("/rates", async (c) => {
  // const rates = await c.fetch("https://api.exchangerate-api.com/v4/latest/USD");
  const rates = await db.query.currencyRate.findMany();
  return c.json({ rates });
});

export default app;
