const BASE = "/api";

function getHeaders() {
  const token = localStorage.getItem("token");
  const h = {
    "Content-Type": "application/json",
    "ngrok-skip-browser-warning": "true",
  };
  if (token) h["Authorization"] = `Bearer ${token}`;
  return h;
}

async function request(method, path, body) {
  const res = await fetch(`${BASE}${path}`, {
    method,
    headers: getHeaders(),
    body: body !== undefined ? JSON.stringify(body) : undefined,
  });
  if (res.status === 204) return null;
  const data = await res.json();
  if (!res.ok) {
    const msg = data?.detail;
    throw new Error(typeof msg === "string" ? msg : JSON.stringify(msg));
  }
  return data;
}

export const authApi = {
  register: (d) => request("POST", "/auth/register", d),
  login: (d) => request("POST", "/auth/login", d),
  me: () => request("GET", "/auth/me"),
  listUsers: () => request("GET", "/auth/users"),
  toggleRole: (id) => request("POST", `/auth/users/${id}/toggle-role`),
};

export const tablesApi = {
  list: () => request("GET", "/tables/"),
  create: (d) => request("POST", "/tables/", d),
  update: (id, d) => request("PUT", `/tables/${id}`, d),
  remove: (id) => request("DELETE", `/tables/${id}`),
};

export const bookingsApi = {
  list: () => request("GET", "/bookings/"),
  create: (d) => request("POST", "/bookings/", d),
  cancel: (id) => request("DELETE", `/bookings/${id}`),
};
