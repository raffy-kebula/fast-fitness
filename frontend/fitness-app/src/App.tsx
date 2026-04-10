import { AuthProvider, useAuth } from "./context/AuthContext";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { LoginPage } from "./pages/LoginPage";
import { RegisterPage } from "./pages/RegisterPage";

function AppRoutes() {
  const { isAuthenticated } = useAuth();

  return (
    <Routes>
      {/* pubbliche */}
      <Route
        path="/login"
        element={!isAuthenticated ? <LoginPage /> : <Navigate to="/" />}
      />

      <Route
        path="/register"
        element={!isAuthenticated ? <RegisterPage /> : <Navigate to="/" />}
      />

      {/* privata */}
      <Route
        path="/"
        element={isAuthenticated ? <Dashboard /> : <Navigate to="/login" />}
      />
    </Routes>
  );
}

function Dashboard() {
  const { user, logout } = useAuth();

  return (
    <div style={{ padding: "2rem" }}>
      <h2>Benvenuto, utente {user?.id}</h2>
      <p>Ruolo: {user?.role}</p>
      <button onClick={logout}>Logout</button>
    </div>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <AppRoutes />
      </BrowserRouter>
    </AuthProvider>
  );
}