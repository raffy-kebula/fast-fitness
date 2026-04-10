interface Step2Data {
  country: string;
  street_address: string;
  street_number: string;
  city: string;
  zip_code: string;
  phone_number: string;
}

interface Props {
  data: Step2Data;
  onChange: (data: Step2Data) => void;
  onNext: () => void;
  onBack: () => void;
}

export function RegisterStep2({ data, onChange, onNext, onBack }: Props) {
  const set = (field: keyof Step2Data) => (e: React.ChangeEvent<HTMLInputElement>) =>
    onChange({ ...data, [field]: e.target.value });

  const valid =
    data.country.trim().length >= 2 &&
    data.street_address.trim().length >= 2 &&
    Number(data.street_number) > 0 &&
    data.city.trim().length >= 2 &&
    /^\d{4,10}$/.test(data.zip_code) &&
    /^\+\d{7,17}$/.test(data.phone_number);

  return (
    <div>
      <div className="mb-3">
        <label className="form-label fw-medium">Paese</label>
        <input className="form-control" value={data.country} onChange={set("country")} placeholder="Italia" />
      </div>
      <div className="row g-2 mb-3">
        <div className="col-8">
          <label className="form-label fw-medium">Via</label>
          <input className="form-control" value={data.street_address} onChange={set("street_address")} placeholder="Via Roma" />
        </div>
        <div className="col-4">
          <label className="form-label fw-medium">N°</label>
          <input type="number" min={1} className="form-control" value={data.street_number} onChange={set("street_number")} placeholder="1" />
        </div>
      </div>
      <div className="row g-2 mb-3">
        <div className="col-7">
          <label className="form-label fw-medium">Città</label>
          <input className="form-control" value={data.city} onChange={set("city")} placeholder="Milano" />
        </div>
        <div className="col-5">
          <label className="form-label fw-medium">CAP</label>
          <input className="form-control" value={data.zip_code} onChange={set("zip_code")} placeholder="20100" maxLength={10} />
        </div>
      </div>
      <div className="mb-3">
        <label className="form-label fw-medium">Telefono</label>
        <input className="form-control" value={data.phone_number} onChange={set("phone_number")} placeholder="+39 3331234567" />
        <div className="form-text">Formato internazionale, es. +39 3331234567</div>
      </div>
      <div className="d-flex gap-2 mt-4">
        <button className="btn btn-outline-secondary w-50" onClick={onBack}>Indietro</button>
        <button className="btn btn-primary w-50" onClick={onNext} disabled={!valid}>Continua</button>
      </div>
    </div>
  );
}