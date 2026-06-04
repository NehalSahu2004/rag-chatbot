import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

function Login() {

  const navigate =
    useNavigate();

  const { login } =
    useAuth();

  const [email, setEmail] =
    useState("");

  const [password, setPassword] =
    useState("");

  const [error, setError] =
    useState("");

  const handleSubmit =
    async (e) => {

      e.preventDefault();

      try {

        await login(
          email,
          password
        );

        navigate("/");

      }

      catch {

        setError(
          "Invalid credentials"
        );
      }

    };

  return (

    <div
      className="
      min-h-screen
      flex
      items-center
      justify-center
      bg-black
      text-white
    "
    >

      <form
        onSubmit={handleSubmit}
        className="
        bg-[#111]
        p-8
        rounded-xl
        w-[400px]
      "
      >

        <h1
          className="
          text-3xl
          mb-6
          text-center
        "
        >
          Login
        </h1>

        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) =>
            setEmail(
              e.target.value
            )
          }
          className="
          w-full
          p-3
          mb-4
          bg-[#222]
          rounded
        "
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) =>
            setPassword(
              e.target.value
            )
          }
          className="
          w-full
          p-3
          mb-4
          bg-[#222]
          rounded
        "
        />

        {error && (

          <p
            className="
            text-red-500
            mb-4
          "
          >
            {error}
          </p>

        )}

        <button
          type="submit"
          className="
          w-full
          bg-blue-600
          p-3
          rounded
        "
        >
          Login
        </button>

      </form>

    </div>

  );

}

export default Login;