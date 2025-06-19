// Electron Preload: セキュアな IPC メソッド
import { contextBridge, ipcRenderer } from 'electron'

contextBridge.exposeInMainWorld('api', {
  fetch: (url: string, options?: RequestInit) =>
    ipcRenderer.invoke('fetch', url, options),
})
