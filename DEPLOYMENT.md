# EcoMind frontend on Vercel with a local backend

The Vercel site `https://ecomind-seven.vercel.app` is allowed by the Python API.

Set this Vercel environment variable and redeploy the frontend:

```text
VITE_API_URL=http://127.0.0.1:8000
```

Then restart the local backend so the updated CORS rules are loaded. The Vercel page can reach that backend only from the same computer on which the backend is running. Other visitors cannot use your computer's `localhost`; a public multi-user deployment requires an HTTPS-hosted backend URL instead.

Additional trusted frontend origins can be supplied when starting the backend with the comma-separated `ECOMIND_ALLOWED_ORIGINS` environment variable.
