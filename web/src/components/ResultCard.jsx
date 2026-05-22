function ResultCard({ result, error, loading }) {
  const isSpam = result?.label === 1;
  const confidence = result ? Math.round(result.confidence * 100) : 0;

  return (
    <section className="result-panel" aria-label="Kết quả phân loại">
      <div className="panel-heading">
        <h2>Kết quả</h2>
        {result && <span>{result.model_status === 'trained' ? 'Model thật' : 'Demo fallback'}</span>}
      </div>

      {loading && <div className="status-box neutral">Đang gửi nội dung email đến backend...</div>}

      {error && <div className="status-box danger">{error}</div>}

      {!loading && !error && !result && (
        <div className="empty-state">
          <div className="empty-icon">✉</div>
          <p>Kết quả sẽ hiển thị tại đây sau khi kiểm tra.</p>
        </div>
      )}

      {result && (
        <div className={`prediction-card ${isSpam ? 'spam' : 'ham'}`}>
          <span className="badge">{isSpam ? 'Spam' : 'Không spam'}</span>
          <strong>{confidence}%</strong>
          <p>{result.message}</p>
          <div className="meter" aria-label={`Độ tin cậy ${confidence}%`}>
            <span style={{ width: `${confidence}%` }} />
          </div>
        </div>
      )}
    </section>
  );
}

export default ResultCard;
