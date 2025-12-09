/**
 * MobileOrchestrator.tsx
 * 
 * React Native component for mobile AI orchestration
 * Handles on-device inference with fallback to desktop/VPS
 */

import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  TextInput,
  ScrollView,
  TouchableOpacity,
  ActivityIndicator,
  StyleSheet,
} from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { initLlama, LlamaContext } from 'react-native-llama';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: number;
  source: 'local' | 'desktop' | 'vps';
}

interface OrchestratorConfig {
  modelPath: string;
  desktopApiUrl?: string;
  vpsApiUrl?: string;
  maxHistoryTurns: number;
}

export const MobileOrchestrator: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [modelLoaded, setModelLoaded] = useState(false);
  const [context, setContext] = useState<LlamaContext | null>(null);
  
  const config: OrchestratorConfig = {
    modelPath: 'file:///path/to/model.gguf',
    desktopApiUrl: 'http://192.168.1.100:5000',
    vpsApiUrl: 'https://vps.example.com',
    maxHistoryTurns: 12,
  };

  useEffect(() => {
    loadModel();
    loadConversationHistory();
  }, []);

  const loadModel = async () => {
    try {
      console.log('Loading model...');
      const llamaContext = await initLlama({
        model: config.modelPath,
        n_ctx: 2048,
        n_batch: 512,
      });
      setContext(llamaContext);
      setModelLoaded(true);
      console.log('Model loaded successfully');
    } catch (error) {
      console.error('Failed to load model:', error);
      setModelLoaded(false);
    }
  };

  const loadConversationHistory = async () => {
    try {
      const history = await AsyncStorage.getItem('conversation_history');
      if (history) {
        setMessages(JSON.parse(history));
      }
    } catch (error) {
      console.error('Failed to load history:', error);
    }
  };

  const saveConversationHistory = async (msgs: Message[]) => {
    try {
      await AsyncStorage.setItem('conversation_history', JSON.stringify(msgs));
    } catch (error) {
      console.error('Failed to save history:', error);
    }
  };

  const formatPrompt = (userMessage: string): string => {
    const systemPrompt = `You are an AI assistant trained in continuity theory. 
You maintain context across instances and understand the orchestrator ecosystem.`;
    
    // Get recent history
    const recentMessages = messages.slice(-config.maxHistoryTurns);
    
    let prompt = `<s>[INST] ${systemPrompt}\n\n`;
    
    for (const msg of recentMessages) {
      if (msg.role === 'user') {
        prompt += `${msg.content}`;
      } else {
        prompt += `[/INST] ${msg.content}</s><s>[INST]`;
      }
    }
    
    prompt += `${userMessage}[/INST]`;
    
    return prompt;
  };

  const generateLocalResponse = async (userMessage: string): Promise<string | null> => {
    if (!context || !modelLoaded) {
      return null;
    }

    try {
      const prompt = formatPrompt(userMessage);
      
      const response = await context.completion({
        prompt,
        n_predict: 512,
        temperature: 0.7,
        top_p: 0.95,
        stop: ['</s>', '[INST]'],
      });

      return response.text.trim();
    } catch (error) {
      console.error('Local inference failed:', error);
      return null;
    }
  };

  const generateDesktopResponse = async (userMessage: string): Promise<string | null> => {
    if (!config.desktopApiUrl) return null;

    try {
      const response = await fetch(`${config.desktopApiUrl}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userMessage }),
        timeout: 5000,
      });

      if (!response.ok) return null;

      const data = await response.json();
      return data.response;
    } catch (error) {
      console.error('Desktop API failed:', error);
      return null;
    }
  };

  const generateVPSResponse = async (userMessage: string): Promise<string | null> => {
    if (!config.vpsApiUrl) return null;

    try {
      const prompt = formatPrompt(userMessage);
      
      const response = await fetch(`${config.vpsApiUrl}/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt }),
        timeout: 10000,
      });

      if (!response.ok) return null;

      const data = await response.json();
      return data.response;
    } catch (error) {
      console.error('VPS API failed:', error);
      return null;
    }
  };

  const handleSend = async () => {
    if (!input.trim() || loading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: input.trim(),
      timestamp: Date.now(),
      source: 'local',
    };

    const newMessages = [...messages, userMessage];
    setMessages(newMessages);
    setInput('');
    setLoading(true);

    try {
      // Try local inference first
      let response = await generateLocalResponse(userMessage.content);
      let source: 'local' | 'desktop' | 'vps' = 'local';

      // Fallback to desktop
      if (!response) {
        response = await generateDesktopResponse(userMessage.content);
        source = 'desktop';
      }

      // Fallback to VPS
      if (!response) {
        response = await generateVPSResponse(userMessage.content);
        source = 'vps';
      }

      if (!response) {
        throw new Error('All inference methods failed');
      }

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: response,
        timestamp: Date.now(),
        source,
      };

      const updatedMessages = [...newMessages, assistantMessage];
      setMessages(updatedMessages);
      await saveConversationHistory(updatedMessages);
    } catch (error) {
      console.error('Failed to generate response:', error);
      // Show error message
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: Date.now(),
        source: 'local',
      };
      const updatedMessages = [...newMessages, errorMessage];
      setMessages(updatedMessages);
    } finally {
      setLoading(false);
    }
  };

  const clearConversation = async () => {
    setMessages([]);
    await AsyncStorage.removeItem('conversation_history');
  };

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.headerText}>Orchestrator Assistant</Text>
        <Text style={styles.statusText}>
          {modelLoaded ? '🟢 Model Loaded' : '🔴 Model Not Loaded'}
        </Text>
        <TouchableOpacity onPress={clearConversation} style={styles.clearButton}>
          <Text style={styles.clearButtonText}>Clear</Text>
        </TouchableOpacity>
      </View>

      <ScrollView style={styles.messagesContainer}>
        {messages.map((msg) => (
          <View
            key={msg.id}
            style={[
              styles.message,
              msg.role === 'user' ? styles.userMessage : styles.assistantMessage,
            ]}
          >
            <Text style={styles.messageText}>{msg.content}</Text>
            <Text style={styles.messageSource}>
              {msg.role} · {msg.source}
            </Text>
          </View>
        ))}
        {loading && (
          <View style={styles.loadingContainer}>
            <ActivityIndicator size="small" color="#007AFF" />
            <Text style={styles.loadingText}>Thinking...</Text>
          </View>
        )}
      </ScrollView>

      <View style={styles.inputContainer}>
        <TextInput
          style={styles.input}
          value={input}
          onChangeText={setInput}
          placeholder="Type your message..."
          multiline
          editable={!loading}
        />
        <TouchableOpacity
          style={[styles.sendButton, loading && styles.sendButtonDisabled]}
          onPress={handleSend}
          disabled={loading}
        >
          <Text style={styles.sendButtonText}>Send</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  header: {
    padding: 16,
    backgroundColor: '#fff',
    borderBottomWidth: 1,
    borderBottomColor: '#ddd',
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
  },
  headerText: {
    fontSize: 18,
    fontWeight: 'bold',
  },
  statusText: {
    fontSize: 12,
    color: '#666',
  },
  clearButton: {
    padding: 8,
    backgroundColor: '#ff3b30',
    borderRadius: 4,
  },
  clearButtonText: {
    color: '#fff',
    fontSize: 12,
  },
  messagesContainer: {
    flex: 1,
    padding: 16,
  },
  message: {
    marginBottom: 12,
    padding: 12,
    borderRadius: 8,
    maxWidth: '80%',
  },
  userMessage: {
    backgroundColor: '#007AFF',
    alignSelf: 'flex-end',
  },
  assistantMessage: {
    backgroundColor: '#fff',
    alignSelf: 'flex-start',
  },
  messageText: {
    fontSize: 16,
    color: '#000',
  },
  messageSource: {
    fontSize: 10,
    color: '#666',
    marginTop: 4,
  },
  loadingContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 12,
  },
  loadingText: {
    marginLeft: 8,
    color: '#666',
  },
  inputContainer: {
    flexDirection: 'row',
    padding: 16,
    backgroundColor: '#fff',
    borderTopWidth: 1,
    borderTopColor: '#ddd',
  },
  input: {
    flex: 1,
    padding: 12,
    backgroundColor: '#f5f5f5',
    borderRadius: 8,
    marginRight: 8,
    maxHeight: 100,
  },
  sendButton: {
    padding: 12,
    backgroundColor: '#007AFF',
    borderRadius: 8,
    justifyContent: 'center',
  },
  sendButtonDisabled: {
    backgroundColor: '#ccc',
  },
  sendButtonText: {
    color: '#fff',
    fontWeight: 'bold',
  },
});
