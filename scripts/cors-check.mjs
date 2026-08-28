const api = 'http://127.0.0.1:8000/api/demo';
const origin = 'https://ecomind-seven.vercel.app';

const response = await fetch(api, { headers: { Origin: origin } });
if (!response.ok || response.headers.get('access-control-allow-origin') !== origin) {
  throw new Error('Vercel GET origin was not accepted');
}

const preflight = await fetch(api, {
  method: 'OPTIONS',
  headers: {
    Origin: origin,
    'Access-Control-Request-Method': 'GET',
    'Access-Control-Request-Private-Network': 'true',
  },
});

if (
  preflight.status !== 204 ||
  preflight.headers.get('access-control-allow-origin') !== origin ||
  preflight.headers.get('access-control-allow-private-network') !== 'true'
) {
  throw new Error('Vercel private-network preflight was not accepted');
}

console.log(JSON.stringify({ status: 'ok', origin, api }));
