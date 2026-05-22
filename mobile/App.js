import { StatusBar } from 'expo-status-bar';
import { SafeAreaView, ScrollView, StyleSheet, Text, View } from 'react-native';
import { useState } from 'react';

import { predictEmail } from './api';
import ResultCard from './components/ResultCard';
import SpamInput from './components/SpamInput';

export default function App() {
  const [text, setText] = useState('');
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  async function handlePredict() {
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
    <SafeAreaView style={styles.safeArea}>
      <StatusBar style="dark" />
      <ScrollView contentContainerStyle={styles.container}>
        <View style={styles.header}>
          <Text style={styles.eyebrow}>D-mail AI Demo</Text>
          <Text style={styles.title}>Phân loại email spam</Text>
          <Text style={styles.subtitle}>Mobile app Expo gọi chung FastAPI backend với web.</Text>
        </View>

        <SpamInput text={text} setText={setText} loading={loading} onSubmit={handlePredict} />
        <ResultCard result={result} error={error} loading={loading} />
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
    backgroundColor: '#f6f8fb',
  },
  container: {
    padding: 18,
    gap: 16,
  },
  header: {
    padding: 22,
    borderRadius: 8,
    backgroundColor: '#0f1f33',
  },
  eyebrow: {
    color: '#5be0b3',
    fontWeight: '700',
    marginBottom: 8,
  },
  title: {
    color: '#ffffff',
    fontSize: 28,
    fontWeight: '800',
    lineHeight: 34,
  },
  subtitle: {
    color: '#c8d4e3',
    lineHeight: 22,
    marginTop: 10,
  },
});
