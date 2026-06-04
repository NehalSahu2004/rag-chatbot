import { createContext, useContext, useState } from "react";
import API from "../api/api";

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {

  const [user, setUser] = useState(null);

  const [token, setToken] = useState(
    localStorage.getItem("token")
  );

  const login = async (
    email,
    password
  ) => {

    const formData = new FormData();

    formData.append(
      "username",
      email
    );

    formData.append(
      "password",
      password
    );

    const response =
      await API.post(
        "/login",
        formData
      );

    const accessToken =
      response.data.access_token;

    localStorage.setItem(
      "token",
      accessToken
    );

    setToken(
      accessToken
    );

    const userResponse =
      await API.get("/me", {
        headers: {
          Authorization:
            `Bearer ${accessToken}`
        }
      });

    setUser(
      userResponse.data
    );

    return true;
  };

  const logout = () => {

    localStorage.removeItem(
      "token"
    );

    setToken(null);

    setUser(null);
  };

  return (

    <AuthContext.Provider
      value={{
        user,
        token,
        login,
        logout,
        isAuthenticated:
          !!token
      }}
    >

      {children}

    </AuthContext.Provider>

  );
};

export const useAuth = () =>
  useContext(AuthContext);