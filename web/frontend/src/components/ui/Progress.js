import { cn } from "../../lib/utils.js";

export function Progress({ value = 0, max = 100, className, color = "primary" }) {
  const percentage = Math.min(100, Math.max(0, (value / max) * 100));
  
  const container = document.createElement("div");
  container.className = cn(
    "relative h-2 w-full overflow-hidden rounded-full bg-muted",
    className
  );
  
  const indicator = document.createElement("div");
  indicator.className = cn(
    "h-full transition-all duration-300 ease-out",
    {
      "bg-primary": color === "primary",
      "bg-red-500": color === "health",
      "bg-blue-500": color === "mana",
      "bg-yellow-500": color === "exp",
      "bg-green-500": color === "success",
    }
  );
  indicator.style.width = `${percentage}%`;
  
  container.appendChild(indicator);
  
  // 添加数据属性用于更新
  container.dataset.value = value;
  container.dataset.max = max;
  
  return container;
}

// 带标签的进度条
export function ProgressWithLabel({ value, max, label, className, color }) {
  const wrapper = document.createElement("div");
  wrapper.className = "space-y-1";
  
  const labelRow = document.createElement("div");
  labelRow.className = "flex justify-between text-xs text-muted-foreground";
  labelRow.innerHTML = `
    <span>${label}</span>
    <span>${value}/${max}</span>
  `;
  
  wrapper.appendChild(labelRow);
  wrapper.appendChild(Progress({ value, max, className, color }));
  
  return wrapper;
}
