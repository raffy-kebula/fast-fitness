interface Step1Data {
  name: string;
  surname: string;
  date_of_birth: string;
  location_of_birth: string;
}

interface Props {
  data: Step1Data;
  onChange: (data: Step1Data) => void;
  onNext: () => void;
}

export function RegisterStep1({ data, onChange, onNext }: Props) {
  const set = (field: keyof Step1Data) => (e: React.ChangeEvent<HTMLInputElement>) =>
    onChange({ ...data, [field]: e.target.value });

  const valid =
    data.name.trim().length >= 2 &&
    data.surname.trim().length >= 2 &&
    !!data.date_of_birth &&
    data.location_of_birth.trim().length >= 2;

  return (
    <div>
      <div className="mb-3">
        <label className="form-label fw-medium">Nome</label>
        <input className="form-control" value={data.name} onChange={set("name")} placeholder="Mario" />
      </div>
      <div className="mb-3">
        <label className="form-label fw-medium">Cognome</label>
        <input className="form-control" value={data.surname} onChange={set("surname")} placeholder="Rossi" />
      </div>
      <div className="mb-3">
        <label className="form-label fw-medium">Data di nascita</label>
        <input type="date" className="form-control" value={data.date_of_birth} onChange={set("date_of_birth")} />
      </div>
      <div className="mb-3">
        <label className="form-label fw-medium">Luogo di nascita</label>
        <input className="form-control" value={data.location_of_birth} onChange={set("location_of_birth")} placeholder="Roma" />
      </div>
      <div className="d-grid mt-4">
        <button className="btn btn-primary" onClick={onNext} disabled={!valid}>
          Continua
        </button>
      </div>
    </div>
  );
}