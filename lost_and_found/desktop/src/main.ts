import { app, BrowserWindow, ipcMain } from "electron";
import path from "path";
import fetch from "node-fetch";

const createWindow = () => {
  const win = new BrowserWindow({
    width: 1024,
    height: 768,
    webPreferences: {
      preload: path.join(__dirname, "preload.js"),
      contextIsolation: true,
      nodeIntegration: false,
    },
  });
  win.loadURL("http://localhost:5173");
};

app.whenReady().then(() => {
  createWindow();
  app.on("activate", () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") app.quit();
});

// fetch IPC
ipcMain.handle("fetch", async (_event, url, options) => {
  const res = await fetch(url, options);
  const data = await res.json();
  return data;
});
