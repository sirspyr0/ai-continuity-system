# Android Mobile Integration Guide

## Overview

The Android mobile component provides a mobile interface for the orchestrator system with on-device AI capabilities and fallback to desktop/VPS when needed.

## Architecture

### Components
1. **React Native/Expo App** - Mobile UI
2. **On-device Model** - Small quantized model (1-3B parameters)
3. **Sync Agent** - Background synchronization with desktop/VPS
4. **Local Storage** - SQLite or AsyncStorage for conversations

### Model Options for Android

#### Option 1: llama.cpp with Android NDK
- Lightweight C++ inference
- Excellent performance on ARM
- Supports GGUF quantized models
- Recommended: Phi-3 Mini 3B or TinyLlama 1.1B

#### Option 2: ONNX Runtime Mobile
- Cross-platform
- Good performance
- Smaller binary size
- Supports quantized ONNX models

#### Option 3: TensorFlow Lite
- Native Android support
- Good optimization
- Requires model conversion to TFLite

### Recommended: llama.cpp Approach

For the Android component, we recommend using llama.cpp with a quantized small model:

1. **Model**: Phi-3 Mini 3B (Q4_K_M quantized) or fine-tuned Mistral 7B (Q4_K_M)
2. **Size**: ~2-4GB depending on quantization
3. **RAM**: Runs well on devices with 6GB+ RAM
4. **Performance**: 5-10 tokens/sec on modern Android devices

## Implementation

### 1. Setup React Native/Expo Project

```bash
npx create-expo-app assistant-mobile
cd assistant-mobile
```

### 2. Install Dependencies

```json
{
  "dependencies": {
    "expo": "~49.0.0",
    "react": "18.2.0",
    "react-native": "0.72.0",
    "@react-native-async-storage/async-storage": "^1.19.0",
    "expo-sqlite": "~11.3.0",
    "react-native-llama": "^0.2.0"
  }
}
```

### 3. Model Integration

See `MobileOrchestrator.tsx` for React Native component that:
- Loads on-device model
- Handles inference
- Falls back to desktop/VPS API
- Syncs conversation history

### 4. Desktop Fallback

When on-device model can't handle request:
1. Check if on same LAN as desktop
2. Send request to desktop API (orchestrator-app)
3. If desktop unavailable, try VPS
4. Cache responses for offline access

## Deployment

### Converting Model for Mobile

```bash
# Convert fine-tuned Mistral to GGUF format
python convert_to_gguf.py \
    --model ./models/mistral-7b-continuity \
    --output ./models/mistral-7b-continuity.gguf

# Quantize to Q4_K_M (recommended for mobile)
./llama.cpp/quantize \
    ./models/mistral-7b-continuity.gguf \
    ./models/mistral-7b-continuity-q4.gguf \
    Q4_K_M
```

### Bundling Model with App

**For Development:**
```typescript
// In App.tsx
import * as FileSystem from 'expo-file-system';

const MODEL_URL = 'http://your-server.com/models/mistral-7b-continuity-q4.gguf';
const MODEL_PATH = `${FileSystem.documentDirectory}model.gguf`;

async function downloadModel() {
  const { exists } = await FileSystem.getInfoAsync(MODEL_PATH);
  if (!exists) {
    await FileSystem.downloadAsync(MODEL_URL, MODEL_PATH);
  }
}
```

**For Production:**
- Bundle small model (~2GB) with app
- Download larger models on first run
- Use Android asset delivery for large files

## Performance Optimization

### 1. Model Size vs Performance

| Model | Size | RAM | Speed | Quality |
|-------|------|-----|-------|---------|
| TinyLlama 1.1B Q4 | ~700MB | 2GB | Fast | Basic |
| Phi-3 Mini 3B Q4 | ~2GB | 4GB | Medium | Good |
| Mistral 7B Q4 | ~4GB | 8GB | Slow | Excellent |

### 2. Memory Management

```typescript
// Free memory after inference
await model.unload();

// Load only when needed
await model.load();
```

### 3. Background Processing

```typescript
// Use React Native background tasks
import BackgroundFetch from 'react-native-background-fetch';

BackgroundFetch.configure({
  minimumFetchInterval: 15, // minutes
}, async (taskId) => {
  // Sync with desktop
  await syncConversations();
  BackgroundFetch.finish(taskId);
});
```

## Sync Strategy

### LAN-First Sync

```typescript
// Check if desktop is available on LAN
async function checkDesktopAvailability(): Promise<boolean> {
  try {
    const response = await fetch('http://192.168.1.x:5000/health', {
      timeout: 1000,
    });
    return response.ok;
  } catch {
    return false;
  }
}

// Sync with desktop
async function syncWithDesktop() {
  const conversations = await getLocalConversations();
  
  const response = await fetch('http://desktop-ip:5000/sync', {
    method: 'POST',
    body: JSON.stringify({ conversations }),
  });
  
  const { updated } = await response.json();
  await updateLocalConversations(updated);
}
```

### Conflict Resolution

Use last-write-wins or vector clocks:

```typescript
interface Message {
  id: string;
  content: string;
  timestamp: number;
  device: 'mobile' | 'desktop' | 'vps';
}

function mergeConversations(local: Message[], remote: Message[]): Message[] {
  const merged = new Map<string, Message>();
  
  for (const msg of [...local, ...remote]) {
    const existing = merged.get(msg.id);
    if (!existing || msg.timestamp > existing.timestamp) {
      merged.set(msg.id, msg);
    }
  }
  
  return Array.from(merged.values()).sort((a, b) => a.timestamp - b.timestamp);
}
```

## Security Considerations

1. **API Authentication**: Use tokens for desktop/VPS API
2. **Encrypted Storage**: Encrypt sensitive conversations
3. **HTTPS Only**: Use HTTPS for remote connections
4. **Model Integrity**: Verify model checksums

## Testing

```bash
# Run on Android emulator
npx expo run:android

# Run on device
npx expo run:android --device
```

## References

- [llama.cpp](https://github.com/ggerganov/llama.cpp)
- [react-native-llama](https://github.com/mybigday/react-native-llama)
- [Expo Documentation](https://docs.expo.dev/)
