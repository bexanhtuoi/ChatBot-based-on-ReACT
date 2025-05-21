import { useState, useRef, useEffect } from 'react';
import { Container, Row, Col, Form, Button, Card, InputGroup, Spinner } from 'react-bootstrap';
import { BsRobot, BsPersonCircle } from 'react-icons/bs';
import './App.css';

function ChatMessage({ message, isLoading }) {
  const isUser = message.role === 'user';
  return (
    <div className={`d-flex mb-3 ${isUser ? 'justify-content-end' : 'justify-content-start'} align-items-end`}>
      {!isUser && (
        <span className="me-2 align-self-end ai-avatar" style={{ fontSize: 38, marginBottom: 0 }}>
          <BsRobot color='white' className={isLoading ? 'ai-typing-spin' : ''} />
        </span>
      )}
      <Card
        bg={isUser ? 'primary' : undefined}
        text={isUser ? 'white' : 'white'}
        style={{
          maxWidth: isUser ? '60%' : '100%',
          minWidth: 0,
          background: isUser ? '#23232b' : '#18181a',
          border: isUser ? '1px solid #333' : 'none',
          boxShadow: 'none',
          marginLeft: !isUser ? 0 : undefined,
          marginRight: isUser ? 0 : undefined,
          wordBreak: 'break-word',
          overflowWrap: 'break-word',
          padding: '0.5rem 1rem',
        }}
        className={isUser ? 'ms-auto' : ''}
      >
        <Card.Body style={{ whiteSpace: 'pre-line', padding: '0', display: 'flex', alignItems: 'center' }}>
          <Card.Text style={{ marginBottom: 0, wordBreak: 'break-word', overflowWrap: 'break-word', flex: 1 }}>{message.content}</Card.Text>
          {isLoading && !isUser && (
            <Spinner animation="border" size="sm" className="ms-2" style={{ color: '#4f8cff' }} />
          )}
        </Card.Body>
      </Card>
      {isUser && (
        <span className="ms-2 align-self-end" style={{ fontSize: 28, marginBottom: 0 }}><BsPersonCircle color='white' /></span>
      )}
    </div>
  );
}

function App() {
  const [messages, setMessages] = useState([
    { role: 'assistant', content: 'Xin chào! Tôi có thể giúp gì cho bạn hôm nay?' }
  ]);
  const [input, setInput] = useState('');
  const [isAITyping, setIsAITyping] = useState(false);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim() || isAITyping) return;
    const userMessage = { role: 'user', content: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsAITyping(true);

    try {
      // Gửi POST lên backend
      await fetch('http://localhost:8000/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams({ chat: input })
      });
      // Fetch kết quả trả về từ backend
      const res = await fetch('http://localhost:8000/api/response');
      const data = await res.json();
      setMessages((prev) => [
        ...prev,
        { role: 'assistant', content: data.data.output || 'Không nhận được phản hồi từ AI.' }
      ]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { role: 'assistant', content: 'Opps!! Somethings wrong :))' }
      ]);
    } finally {
      setIsAITyping(false);
    }
  };

  const lastMsgIdx = messages.length - 1;

  return (
    <>
      { }
      <div
        className="brand-header"
      >
        <BsRobot color="#4f8cff" size={33} style={{ marginRight: 10 }} />
        <span style={{ color: '#fff', fontWeight: 700, fontSize: 18, letterSpacing: 1 }}>AI ChatBot</span>
      </div>
      <Container className="main-content" style={{ minHeight: '100vh', width: '100vw', paddingBottom: 90 }}>
        <Row className="flex-grow-1 justify-content-center align-items-center h-100 m-0" style={{ flex: 1 }}>
          <Col
            xs={12}
            md={8}
            lg={7}
            className="d-flex flex-column h-100 p-0"
            style={{ maxWidth: 920, width: '100%' }}
          >
            <Card className="flex-grow-1 mb-3" style={{ background: '#18181a', border: 'none', boxShadow: 'none', borderRadius: 0 }}>
              <Card.Body className="d-flex flex-column justify-content-end p-3">
                {messages.map((msg, idx) => (
                  <ChatMessage key={idx} message={msg} isLoading={isAITyping && idx === lastMsgIdx && msg.role === 'assistant'} />
                ))}
                {isAITyping && (messages[lastMsgIdx]?.role !== 'assistant') && (
                  <div className="d-flex mb-3 justify-content-start align-items-end">
                    <span className="me-2 align-self-end ai-avatar" style={{ fontSize: 38, marginBottom: 0 }}><BsRobot color='white' className="ai-typing-spin" /></span>
                    <Card style={{ background: '#18181a', border: 'none', boxShadow: 'none', padding: '0.5rem 1rem', maxWidth: '100%' }}>
                      <Card.Body style={{ padding: 0, display: 'flex', alignItems: 'center' }}>
                        <Spinner animation="border" size="sm" style={{ color: '#4f8cff' }} />
                        <span className="ms-2" style={{ color: '#aaa' }}>AI đang trả lời...</span>
                      </Card.Body>
                    </Card>
                  </div>
                )}
                <div ref={messagesEndRef} />
              </Card.Body>
            </Card>
          </Col>
        </Row>
      </Container>
      { }
      {!isAITyping && (
        <div style={{ position: 'fixed', left: 0, right: 0, bottom: 0, zIndex: 100, background: '#18181a', padding: '12px 0 12px 0' }}>
          <div style={{ maxWidth: 800, margin: '0 auto', padding: '0 16px' }}>
            <Form onSubmit={handleSend}>
              <InputGroup>
                <Form.Control
                  type="text"
                  placeholder="Nhập tin nhắn..."
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === 'Enter' && !e.shiftKey) handleSend(e);
                  }}
                  autoFocus
                />
                <Button type="submit" variant="primary">
                  Gửi
                </Button>
              </InputGroup>
            </Form>
          </div>
        </div>
      )}
    </>
  );
}

export default App;
