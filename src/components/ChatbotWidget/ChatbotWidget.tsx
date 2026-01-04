// import React, { useState, useEffect, useRef } from 'react';
// import styles from './ChatbotWidget.module.css';
// import { IoChatbubbleEllipsesOutline, IoSend, IoClose, IoTrashOutline, IoAttach, IoPersonCircle } from 'react-icons/io5';
// import { RiRobotLine } from 'react-icons/ri';

// interface Message {
//   id: number | 'loading';
//   text: string;
//   sender: 'user' | 'bot';
//   timestamp: Date;
//   sources?: string[];
//   isLoading?: boolean;
// }

// interface ChatRequest {
//   message: string;
//   selected_text: string | null;
// }

// interface ChatResponse {
//   response: string;
//   conversation_id: string;
//   sources: string[];
// }

// const ChatbotWidget: React.FC = () => {
//   const [isOpen, setIsOpen] = useState(false);
//   const [messages, setMessages] = useState<Message[]>([]);
//   const [inputValue, setInputValue] = useState('');
//   const [isLoading, setIsLoading] = useState(false);
//   const [selectedText, setSelectedText] = useState('');
//   const [attachedText, setAttachedText] = useState('');
//   const [showSelectionPopup, setShowSelectionPopup] = useState(false);
//   const [popupPosition, setPopupPosition] = useState({ x: 0, y: 0 });
//   const [wsConnected, setWsConnected] = useState(false);
//   const [isTyping, setIsTyping] = useState(false);

//   const messagesEndRef = useRef<HTMLDivElement>(null);
//   const inputRef = useRef<HTMLTextAreaElement>(null);
//   const wsRef = useRef<WebSocket | null>(null);
//   const reconnectTimeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);
//   const conversationIdRef = useRef<string>(crypto.randomUUID());

//   // Format time
//   const formatTime = (date: Date) => {
//     return date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
//   };

//   // Capture selected text from the page with popup confirmation
//   useEffect(() => {
//     const handleSelection = () => {
//       setTimeout(() => {
//         const selection = window.getSelection();
//         if (selection && selection.toString().trim().length > 10) {
//           const text = selection.toString().trim();
//           const range = selection.getRangeAt(0);
//           const rect = range.getBoundingClientRect();

//           setSelectedText(text);
//           setPopupPosition({
//             x: rect.left + rect.width / 2,
//             y: rect.top - 50
//           });
//           setShowSelectionPopup(true);
//         } else {
//           setShowSelectionPopup(false);
//         }
//       }, 10);
//     };

//     const handleClickOutside = (e: MouseEvent) => {
//       const target = e.target as HTMLElement;
//       if (!target.closest(`.${styles.selectionPopup}`)) {
//         setShowSelectionPopup(false);
//       }
//     };

//     document.addEventListener('mouseup', handleSelection);
//     document.addEventListener('click', handleClickOutside);

//     return () => {
//       document.removeEventListener('mouseup', handleSelection);
//       document.removeEventListener('click', handleClickOutside);
//     };
//   }, []);

//   // WebSocket connection
//   useEffect(() => {
//     const connectWebSocket = () => {
//       const WS_PROTOCOL = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
//       const WS_HOST = window.location.hostname;
//       const WS_PORT = '8000';
//       const WS_URL = `${WS_PROTOCOL}//${WS_HOST}:${WS_PORT}/ws`;

//       try {
//         wsRef.current = new WebSocket(WS_URL);

//         wsRef.current.onopen = () => {
//           console.log('WebSocket connected');
//           setWsConnected(true);
//           wsRef.current?.send(JSON.stringify({ type: 'ping', content: 'hello' }));
//         };

//         wsRef.current.onmessage = (event) => {
//           try {
//             const data = JSON.parse(event.data);
//             if (data.type === 'chat_response') {
//               setIsTyping(false);
//               const botMessage: Message = {
//                 id: Date.now() + 1,
//                 text: data.content,
//                 sender: 'bot',
//                 timestamp: new Date(),
//                 sources: data.sources || [],
//               };
//               setMessages(prev => {
//                 const newMessages = [...prev];
//                 const loadingIndex = newMessages.findIndex(msg => msg.id === 'loading');
//                 if (loadingIndex !== -1) newMessages[loadingIndex] = botMessage;
//                 else newMessages.push(botMessage);
//                 return newMessages;
//               });
//               setIsLoading(false);
//             } else if (data.type === 'pong') {
//               console.log('Received pong from server');
//             } else if (data.type === 'error') {
//               setIsTyping(false);
//               const errorMessage: Message = {
//                 id: Date.now() + 1,
//                 text: data.content,
//                 sender: 'bot',
//                 timestamp: new Date()
//               };
//               setMessages(prev => {
//                 const newMessages = [...prev];
//                 const loadingIndex = newMessages.findIndex(msg => msg.id === 'loading');
//                 if (loadingIndex !== -1) newMessages[loadingIndex] = errorMessage;
//                 else newMessages.push(errorMessage);
//                 return newMessages;
//               });
//               setIsLoading(false);
//             }
//           } catch (error) {
//             console.error('Error parsing WebSocket message:', error);
//           }
//         };

//         wsRef.current.onclose = () => {
//           console.log('WebSocket disconnected');
//           setWsConnected(false);
//           if (reconnectTimeoutRef.current) clearTimeout(reconnectTimeoutRef.current);
//           reconnectTimeoutRef.current = setTimeout(connectWebSocket, 3000);
//         };

//         wsRef.current.onerror = (error) => {
//           console.error('WebSocket error:', error);
//           setWsConnected(false);
//         };
//       } catch (error) {
//         console.error('Failed to create WebSocket connection:', error);
//         setWsConnected(false);
//         if (reconnectTimeoutRef.current) clearTimeout(reconnectTimeoutRef.current);
//         reconnectTimeoutRef.current = setTimeout(connectWebSocket, 3000);
//       }
//     };

//     connectWebSocket();

//     return () => {
//       if (wsRef.current) wsRef.current.close();
//       if (reconnectTimeoutRef.current) clearTimeout(reconnectTimeoutRef.current);
//     };
//   }, []);

//   const scrollToBottom = () => messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
//   useEffect(() => scrollToBottom(), [messages]);

//   const toggleChat = () => {
//     setIsOpen(!isOpen);
//     if (!isOpen) {
//       setTimeout(() => inputRef.current?.focus(), 100);
//     }
//   };

//   // Handle text attachment confirmation
//   const handleAttachText = () => {
//     setAttachedText(selectedText);
//     setShowSelectionPopup(false);
//     setSelectedText('');
//     if (!isOpen) {
//       setIsOpen(true);
//     }
//     setTimeout(() => inputRef.current?.focus(), 100);
//   };

//   // Remove attached text
//   const removeAttachedText = () => {
//     setAttachedText('');
//   };

//   const sendMessage = async () => {
//     if (!inputValue.trim() || isLoading) return;

//     const userMessage: Message = {
//       id: Date.now(),
//       text: inputValue,
//       sender: 'user',
//       timestamp: new Date()
//     };

//     setMessages(prev => [...prev, userMessage]);
//     const messageToSend = inputValue;
//     const contextText = attachedText;
//     setInputValue('');
//     setAttachedText('');
//     setIsLoading(true);
//     setIsTyping(true);

//     if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
//       wsRef.current.send(JSON.stringify({
//         type: "chat",
//         content: messageToSend,
//         selected_text: contextText || null,
//         conversation_id: conversationIdRef.current
//       }));
//     } else {
//       try {
//         const BACKEND_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
//           ? 'http://localhost:8000'
//           : 'https://areebahammad-rag-chatbot.hf.space/api/chatbot/chat';
//         const timeoutPromise = new Promise((_, reject) => setTimeout(() => reject(new Error('Request timeout')), 60000));
//         const fetchPromise = fetch(`${BACKEND_URL}/api/chatbot/chat`, {
//           method: 'POST',
//           headers: { 'Content-Type': 'application/json' },
//           body: JSON.stringify({ message: messageToSend, selected_text: contextText || null })
//         });
//         const response = await Promise.race([fetchPromise, timeoutPromise]) as Response;
//         if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
//         const data: ChatResponse = await response.json();
//         setIsTyping(false);
//         const botMessage: Message = {
//           id: Date.now() + 1,
//           text: data.response,
//           sender: 'bot',
//           timestamp: new Date(),
//           sources: data.sources || []
//         };
//         setMessages(prev => [...prev, botMessage]);
//       } catch (error: any) {
//         console.error('Error sending message:', error);
//         setIsTyping(false);
//         const errorMessage: Message = {
//           id: Date.now() + 1,
//           text: error.message || 'Error',
//           sender: 'bot',
//           timestamp: new Date()
//         };
//         setMessages(prev => [...prev, errorMessage]);
//       } finally {
//         setIsLoading(false);
//       }
//     }
//   };

//   const handleKeyPress = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
//     if (e.key === 'Enter' && !e.shiftKey) {
//       e.preventDefault();
//       sendMessage();
//     }
//   };

//   const clearChat = () => {
//     setMessages([]);
//     setAttachedText('');
//     setInputValue('');
//   };

//   return (
//     <>
//       {/* Selection Popup */}
//       {showSelectionPopup && (
//         <div
//           className={styles.selectionPopup}
//           style={{
//             left: `${popupPosition.x}px`,
//             top: `${popupPosition.y}px`,
//           }}
//         >
//           <button onClick={handleAttachText} className={styles.attachButton}>
//             <IoAttach size={16} />
//             Attach to chat
//           </button>
//         </div>
//       )}

//       {/* Float Button */}
//       {!isOpen && (
//         <button
//           className={styles.floatButton}
//           onClick={toggleChat}
//           aria-label="Open chat"
//         >
//           <IoChatbubbleEllipsesOutline size={28} />
//         </button>
//       )}

//       {/* Chat Widget */}
//       {isOpen && (
//         <div className={styles.chatWidget}>
//           {/* Header */}
//           <div className={styles.header}>
//             <div className={styles.headerLeft}>
//               <div className={styles.botAvatar}>
//                 <RiRobotLine size={26} />
//               </div>
//               <div className={styles.headerInfo}>
//                 <h3>Physical AI Assistant</h3>
//                 <span className={styles.status}>
//                   <span className={`${styles.statusDot} ${wsConnected ? styles.connected : styles.disconnected}`}></span>
//                   {wsConnected ? 'Online' : 'Offline'}
//                 </span>
//               </div>
//             </div>
//             <div className={styles.headerActions}>
//               <button onClick={clearChat} title="Clear chat" className={styles.iconBtn}>
//                 <IoTrashOutline size={18} />
//               </button>
//               <button onClick={toggleChat} title="Close" className={styles.iconBtn}>
//                 <IoClose size={20} />
//               </button>
//             </div>
//           </div>

//           {/* Messages */}
//           <div className={styles.messagesContainer}>
//             {messages.length === 0 ? (
//               <div className={styles.welcomeMessage}>
//                 <div className={styles.welcomeIcon}>
//                   <IoChatbubbleEllipsesOutline size={48} />
//                 </div>
//                 <h4>Welcome to Physical AI Assistant</h4>
//                 <p>Ask me anything about the textbook content. Select text from the page and attach it to your questions.</p>
//               </div>
//             ) : (
//               messages.map(msg => (
//                 <div key={msg.id} className={`${styles.messageWrapper} ${styles[msg.sender]}`}>
//                   <div className={styles.messageContent}>
//                     <div className={styles.messageAvatar}>
//                       {msg.sender === 'bot' ? (
//                         <RiRobotLine size={20} />
//                       ) : (
//                         <IoPersonCircle size={20} />
//                       )}
//                     </div>
//                     <div className={styles.messageBubble}>
//                       <div className={styles.messageText}>{msg.text}</div>
//                       {msg.sources && msg.sources.length > 0 && (
//                         <div className={styles.messageSources}>
//                           <span>Sources: {msg.sources.slice(0, 3).join(', ')}</span>
//                         </div>
//                       )}
//                       <div className={styles.messageTime}>{formatTime(msg.timestamp)}</div>
//                     </div>
//                   </div>
//                 </div>
//               ))
//             )}

//             {/* Typing Indicator */}
//             {isTyping && (
//               <div className={`${styles.messageWrapper} ${styles.bot}`}>
//                 <div className={styles.messageContent}>
//                   <div className={styles.messageAvatar}>
//                     <RiRobotLine size={20} />
//                   </div>
//                   <div className={styles.typingIndicator}>
//                     <span></span>
//                     <span></span>
//                     <span></span>
//                   </div>
//                 </div>
//               </div>
//             )}

//             <div ref={messagesEndRef} />
//           </div>

//           {/* Attached Text Box */}
//           {attachedText && (
//             <div className={styles.attachedTextBox}>
//               <div className={styles.attachedTextLabel}>
//                 <IoAttach size={14} />
//                 Attached Context
//               </div>
//               <div className={styles.attachedTextContent}>
//                 "{attachedText.substring(0, 100)}{attachedText.length > 100 ? '...' : ''}"
//               </div>
//               <button onClick={removeAttachedText} className={styles.removeAttached}>
//                 <IoClose size={14} />
//               </button>
//             </div>
//           )}

//           {/* Input Area */}
//           <div className={styles.inputArea}>
//             <textarea
//               ref={inputRef}
//               value={inputValue}
//               onChange={e => setInputValue(e.target.value)}
//               onKeyDown={handleKeyPress}
//               placeholder="Type your message..."
//               className={styles.input}
//               rows={1}
//             />
//             <button
//               onClick={sendMessage}
//               disabled={!inputValue.trim() || isLoading}
//               className={styles.sendButton}
//               aria-label="Send message"
//             >
//               <IoSend size={20} />
//             </button>
//           </div>
//         </div>
//       )}
//     </>
//   );
// };

// export default ChatbotWidget;

import React, { useState, useEffect, useRef } from 'react';
import styles from './ChatbotWidget.module.css';
import { IoChatbubbleEllipsesOutline, IoSend, IoClose, IoTrashOutline, IoAttach, IoPersonCircle } from 'react-icons/io5';
import { RiRobotLine } from 'react-icons/ri';

interface Message {
  id: number;
  text: string;
  sender: 'user' | 'bot';
  timestamp: Date;
  sources?: string[];
  isLoading?: boolean;
}

interface ChatResponse {
  response: string;
  conversation_id: string;
  sources: string[];
}

const ChatbotWidget: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [selectedText, setSelectedText] = useState('');
  const [attachedText, setAttachedText] = useState('');
  const [showSelectionPopup, setShowSelectionPopup] = useState(false);
  const [popupPosition, setPopupPosition] = useState({ x: 0, y: 0 });
  const [isTyping, setIsTyping] = useState(false);

  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);
  const conversationIdRef = useRef<string>(crypto.randomUUID());

  // Format time
  const formatTime = (date: Date) => {
    return date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
  };

  // Capture selected text from the page with popup confirmation
  useEffect(() => {
    const handleSelection = () => {
      setTimeout(() => {
        const selection = window.getSelection();
        if (selection && selection.toString().trim().length > 10) {
          const text = selection.toString().trim();
          const range = selection.getRangeAt(0);
          const rect = range.getBoundingClientRect();

          setSelectedText(text);
          setPopupPosition({
            x: rect.left + rect.width / 2,
            y: rect.top - 50
          });
          setShowSelectionPopup(true);
        } else {
          setShowSelectionPopup(false);
        }
      }, 10);
    };

    const handleClickOutside = (e: MouseEvent) => {
      const target = e.target as HTMLElement;
      if (!target.closest(`.${styles.selectionPopup}`)) {
        setShowSelectionPopup(false);
      }
    };

    document.addEventListener('mouseup', handleSelection);
    document.addEventListener('click', handleClickOutside);

    return () => {
      document.removeEventListener('mouseup', handleSelection);
      document.removeEventListener('click', handleClickOutside);
    };
  }, []);

  const scrollToBottom = () => messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  useEffect(() => scrollToBottom(), [messages]);

  const toggleChat = () => {
    setIsOpen(!isOpen);
    if (!isOpen) setTimeout(() => inputRef.current?.focus(), 100);
  };

  const handleAttachText = () => {
    setAttachedText(selectedText);
    setShowSelectionPopup(false);
    setSelectedText('');
    if (!isOpen) setIsOpen(true);
    setTimeout(() => inputRef.current?.focus(), 100);
  };

  const removeAttachedText = () => setAttachedText('');

  // ---- REST API messaging ----
  const sendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now(),
      text: inputValue,
      sender: 'user',
      timestamp: new Date()
    };
    setMessages(prev => [...prev, userMessage]);

    const messageToSend = inputValue;
    const contextText = attachedText;
    setInputValue('');
    setAttachedText('');
    setIsLoading(true);
    setIsTyping(true);

    try {
      const BACKEND_URL =
        window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
          ? 'http://localhost:8000'
          : 'https://areebahammad-rag-chatbot.hf.space'; // Hugging Face backend

      const timeoutPromise = new Promise((_, reject) => setTimeout(() => reject(new Error('Request timeout')), 60000));
      const fetchPromise = fetch(`${BACKEND_URL}/api/chatbot/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: messageToSend, selected_text: contextText || null })
      });
      const response = await Promise.race([fetchPromise, timeoutPromise]) as Response;
      if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

      const data: ChatResponse = await response.json();
      setIsTyping(false);
      const botMessage: Message = {
        id: Date.now() + 1,
        text: data.response,
        sender: 'bot',
        timestamp: new Date(),
        sources: data.sources || []
      };
      setMessages(prev => [...prev, botMessage]);
    } catch (error: any) {
      console.error('Error sending message:', error);
      setIsTyping(false);
      const errorMessage: Message = {
        id: Date.now() + 1,
        text: error.message || 'Error',
        sender: 'bot',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const clearChat = () => {
    setMessages([]);
    setAttachedText('');
    setInputValue('');
  };

  return (
    <>
      {showSelectionPopup && (
        <div
          className={styles.selectionPopup}
          style={{ left: `${popupPosition.x}px`, top: `${popupPosition.y}px` }}
        >
          <button onClick={handleAttachText} className={styles.attachButton}>
            <IoAttach size={16} /> Attach to chat
          </button>
        </div>
      )}

      {!isOpen && (
        <button className={styles.floatButton} onClick={toggleChat} aria-label="Open chat">
          <IoChatbubbleEllipsesOutline size={28} />
        </button>
      )}

      {isOpen && (
        <div className={styles.chatWidget}>
          {/* Header */}
          <div className={styles.header}>
            <div className={styles.headerLeft}>
              <div className={styles.botAvatar}><RiRobotLine size={26} /></div>
              <div className={styles.headerInfo}>
                <h3>Physical AI Assistant</h3>
                <span className={styles.status}>
                  <span className={`${styles.statusDot} ${styles.connected}`}></span>
                  Online
                </span>
              </div>
            </div>
            <div className={styles.headerActions}>
              <button onClick={clearChat} title="Clear chat" className={styles.iconBtn}><IoTrashOutline size={18} /></button>
              <button onClick={toggleChat} title="Close" className={styles.iconBtn}><IoClose size={20} /></button>
            </div>
          </div>

          {/* Messages */}
          <div className={styles.messagesContainer}>
            {messages.length === 0 ? (
              <div className={styles.welcomeMessage}>
                <div className={styles.welcomeIcon}><IoChatbubbleEllipsesOutline size={48} /></div>
                <h4>Welcome to Physical AI Assistant</h4>
                <p>Ask me anything about the textbook content. Select text and attach it to your questions.</p>
              </div>
            ) : (
              messages.map(msg => (
                <div key={msg.id} className={`${styles.messageWrapper} ${styles[msg.sender]}`}>
                  <div className={styles.messageContent}>
                    <div className={styles.messageAvatar}>
                      {msg.sender === 'bot' ? <RiRobotLine size={20} /> : <IoPersonCircle size={20} />}
                    </div>
                    <div className={styles.messageBubble}>
                      <div className={styles.messageText}>{msg.text}</div>
                      {msg.sources && msg.sources.length > 0 && (
                        <div className={styles.messageSources}>
                          <span>Sources: {msg.sources.slice(0, 3).join(', ')}</span>
                        </div>
                      )}
                      <div className={styles.messageTime}>{formatTime(msg.timestamp)}</div>
                    </div>
                  </div>
                </div>
              ))
            )}

            {isTyping && (
              <div className={`${styles.messageWrapper} ${styles.bot}`}>
                <div className={styles.messageContent}>
                  <div className={styles.messageAvatar}><RiRobotLine size={20} /></div>
                  <div className={styles.typingIndicator}><span></span><span></span><span></span></div>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          {/* Attached Text Box */}
          {attachedText && (
            <div className={styles.attachedTextBox}>
              <div className={styles.attachedTextLabel}><IoAttach size={14} /> Attached Context</div>
              <div className={styles.attachedTextContent}>
                "{attachedText.substring(0, 100)}{attachedText.length > 100 ? '...' : ''}"
              </div>
              <button onClick={removeAttachedText} className={styles.removeAttached}><IoClose size={14} /></button>
            </div>
          )}

          {/* Input Area */}
          <div className={styles.inputArea}>
            <textarea
              ref={inputRef}
              value={inputValue}
              onChange={e => setInputValue(e.target.value)}
              onKeyDown={handleKeyPress}
              placeholder="Type your message..."
              className={styles.input}
              rows={1}
            />
            <button
              onClick={sendMessage}
              disabled={!inputValue.trim() || isLoading}
              className={styles.sendButton}
              aria-label="Send message"
            >
              <IoSend size={20} />
            </button>
          </div>
        </div>
      )}
    </>
  );
};

export default ChatbotWidget;
