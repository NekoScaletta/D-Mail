import { useState } from 'react';

import { predictEmail } from './api.js';
import ResultCard from './components/ResultCard.jsx';
import SpamForm from './components/SpamForm.jsx';

const sampleEmails = [
  'Congratulations, you won a free prize. Click now to claim your reward.',
  'Hi team, please review the project report before tomorrow morning.',
];

function App() {
  const [text, setText] = useState('');
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  async function handleSubmit() {
    const value = text.trim();
    if (!value) {
      setError('Vui lòng nhập nội dung email cần kiểm tra.');
      setResult(null);
      return;
    }

    setLoading(true);
    setError('');
    setResult(null);

    try {
      const prediction = await predictEmail(value);
      setResult(prediction);
    } catch (err) {
      setError(err.message || 'Không thể kết nối backend.');
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="page-shell">
      <section className="hero-panel">
        <div className="hero-copy">
          <p className="eyebrow">D-mail AI Demo</p>
          <h1>Phân loại email spam cho web và mobile</h1>
          <p className="subtitle">
            Nhập nội dung email, hệ thống gọi FastAPI backend và trả về nhãn dự đoán kèm độ tin cậy.
          </p>
        </div>
        <div className="signal-visual" aria-hidden="true">
          <span className="signal-line strong" />
          <span className="signal-line" />
          <span className="signal-line muted" />
          <span className="mail-chip">AI</span>
        </div>
      </section>

      <section className="workspace">
        <SpamForm
          text={text}
          setText={setText}
          loading={loading}
          onSubmit={handleSubmit}
          onUseSample={(sample) => {
            setText(sample);
            setError('');
            setResult(null);
          }}
          sampleEmails={sampleEmails}
        />

        <ResultCard result={result} error={error} loading={loading} />
      </section>
    </main>
  );
}

export default App;
