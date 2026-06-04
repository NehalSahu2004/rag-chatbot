import {
  BrowserRouter,
  Routes,
  Route
} from "react-router-dom";

import Home from "../pages/Home";
import Login from "../pages/Login";

import ProtectedRoute from "../components/ProtectedRoute";

function AppRoutes() {

  return (

    <BrowserRouter>

      <Routes>

        <Route
          path="/login"
          element={<Login />}
        />

        <Route
          path="/"
          element={

            <ProtectedRoute>

              <Home />

            </ProtectedRoute>

          }
        />

      </Routes>

    </BrowserRouter>

  );

}

export default AppRoutes;