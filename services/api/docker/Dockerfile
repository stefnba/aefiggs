ARG BUN_VERSION=1.1.13

FROM oven/bun:${BUN_VERSION}-slim as base

WORKDIR /app

# Set production environment
ENV NODE_ENV="production"


FROM base as build

COPY --link bun.lockb package.json ./
RUN bun install --ci

COPY --link src /app/src
COPY --link drizzle /app/drizzle

FROM base

COPY --from=build /app /app

EXPOSE 3000
CMD [ "bun", "run", "start" ]