export const login = (username, password) =>
  request("/login", {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: new URLSearchParams({
      username,
      password,
    }),
  });

export const getCurrentSession = () =>
  request("/session");