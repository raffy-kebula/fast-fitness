import { useState, type FormEvent } from "react";

interface LoginFormProps {
  onSubmit: (username: string, password: string) => void;
  loading: boolean;
  error: string | null;
}

export function LoginForm({ onSubmit, loading, error }: LoginFormProps) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    if (username.trim() && password) {
      onSubmit(username.trim(), password);
    }
  };

  return (
    <form onSubmit={handleSubmit} noValidate>
      <div className="mb-3">
        <label htmlFor="username" className="form-label fw-medium">
          Username
        </label>
        <input
          id="username"
          type="text"
          className="form-control"
          autoComplete="username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          disabled={loading}
          placeholder="Il tuo username"
          required
        />
      </div>

      <div className="mb-3">
        <label htmlFor="password" className="form-label fw-medium">
          Password
        </label>
        <div className="input-group">
          <input
            id="password"
            type={showPassword ? "text" : "password"}
            className="form-control"
            autoComplete="current-password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            disabled={loading}
            placeholder="••••••••"
            required
          />
          <button
            type="button"
            className="btn btn-outline-secondary"
            onClick={() => setShowPassword((v) => !v)}
            aria-label={showPassword ? "Nascondi password" : "Mostra password"}
          >
            {showPassword ? "Nascondi" : "Mostra"}
          </button>
        </div>
      </div>

      {error && (
        <div className="alert alert-danger py-2 px-3" role="alert">
          {error}
        </div>
      )}

      <div className="d-grid mt-4">
        <button
          type="submit"
          className="btn btn-primary"
          disabled={loading || !username.trim() || !password}
        >
          {loading && (
            <span
              className="spinner-border spinner-border-sm me-2"
              role="status"
              aria-hidden="true"
            />
          )}
          {loading ? "Accesso in corso..." : "Accedi"}
        </button>
      </div>
    </form>
  );
}