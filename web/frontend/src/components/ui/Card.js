import { cn } from "../../lib/utils.js";

export function Card({ children, className, ...props }) {
  const card = document.createElement("div");
  card.className = cn(
    "rounded-xl border bg-card text-card-foreground shadow",
    className
  );
  card.innerHTML = children;
  
  Object.entries(props).forEach(([key, value]) => {
    card.setAttribute(key, value);
  });
  
  return card;
}

export function CardHeader({ children, className }) {
  const header = document.createElement("div");
  header.className = cn("flex flex-col space-y-1.5 p-6", className);
  header.innerHTML = children;
  return header;
}

export function CardTitle({ children, className }) {
  const title = document.createElement("h3");
  title.className = cn("font-semibold leading-none tracking-tight", className);
  title.innerHTML = children;
  return title;
}

export function CardDescription({ children, className }) {
  const desc = document.createElement("p");
  desc.className = cn("text-sm text-muted-foreground", className);
  desc.innerHTML = children;
  return desc;
}

export function CardContent({ children, className }) {
  const content = document.createElement("div");
  content.className = cn("p-6 pt-0", className);
  content.innerHTML = children;
  return content;
}

export function CardFooter({ children, className }) {
  const footer = document.createElement("div");
  footer.className = cn("flex items-center p-6 pt-0", className);
  footer.innerHTML = children;
  return footer;
}
