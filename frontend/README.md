# Local Hub Frontend

Vue/Vite frontend for Local Hub.

## Setup

```sh
npm install
```

## Development

Start the backend from the repository root first. The backend serves the main API and the AI chatbot API together on port `8000`.

```sh
npm run dev:backend
```

Then start the frontend:

```sh
npm run dev
```

The Vite dev server proxies `/api` and `/api/chat` to `http://127.0.0.1:8000`.

From the repository root, you can also run:

```sh
npm run dev:frontend
```

## Build

```sh
npm run build
```
