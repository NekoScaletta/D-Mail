function SpamForm({ text, setText, loading, onSubmit, onUseSample, sampleEmails }) {
  return (
    <section className="input-panel" aria-label="Form kiểm tra email">
      <div className="panel-heading">
        <h2>Nội dung email</h2>
        <span>{text.trim().length} ký tự</span>
      </div>

      <textarea
        value={text}
        onChange={(event) => setText(event.target.value)}
        placeholder="Dán nội dung email cần kiểm tra..."
        rows={10}
      />

      <div className="sample-row">
        {sampleEmails.map((sample, index) => (
          <button key={sample} type="button" className="ghost-button" onClick={() => onUseSample(sample)}>
            Mẫu {index + 1}
          </button>
        ))}
      </div>

      <button type="button" className="primary-button" onClick={onSubmit} disabled={loading}>
        {loading ? 'Đang kiểm tra...' : 'Kiểm tra'}
      </button>
    </section>
  );
}

export default SpamForm;
