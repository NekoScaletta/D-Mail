import { StyleSheet, Text, View } from 'react-native';

export default function ResultCard({ result, error, loading }) {
  const isSpam = result?.label === 1;
  const confidence = result ? Math.round(result.confidence * 100) : 0;

  if (loading) {
    return (
      <View style={styles.panel}>
        <Text style={styles.muted}>Đang gửi nội dung email đến backend...</Text>
      </View>
    );
  }

  if (error) {
    return (
      <View style={[styles.panel, styles.errorPanel]}>
        <Text style={styles.errorText}>{error}</Text>
      </View>
    );
  }

  if (!result) {
    return (
      <View style={styles.panel}>
        <Text style={styles.title}>Kết quả</Text>
        <Text style={styles.muted}>Kết quả sẽ hiển thị tại đây sau khi kiểm tra.</Text>
      </View>
    );
  }

  return (
    <View style={[styles.panel, isSpam ? styles.spamPanel : styles.hamPanel]}>
      <View style={styles.row}>
        <Text style={styles.title}>{isSpam ? 'Spam' : 'Không spam'}</Text>
        <Text style={styles.mode}>{result.model_status === 'trained' ? 'Model thật' : 'Demo'}</Text>
      </View>
      <Text style={styles.confidence}>{confidence}%</Text>
      <Text style={styles.muted}>{result.message}</Text>
      <View style={styles.meter}>
        <View style={[styles.meterFill, { width: `${confidence}%` }]} />
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  panel: {
    padding: 18,
    borderRadius: 8,
    backgroundColor: '#ffffff',
  },
  spamPanel: {
    backgroundColor: '#fff5f2',
  },
  hamPanel: {
    backgroundColor: '#f0fbf6',
  },
  errorPanel: {
    backgroundColor: '#fff0f3',
  },
  row: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    gap: 12,
  },
  title: {
    color: '#17202a',
    fontSize: 18,
    fontWeight: '800',
  },
  mode: {
    color: '#66788f',
  },
  confidence: {
    color: '#17202a',
    fontSize: 40,
    fontWeight: '900',
    marginVertical: 10,
  },
  muted: {
    color: '#4f5f73',
    lineHeight: 22,
  },
  errorText: {
    color: '#8a1f2d',
    lineHeight: 22,
  },
  meter: {
    height: 10,
    overflow: 'hidden',
    marginTop: 14,
    borderRadius: 999,
    backgroundColor: 'rgba(23, 32, 42, 0.12)',
  },
  meterFill: {
    height: '100%',
    borderRadius: 999,
    backgroundColor: '#2c7be5',
  },
});
