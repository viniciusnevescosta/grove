const storageKey = "grove-theme";
const root = document.documentElement;
const saved = window.localStorage.getItem(storageKey);
const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
const mode = saved === "night" || saved === "mist" ? saved : prefersDark ? "night" : "mist";

root.dataset.theme = mode === "night" ? "still-orbit-night" : "still-orbit-mist";
root.classList.toggle("dark", mode === "night");
