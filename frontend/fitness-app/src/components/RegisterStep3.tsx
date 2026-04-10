import { useState } from "react";

interface Step3Data {
  username: string;
  email: string;
  password: string;
  confirmPassword: string;
}

interface Props {
  data: Step3Data;
  onChange: (data: Step3Data) => void;
  onSubmit: () => void;
  onBack: () => void;
  loading: boolean;
  error: string | null;
}

const PASSWORD_RE = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*(),.?":{}|<>]).{8,}$/;

export function RegisterStep3({ data, onChange, onSubmit, onBack, loading, error }: Props) {
  const [showPw, setShowPw] = useState(false);
  const [showConfirm, setShowConfirm] = useState(false);

  const set = (field: keyof Step3Data) => (e: React.ChangeEvent<HTMLInputElement>) =>
    onChange({ ...data, [field]: e.target.value });

  const passwordValid = PASSWORD_RE.test(data.password);
  const passwordMatch = data.password === data.confirmPassword && data.confirmPassword !== "";

  const valid =
    data.username.trim().length >= 3 &&
    data.email.includes("@") &&
    passwordValid &&
    passwordMatch;

  return (
    <div>
      <div className="mb-3">
        <label className="form-label fw-medium">Username</label>
        <input
          className="form-control"
          value={data.username}
          onChange={set("username")}
          placeholder="mario_rossi"
          autoComplete="username"
        />
        <div className="form-text">Minimo 3 caratteri.</div>
      </div>
      <div className="mb-3">
        <label className="form-label fw-medium">Email</label>
        <input
          type="email"
          className="form-control"
          value={data.email}
          onChange={set("email")}
          placeholder="mario@example.com"
          autoComplete="email"
        />
      </div>
      <div className="mb-3">
        <label className="form-label fw-medium">Password</label>
        <div className="input-group">
          <input
            type={showPw ? "text" : "password"}
            className={`form-control ${data.password && !passwordValid ? "is-invalid" : ""}`}
            value={data.password}
            onChange={set("password")}
            placeholder="••••••••"
            autoComplete="new-password"
          />
          <button type="button" className="btn btn-outline-secondary" onClick={() => setShowPw(v => !v)}>
            {showPw ? "Nascondi" : "Mostra"}
          </button>
        </div>
        <div className="form-text">
          Min. 8 caratteri, una maiuscola, una minuscola, un numero, un carattere speciale.
        </div>
      </div>
      <div className="mb-3">
        <label className="form-label fw-medium">Conferma password</label>
        <div className="input-group">
          <input
            type={showConfirm ? "text" : "password"}
            className={`form-control ${data.confirmPassword && !passwordMatch ? "is-invalid" : ""}`}
            value={data.confirmPassword}
            onChange={set("confirmPassword")}
            placeholder="••••••••"
            autoComplete="new-password"
          />
          <button type="button" className="btn btn-outline-secondary" onClick={() => setShowConfirm(v => !v)}>
            {showConfirm ? "Nascondi" : "Mostra"}
          </button>
          {data.confirmPassword && !passwordMatch && (
            <div className="invalid-feedback">Le password non coincidono.</div>
          )}
        </div>
      </div>

      {error && (
        <div className="alert alert-danger py-2 px-3" role="alert">
          {error}
        </div>
      )}

      <div className="d-flex gap-2 mt-4">
        <button className="btn btn-outline-secondary w-50" onClick={onBack} disabled={loading}>
          Indietro
        </button>
        <button className="btn btn-primary w-50" onClick={onSubmit} disabled={!valid || loading}>
          {loading && <span className="spinner-border spinner-border-sm me-2" aria-hidden="true" />}
          {loading ? "Registrazione..." : "Registrati"}
        </button>
      </div>
    </div>
  );
}