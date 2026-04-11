import { useAuth } from "../context/AuthContext.tsx";

export function ProfilePage() {
  const { user } = useAuth();

  return (
    <div className="container mt-5">
      <div className="row justify-content-center">
        <div className="col-md-6">
          <div className="card p-4">

            {/* Avatar + nome */}
            <div className="d-flex flex-column align-items-center mb-4">
              <div
                style={{
                  width: "80px",
                  height: "80px",
                  borderRadius: "50%",
                  backgroundColor: "#ddd",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  fontSize: "2rem",
                  fontWeight: "bold",
                }}
              >
                {user?.role?.charAt(0)?.toUpperCase() || "U"}
              </div>
              {user?.role === "ADMIN" && (
                <span className="badge bg-dark mt-2">ADMIN</span>
              )}
              <h4 className="mt-3 mb-0">{user?.id || "Utente"}</h4>
            </div>

            {/* Info utente */}
            <ul className="list-group list-group-flush mb-4">
              <li className="list-group-item d-flex justify-content-between">
                <span className="text-muted">ID</span>
                <span>{user?.id}</span>
              </li>
              <li className="list-group-item d-flex justify-content-between">
                <span className="text-muted">Email</span>
                <span>{user?.id || "—"}</span>
              </li>
              <li className="list-group-item d-flex justify-content-between">
                <span className="text-muted">Ruolo</span>
                <span>{user?.role}</span>
              </li>
            </ul>

          </div>
        </div>
      </div>
    </div>
  );
}