import { useState } from "react";
import axios from "axios";
import "./App.css";

interface Message {
  role: "user" | "assistant";
  content: string;
}

function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const newMessages: Message[] = [...messages, { role: "user", content: input }];
    setMessages(newMessages);
    setInput("");
    setLoading(true);

    try {
      const res = await axios.post("http://localhost:8000/chat", {
        messages: newMessages.map((msg) => ({
          role: msg.role,
          content: msg.content,
        })),
      });

      const reply: Message = {
        role: "assistant",
        content: res.data.reply,
      };

      setMessages([...newMessages, reply]);
    } catch (err) {
      console.error(err);
      setMessages([
        ...newMessages,
        { role: "assistant", content: "⚠️ Something went wrong." },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <h1 className="header">💼 Financial Assistant</h1>
      <div className="chat-window">
        {messages.map((msg, i) => (
          <div key={i} className={`message ${msg.role}`}>
            <strong>{msg.role === "user" ? "You" : "Assistant"}:</strong> {msg.content}
          </div>
        ))}
        {loading && <div className="message assistant">Assistant: typing...</div>}
      </div>
      <div className="input-area">
        <input
          type="text"
          placeholder="Ask about mortgages or product search..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
        />
        <button onClick={sendMessage} disabled={loading}>
          Send
        </button>
      </div>
    </div>
  );
}

export default App;
