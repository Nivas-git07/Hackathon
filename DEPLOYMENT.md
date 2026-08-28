# EcoMind runtime on Vercel with a local backend

The React + Vite application now lives in `runtime`. Set the Vercel project's
Root Directory to `runtime`, then use the standard Vite build settings:

```text
Build Command: npm run build
Output Directory: dist
```

The Vercel site `https://ecomind-seven.vercel.app` is allowed by the Python API.

Set this Vercel environment variable and redeploy the site:

```text
VITE_API_URL=http://127.0.0.1:8000
```

Then restart the local backend so the updated CORS rules are loaded. The Vercel page can reach that backend only from the same computer on which the backend is running. Other visitors cannot use your computer's `localhost`; a public multi-user deployment requires an HTTPS-hosted backend URL instead.

Additional trusted frontend origins can be supplied when starting the backend with the comma-separated `ECOMIND_ALLOWED_ORIGINS` environment variable.

For local development, run these commands from `runtime`:

```text
npm install
npm run dev
```

Then open `http://127.0.0.1:5173/dashboard`.
