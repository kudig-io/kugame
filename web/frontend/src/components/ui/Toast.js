// Toast 通知系统
const toastContainer = document.createElement("div");
toastContainer.id = "toast-container";
toastContainer.className = "fixed bottom-4 right-4 z-50 flex flex-col gap-2";
document.body.appendChild(toastContainer);

export function toast({ title, description, variant = "default", duration = 3000 }) {
  const toastEl = document.createElement("div");
  toastEl.className = `
    pointer-events-auto relative flex w-full max-w-sm items-center justify-between 
    space-x-4 overflow-hidden rounded-md border p-4 pr-6 shadow-lg transition-all
    ${variant === "default" ? "bg-background text-foreground" : ""}
    ${variant === "success" ? "bg-green-500/10 border-green-500/20 text-green-500" : ""}
    ${variant === "error" ? "bg-red-500/10 border-red-500/20 text-red-500" : ""}
    ${variant === "warning" ? "bg-yellow-500/10 border-yellow-500/20 text-yellow-500" : ""}
    ${variant === "info" ? "bg-blue-500/10 border-blue-500/20 text-blue-500" : ""}
    animate-in slide-in-from-bottom-2 fade-in duration-300
  `;
  
  const content = document.createElement("div");
  content.className = "flex-1";
  
  if (title) {
    const titleEl = document.createElement("h4");
    titleEl.className = "font-semibold text-sm";
    titleEl.textContent = title;
    content.appendChild(titleEl);
  }
  
  if (description) {
    const descEl = document.createElement("p");
    descEl.className = "text-sm opacity-90";
    descEl.textContent = description;
    content.appendChild(descEl);
  }
  
  toastEl.appendChild(content);
  
  // 关闭按钮
  const closeBtn = document.createElement("button");
  closeBtn.className = "absolute right-2 top-2 rounded-md p-1 opacity-50 hover:opacity-100";
  closeBtn.innerHTML = "<svg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><path d='m18 6-12 12'/><path d='m6 6 12 12'/></svg>";
  closeBtn.onclick = () => removeToast(toastEl);
  toastEl.appendChild(closeBtn);
  
  toastContainer.appendChild(toastEl);
  
  // 自动关闭
  setTimeout(() => removeToast(toastEl), duration);
  
  return toastEl;
}

function removeToast(toastEl) {
  toastEl.style.opacity = "0";
  toastEl.style.transform = "translateX(100%)";
  setTimeout(() => toastEl.remove(), 300);
}

// 快捷方法
toast.success = (title, description) => toast({ title, description, variant: "success" });
toast.error = (title, description) => toast({ title, description, variant: "error" });
toast.warning = (title, description) => toast({ title, description, variant: "warning" });
toast.info = (title, description) => toast({ title, description, variant: "info" });
