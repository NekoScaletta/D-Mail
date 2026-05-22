import { ActivityIndicator, Pressable, StyleSheet, Text, TextInput, View } from 'react-native';

export default function SpamInput({ text, setText, loading, onSubmit }) {
  return (
    <View style={styles.panel}>
      <View style={styles.heading}>
        <Text style={styles.title}>Nội dung email</Text>
        <Text style={styles.counter}>{text.trim().length} ký tự</Text>
      </View>

      <TextInput
        value={text}
        onChangeText={setText}
        placeholder="Dán nội dung email cần kiểm tra..."
        multiline
        textAlignVertical="top"
        style={styles.input}
      />

      <Pressable style={[styles.button, loading && styles.buttonDisabled]} onPress={onSubmit} disabled={loading}>
        {loading ? <ActivityIndicator color="#ffffff" /> : <Text style={styles.buttonText}>Kiểm tra</Text>}
      </Pressable>
    </View>
  );
}

const styles = StyleSheet.create({
  panel: {
    padding: 18,
    borderRadius: 8,
    backgroundColor: '#ffffff',
  },
  heading: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 12,
    gap: 12,
  },
  title: {
    color: '#17202a',
    fontSize: 17,
    fontWeight: '800',
  },
  counter: {
    color: '#66788f',
  },
  input: {
    minHeight: 170,
    padding: 14,
    borderWidth: 1,
    borderColor: '#c8d4e3',
    borderRadius: 8,
    color: '#17202a',
    lineHeight: 22,
  },
  button: {
    minHeight: 48,
    alignItems: 'center',
    justifyContent: 'center',
    marginTop: 14,
    borderRadius: 8,
    backgroundColor: '#1f6fd1',
  },
  buttonDisabled: {
    opacity: 0.75,
  },
  buttonText: {
    color: '#ffffff',
    fontWeight: '800',
  },
});
