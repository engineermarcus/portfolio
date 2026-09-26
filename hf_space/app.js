// Knowledge base and conversational logic for Neiman Marcus's Portfolio Agent
const PORTFOLIO_INFO = {
  name: "Neiman Marcus",
  github: "https://github.com/engineermarcus",
  email: "engineermarcus72@gmail.com",
  achievements: [
    { title: "Quickdraw", desc: "Closed issue or PR within 5 minutes of opening." },
    { title: "Pull Shark", desc: "Merged impactful pull requests across production repositories." },
    { title: "YOLO", desc: "Merged PRs directly without code review — decisive execution." }
  ],
  projects: [
    {
      name: "cybernetics & positron",
      lang: "JavaScript / Node.js",
      desc: "Browser-based Linux shell and IDE installed globally via npm, featuring an AI voice assistant, live code editor, and encrypted cloud tunneling."
    },
    {
      name: "moviebox-api (Magpie)",
      lang: "Python / Playwright",
      desc: "Headless media CLI running inside Termux on Android via proot Ubuntu container. Automates headless browser scoring and chunked high-res streaming with Internet Archive sync."
    },
    {
      name: "marcus-enterprises & AM2PM Store",
      lang: "JavaScript / Express",
      desc: "Reusable Paystack payment gateway deployed on Render powering an active Nairobi storefront on Mwingi Rd, Kileleshwa."
    },
    {
      name: "agents & rag-qa-system",
      lang: "Python",
      desc: "Autonomous multi-agent workflows, tool execution loops, and retrieval-augmented generation pipelines."
    },
    {
      name: "colibri",
      lang: "C",
      desc: "Frontier MoE model inference runner implemented in pure C with zero dependencies, streaming active experts directly from NVMe/disk."
    },
    {
      name: "cuckoo & rodent-app",
      lang: "Kotlin",
      desc: "Native Android utility and research applications built with Kotlin and coroutines."
    },
    {
      name: "tcp",
      lang: "Shell / Networking",
      desc: "Tailscale mesh network bridging Android mobile devices and development workstations."
    }
  ]
};

const chatHistory = document.getElementById("chatHistory");
const chatInput = document.getElementById("chatInput");
const sendBtn = document.getElementById("sendBtn");

function addMessage(role, text) {
  const msgEl = document.createElement("div");
  msgEl.className = `message ${role}`;
  
  const avatar = document.createElement("div");
  avatar.className = "message-avatar";
  avatar.innerHTML = role === "user" ? "👤" : "⚡";
  
  const content = document.createElement("div");
  content.className = "message-content";
  
  // Format markdown bold and code ticks
  let formatted = text
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/`(.*?)`/g, '<code>$1</code>')
    .replace(/\n/g, '<br>');
  
  content.innerHTML = formatted;
  
  msgEl.appendChild(avatar);
  msgEl.appendChild(content);
  chatHistory.appendChild(msgEl);
  
  chatHistory.scrollTop = chatHistory.scrollHeight;
}

function answerLocally(query) {
  const q = query.toLowerCase();
  
  if (q.includes("achievement") || q.includes("badge")) {
    return "Marcus has earned 3 official GitHub Achievements on his profile ([@engineermarcus](https://github.com/engineermarcus)):\n- 🎯 **Quickdraw**: Closed an issue or PR within 5 minutes.\n- 🦈 **Pull Shark**: Pull requests merged across projects.\n- ⚡ **YOLO**: Merged PRs without review, demonstrating rapid agile delivery.";
  }
  
  if (q.includes("moviebox") || q.includes("magpie") || q.includes("termux")) {
    return "The **moviebox-api** (Magpie CLI) is a standout engineering feat: it runs directly inside **Termux on Android** via a proot Ubuntu container. It drives headless Chromium using Playwright to bypass anti-bot challenges, score candidates, and stream media down in chunks via httpx with live progress bars and optional Internet Archive upload.";
  }
  
  if (q.includes("cybernetics") || q.includes("positron") || q.includes("shell") || q.includes("ide")) {
    return "**Cybernetics & Positron** is a browser-based Linux shell and IDE deployable anywhere via npm. Once authenticated, it creates a secure tunneled HTTPS session into a cloud terminal bundled with an AI voice assistant, Monaco-based code editor, and media inspection utilities.";
  }
  
  if (q.includes("paystack") || q.includes("store") || q.includes("am2pm") || q.includes("client")) {
    return "**Marcus Enterprises** is a reusable Node/Express payment gateway built by Marcus and deployed on Render. It powers the live e-commerce platform for **AM2PM Liquor Store** in Kileleshwa, Nairobi, handling catalog lookups, checkout sessions, and webhook reconciliation.";
  }
  
  if (q.includes("ai") || q.includes("agent") || q.includes("rag") || q.includes("llm") || q.includes("qwen")) {
    return "Marcus's AI focus centers on **practical agentic automation & efficient inference**:\n- **Agent Frameworks**: State-machine and DAG-based autonomous agents with tool calling.\n- **Local Model Optimization**: Running compact Qwen 2.5 (1B-7B) models and frontier MoE engines (Colibri in pure C).\n- **Retrieval-Augmented Generation**: Vector search and context retrieval (`rag-qa-system`).\n- **Real-Time Multimodal**: Real-time voice & vision agents with Gemini Live API.";
  }
  
  if (q.includes("contact") || q.includes("hire") || q.includes("email") || q.includes("reach")) {
    return "You can reach Neiman Marcus at **engineermarcus72@gmail.com** or via his GitHub at **github.com/engineermarcus**. He is open to software engineering, AI systems, and automation roles.";
  }
  
  return `Marcus has built over 32 public repositories across AI agents, Linux dev environments, and production backends. Some top repositories to check out: **cybernetics**, **moviebox-api**, **agents**, **rag-qa-system**, **colibri**, and **cuckoo**!`;
}

async function handleSend() {
  const text = chatInput.value.trim();
  if (!text) return;
  
  addMessage("user", text);
  chatInput.value = "";
  
  // Show typing indicator
  const typingIndicator = document.createElement("div");
  typingIndicator.className = "message agent";
  typingIndicator.id = "typing";
  typingIndicator.innerHTML = `
    <div class="message-avatar">⚡</div>
    <div class="message-content"><em>Agent reasoning...</em></div>
  `;
  chatHistory.appendChild(typingIndicator);
  chatHistory.scrollTop = chatHistory.scrollHeight;
  
  setTimeout(() => {
    const el = document.getElementById("typing");
    if (el) el.remove();
    
    const reply = answerLocally(text);
    addMessage("agent", reply);
  }, 400);
}

sendBtn.addEventListener("click", handleSend);
chatInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter") handleSend();
});

// Quick prompt chips
document.querySelectorAll(".chip").forEach(chip => {
  chip.addEventListener("click", () => {
    chatInput.value = chip.getAttribute("data-prompt") || chip.innerText;
    handleSend();
  });
});
